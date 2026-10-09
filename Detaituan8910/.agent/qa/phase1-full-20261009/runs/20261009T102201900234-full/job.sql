SET 'execution.runtime-mode' = 'BATCH';
SET 'execution.target' = 'remote';
SET 'rest.address' = 'localhost';
SET 'rest.port' = '8081';
SET 'parallelism.default' = '1';
SET 'table.dml-sync' = 'true';
SET 'restart-strategy.type' = 'none';
SET 'pipeline.name' = 'uci-full-20261009T102201900234-full';

CREATE TABLE raw_input (
  d STRING, t STRING, p STRING, r STRING, v STRING, a STRING,
  s1 STRING, s2 STRING, s3 STRING
) WITH (
  'connector' = 'filesystem', 'path' = 'file:///mnt/d/Hoctap/bigdata/Detaituan8910/data/raw/household_power_consumption.txt', 'format' = 'csv',
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
  CONCAT(SPLIT_INDEX(d, '/', 2), '-', LPAD(SPLIT_INDEX(d, '/', 1), 2, '0'), '-', LPAD(SPLIT_INDEX(d, '/', 0), 2, '0'), ' ', t) AS iso_stamp,
  CASE WHEN p IS NULL OR TRIM(p) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM(p) END AS power_kw_text,
  CASE WHEN r IS NULL OR TRIM(r) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM(r) END AS reactive_text,
  CASE WHEN v IS NULL OR TRIM(v) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM(v) END AS voltage_text,
  CASE WHEN a IS NULL OR TRIM(a) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM(a) END AS intensity_text,
  CASE WHEN s1 IS NULL OR TRIM(s1) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM(s1) END AS sub1_wh_text,
  CASE WHEN s2 IS NULL OR TRIM(s2) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM(s2) END AS sub2_wh_text,
  CASE WHEN s3 IS NULL OR TRIM(s3) IN ('', '?') THEN CAST(NULL AS STRING) ELSE TRIM(s3) END AS sub3_wh_text
FROM tagged WHERE NOT is_header;

CREATE VIEW parsed AS
SELECT *,
  TRY_CAST(iso_stamp AS TIMESTAMP(3)) AS event_time,
  CASE WHEN REGEXP(power_kw_text, '^[+]?[0-9]+([.][0-9]{1,6})?$') THEN TRY_CAST(power_kw_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS power_kw,
  CASE WHEN REGEXP(reactive_text, '^[+]?[0-9]+([.][0-9]{1,6})?$') THEN TRY_CAST(reactive_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS reactive,
  CASE WHEN REGEXP(voltage_text, '^[+]?[0-9]+([.][0-9]{1,6})?$') THEN TRY_CAST(voltage_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS voltage,
  CASE WHEN REGEXP(intensity_text, '^[+]?[0-9]+([.][0-9]{1,6})?$') THEN TRY_CAST(intensity_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS intensity,
  CASE WHEN REGEXP(sub1_wh_text, '^[+]?[0-9]+([.][0-9]{1,6})?$') THEN TRY_CAST(sub1_wh_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS sub1_wh,
  CASE WHEN REGEXP(sub2_wh_text, '^[+]?[0-9]+([.][0-9]{1,6})?$') THEN TRY_CAST(sub2_wh_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS sub2_wh,
  CASE WHEN REGEXP(sub3_wh_text, '^[+]?[0-9]+([.][0-9]{1,6})?$') THEN TRY_CAST(sub3_wh_text AS DECIMAL(18,6)) ELSE CAST(NULL AS DECIMAL(18,6)) END AS sub3_wh
FROM cleaned;

CREATE VIEW checked AS
SELECT *,
  NOT COALESCE(REGEXP(d, '^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$') AND REGEXP(t, '^[0-9]{2}:[0-9]{2}:00$'), FALSE)
  OR event_time IS NULL OR COALESCE(DATE_FORMAT(event_time, 'yyyy-MM-dd HH:mm:ss') <> iso_stamp, TRUE)
  OR (power_kw_text IS NOT NULL AND power_kw IS NULL) OR (reactive_text IS NOT NULL AND reactive IS NULL) OR (voltage_text IS NOT NULL AND voltage IS NULL) OR (intensity_text IS NOT NULL AND intensity IS NULL) OR (sub1_wh_text IS NOT NULL AND sub1_wh IS NULL) OR (sub2_wh_text IS NOT NULL AND sub2_wh IS NULL) OR (sub3_wh_text IS NOT NULL AND sub3_wh IS NULL) AS parse_error,
  CASE WHEN power_kw_text IS NULL THEN 1 ELSE 0 END + CASE WHEN reactive_text IS NULL THEN 1 ELSE 0 END + CASE WHEN voltage_text IS NULL THEN 1 ELSE 0 END + CASE WHEN intensity_text IS NULL THEN 1 ELSE 0 END + CASE WHEN sub1_wh_text IS NULL THEN 1 ELSE 0 END + CASE WHEN sub2_wh_text IS NULL THEN 1 ELSE 0 END + CASE WHEN sub3_wh_text IS NULL THEN 1 ELSE 0 END AS missing_cells
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
) WITH ('connector' = 'filesystem', 'path' = 'file:///mnt/d/Hoctap/bigdata/Detaituan8910/data/processed/runs/20261009T102201900234-full/flink-parts/hourly', 'format' = 'csv', 'csv.null-literal' = 'NULL');

CREATE TABLE metrics_sink (
  total_input_rows BIGINT, header_rows BIGINT, data_rows BIGINT, parse_error_rows BIGINT, missing_cells BIGINT
) WITH ('connector' = 'filesystem', 'path' = 'file:///mnt/d/Hoctap/bigdata/Detaituan8910/data/processed/runs/20261009T102201900234-full/flink-parts/metrics', 'format' = 'csv', 'csv.null-literal' = 'NULL');

CREATE TABLE minute_sink (
  d STRING, t STRING, event_time TIMESTAMP(3), parse_error BOOLEAN, missing_cells INTEGER,
  power_kw DECIMAL(18,6), sub1_wh DECIMAL(18,6), sub2_wh DECIMAL(18,6), sub3_wh DECIMAL(18,6), residual_wh DOUBLE,
  p STRING, r STRING, v STRING, a STRING, s1 STRING, s2 STRING, s3 STRING
) WITH ('connector' = 'filesystem', 'path' = 'file:///mnt/d/Hoctap/bigdata/Detaituan8910/data/processed/runs/20261009T102201900234-full/flink-parts/minutes', 'format' = 'csv', 'csv.null-literal' = 'NULL');

CREATE TABLE duplicate_sink (
  event_time TIMESTAMP(3), occurrences BIGINT
) WITH ('connector' = 'filesystem', 'path' = 'file:///mnt/d/Hoctap/bigdata/Detaituan8910/data/processed/runs/20261009T102201900234-full/flink-parts/duplicates', 'format' = 'csv', 'csv.null-literal' = 'NULL');

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
