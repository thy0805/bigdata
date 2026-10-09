import numpy as np


POLICY = "D09:max(0,prediction_raw)"


def nonnegative(raw):
    values = np.asarray(raw, dtype=np.float64)
    if values.ndim != 1 or not np.isfinite(values).all():
        raise ValueError("Predictions must be a finite one-dimensional array")
    return np.maximum(0.0, values)


def predict_bundle(bundle, features):
    if bundle["prediction_policy"] != POLICY:
        raise ValueError("Unapproved prediction policy")
    if list(features.columns) != bundle["feature_columns"]:
        raise ValueError("Feature order/schema mismatch")
    if not np.isfinite(features.to_numpy(dtype=np.float64)).all():
        raise ValueError("Missing or non-finite feature values")
    raw = bundle["estimator"].predict(features)
    return raw, nonnegative(raw)
