"""Training scaffold. Requires a defensible CSV with a binary target column 'accident'."""
import argparse
from pathlib import Path
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", required=True, help="CSV with feature columns and binary accident target")
    parser.add_argument("--target", default="accident")
    parser.add_argument("--output", default="models/accident_model.joblib")
    args = parser.parse_args()
    data = pd.read_csv(args.data)
    if args.target not in data: raise SystemExit(f"Missing target column: {args.target}")
    y = data.pop(args.target)
    if y.nunique() != 2: raise SystemExit("Target must contain exactly two classes.")
    numeric = data.select_dtypes(include="number").columns.tolist()
    categorical = [c for c in data.columns if c not in numeric]
    pre = ColumnTransformer([
        ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("encode", OneHotEncoder(handle_unknown="ignore"))]), categorical)
    ])
    model = Pipeline([("features", pre), ("classifier", RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=42, min_samples_leaf=3))])
    x_train, x_test, y_train, y_test = train_test_split(data, y, test_size=.2, random_state=42, stratify=y)
    model.fit(x_train, y_train)
    print(classification_report(y_test, model.predict(x_test)))
    if hasattr(model, "predict_proba"): print("ROC-AUC:", round(roc_auc_score(y_test, model.predict_proba(x_test)[:, 1]), 4))
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True); joblib.dump(model, out)
    print("Saved:", out)
    print("WARNING: random split is only a smoke-test; use time/geographic holdouts and calibration before claiming probability.")

if __name__ == "__main__": main()
