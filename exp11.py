# iris_dt_nb_metrics.py
# Trains Decision Tree and Naive Bayes on Iris and prints train/test Accuracy & F1 (macro).
# Place Kaggle's Iris.csv (or IRIS.csv) beside this script.
# Kaggle columns: Id, SepalLengthCm, SepalWidthCm, PetalLengthCm, PetalWidthCm, Species

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, f1_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

def load_iris_dataframe():
    """Load Iris from a local CSV. Tries common Kaggle filenames."""
    for name in ["Iris.csv", "IRIS.csv"]:
        if os.path.exists(name):
            return pd.read_csv(name), name
    raise FileNotFoundError(
        "Iris dataset not found. Put 'Iris.csv' or 'IRIS.csv' in the same folder as this script."
    )

def split_X_y(df):
    """
    Robustly select features and label.
    Works for Kaggle (CamelCase) and other common variants.
    """
    # Candidate label columns (case-insensitive)
    label_candidates = ["Species", "species", "Class", "class", "variety"]
    label_col = None
    for c in label_candidates:
        if c in df.columns:
            label_col = c
            break
    if label_col is None:
        # Fallback: last non-numeric column
        non_numeric = df.select_dtypes(exclude=[np.number]).columns.tolist()
        if not non_numeric:
            raise ValueError("Could not find a non-numeric label column.")
        label_col = non_numeric[-1]

    # Drop obvious ID columns if present
    drop_cols = {label_col}
    for c in ["Id", "id", "ID", "index"]:
        if c in df.columns:
            drop_cols.add(c)

    # Features = numeric columns after dropping label/ID
    X_df = df.drop(columns=list(drop_cols), errors="ignore")
    X = X_df.select_dtypes(include=[np.number]).to_numpy()
    if X.shape[1] == 0:
        raise ValueError("No numeric feature columns found after dropping label/ID.")

    # Encode labels
    y_raw = df[label_col].astype(str)
    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    return X, y, le, label_col, X_df.columns.tolist(), df

def evaluate(model, X_train, y_train, X_test, y_test):
    model.fit(X_train, y_train)
    ytr = model.predict(X_train)
    yte = model.predict(X_test)
    return {
        "train_acc": accuracy_score(y_train, ytr),
        "train_f1":  f1_score(y_train, ytr, average="macro"),
        "test_acc":  accuracy_score(y_test, yte),
        "test_f1":   f1_score(y_test, yte, average="macro"),
    }

def main():
    df, fname = load_iris_dataframe()
    X, y, le, label_col, feature_names, _ = split_X_y(df)

    # Stratified split for fair class balance
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    dt = DecisionTreeClassifier(criterion="entropy", random_state=42)
    nb = GaussianNB()

    dt_res = evaluate(dt, X_tr, y_tr, X_te, y_te)
    nb_res = evaluate(nb, X_tr, y_tr, X_te, y_te)

    # Pretty print
    def fmt(res):
        return (f"Train Acc: {res['train_acc']:.4f} | Train F1: {res['train_f1']:.4f} | "
                f"Test Acc: {res['test_acc']:.4f} | Test F1: {res['test_f1']:.4f}")

    print("=== Iris: Decision Tree vs Naive Bayes ===")
    print(f"Loaded file           : {fname}")
    print(f"Detected label column : {label_col}")
    print(f"Feature columns       : {feature_names}")
    print(f"Train size: {len(y_tr)} | Test size: {len(y_te)} | Classes: {list(le.classes_)}\n")

    print("Decision Tree   ->", fmt(dt_res))
    print("Naive Bayes     ->", fmt(nb_res))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR:", e, file=sys.stderr)
        sys.exit(1)
