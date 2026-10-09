SET 'execution.runtime-mode' = 'BATCH';
SET 'execution.target' = 'remote';
SET 'rest.address' = 'localhost';
SET 'rest.port' = '8081';
SET 'parallelism.default' = '1';
SET 'table.dml-sync' = 'true';
SET 'restart-strategy.type' = 'none';
SET 'pipeline.name' = '{{JOB_NAME}}';

CREATE TABLE raw_input (
  d STRING, t STRING, p STRING, r STRING, v STRING, a STRING,
  s1 STRING, s2 STRING, s3 STRING
) WITH (
  'connector' = 'filesystem', 'path' = '{{SOURCE}}', 'format' = 'csv',
  'csv.field-delimiter' = ';', 'csv.ignore-parse-errors' = 'false',
  'csv.fail-on-missing-columns' = 'true', 'csv.ignore-trailing-unmappable' = 'false',
  'csv.allow-trailing-comma' = 'false', 'csv.empty-string-as-null' = 'false'
);

CREATE VIEW tagged AS
SELECT *, COALESCE(d = 'Date' AND t = 'Time' AND p = 'Global_active_power'
  AND r = 'Global_reactive_power' AND v = 'Voltage' AND a = 'Global_intensity'
  AND s1 = 'Sub_metering_1' AND s2 = 'Sub_metering_2' AND s3 = 'Sub_metering_3', FALSE) AS is_header
FROM raw_input;

CREATE VIEW cleaned AS
SELECT d, t, p, r, v, a, s1, s2, s3,
  CONCAT(SUBSTRING(d, 7, 4), '-', SUBSTRING(d, 4, 2), '-', SUBSTRING(d, 1, 2), ' ', t) AS iso_stamp,
  {{CLEAN_COLUMNS}}
FROM tagged WHERE NOT is_header;

CREATE VIEW parsed AS
SELECT *,
  TRY_CAST(iso_stamp AS TIMESTAMP(3)) AS event_time,
  {{PARSE_COLUMNS}}
FROM cleaned;

CREATE VIEW checked AS
SELECT *,
  NOT COALESCE(REGEXP(d, '^[0-9]{2}/[0-9]{2}/[0-9]{4}$') AND REGEXP(t, '^[0-9]{2}:[0-9]{2}:00$'), FALSE)
  OR event_time IS NULL OR COALESCE(DATE_FORMAT(event_time, 'yyyy-MM-dd HH:mm:ss') <> iso_stamp, TRUE)
  OR {{ERROR_COLUMNS}} AS parse_error,
  {{MISSING_COLUMNS}} AS missing_cells
FROM parsed;

CREATE VIEW minute_rows AS
SELECT d, t, event_time, parse_error, missing_cells, power_kw, sub1_wh, sub2_wh, sub3_wh,
  CAST(power_kw * 1000 - 60 * (sub1_wh + sub2_wh + sub3_wh) AS DOUBLE) / 60.0 AS residual_wh,
  p, r, v, a, s1, s2, s3
FROM checked;

CREATE VIEW hourly_base AS
SELECT FLOOR(event_time TO HOUR) AS hour_start,
  COUNT(*) AS record_count, COUNT(DISTINCT event_time) AS distinct_minute_count,
  COUNT(power_kw) AS valid_power_count,
  CAST(SUM(power_kw) AS DOUBLE) / 60.0 AS observed_energy_kwh,
  COUNT(sub1_wh) AS sub1_valid_count, COUNT(sub2_wh) AS sub2_valid_count, COUNT(sub3_wh) AS sub3_valid_count,
  CAST(SUM(sub1_wh) AS DOUBLE) / 1000.0 AS sub1_observed_kwh,
  CAST(SUM(sub2_wh) AS DOUBLE) / 1000.0 AS sub2_observed_kwh,
  CAST(SUM(sub3_wh) AS DOUBLE) / 1000.0 AS sub3_observed_kwh,
  SUM(CASE WHEN residual_wh < 0 THEN CAST(1 AS BIGINT) ELSE CAST(0 AS BIGINT) END) AS negative_residual_count
FROM minute_rows WHERE NOT parse_error GROUP BY FLOOR(event_time TO HOUR);

CREATE TABLE hourly_sink (
  hour_start TIMESTAMP(3), record_count BIGINT, distinct_minute_count BIGINT, valid_power_count BIGINT,
  observed_energy_kwh DOUBLE, is_complete BOOLEAN, energy_kwh DOUBLE,
  sub1_valid_count BIGINT, sub2_valid_count BIGINT, sub3_valid_count BIGINT,
  sub1_observed_kwh DOUBLE, sub2_observed_kwh DOUBLE, sub3_observed_kwh DOUBLE,
  negative_residual_count BIGINT
) WITH ('connector' = 'filesystem', 'path' = '{{OUTPUT}}/hourly', 'format' = 'csv', 'csv.null-literal' = 'NULL');

CREATE TABLE metrics_sink (
  total_input_rows BIGINT, header_rows BIGINT, data_rows BIGINT, parse_error_rows BIGINT, missing_cells BIGINT
) WITH ('connector' = 'filesystem', 'path' = '{{OUTPUT}}/metrics', 'format' = 'csv', 'csv.null-literal' = 'NULL');

CREATE TABLE minute_sink (
  d STRING, t STRING, event_time TIMESTAMP(3), parse_error BOOLEAN, missing_cells INTEGER,
  power_kw DECIMAL(18,6), sub1_wh DECIMAL(18,6), sub2_wh DECIMAL(18,6), sub3_wh DECIMAL(18,6), residual_wh DOUBLE,
  p STRING, r STRING, v STRING, a STRING, s1 STRING, s2 STRING, s3 STRING
) WITH ('connector' = 'filesystem', 'path' = '{{OUTPUT}}/minutes', 'format' = 'csv', 'csv.null-literal' = 'NULL');

CREATE TABLE duplicate_sink (
  event_time TIMESTAMP(3), occurrences BIGINT
) WITH ('connector' = 'filesystem', 'path' = '{{OUTPUT}}/duplicates', 'format' = 'csv', 'csv.null-literal' = 'NULL');

EXECUTE STATEMENT SET
BEGIN
INSERT INTO hourly_sink
SELECT hour_start, record_count, distinct_minute_count, valid_power_count, observed_energy_kwh,
  record_count = 60 AND distinct_minute_count = 60 AND valid_power_count = 60,
  CASE WHEN record_count = 60 AND distinct_minute_count = 60 AND valid_power_count = 60
    THEN observed_energy_kwh ELSE CAST(NULL AS DOUBLE) END,
  sub1_valid_count, sub2_valid_count, sub3_valid_count,
  sub1_observed_kwh, sub2_observed_kwh, sub3_observed_kwh, negative_residual_count
FROM hourly_base;
INSERT INTO metrics_sink
SELECT COUNT(*), SUM(CASE WHEN is_header THEN CAST(1 AS BIGINT) ELSE CAST(0 AS BIGINT) END),
  (SELECT COUNT(*) FROM minute_rows),
  (SELECT COUNT(*) FROM minute_rows WHERE parse_error),
  (SELECT COALESCE(SUM(CAST(missing_cells AS BIGINT)), CAST(0 AS BIGINT)) FROM minute_rows)
FROM tagged;
INSERT INTO minute_sink SELECT * FROM minute_rows;
INSERT INTO duplicate_sink
SELECT event_time, COUNT(*) FROM minute_rows WHERE NOT parse_error GROUP BY event_time HAVING COUNT(*) > 1;
END;
