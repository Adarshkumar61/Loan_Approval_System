# train_model.py

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# ================= LOAD DATA =================

data = pd.read_csv("loan_approval.csv")  
# rename above file if needed

# ================= CLEAN DATA =================

# Drop non-informative column
data = data.drop(columns=["name"])

# Convert target to binary
data["loan_approved"] = data["loan_approved"].map({True: 1, False: 0})

# Remove missing values (safe, realistic)
data = data.dropna()

# ================= SPLIT FEATURES & TARGET =================

X = data.drop("loan_approved", axis=1)
y = data["loan_approved"]

# Identify column types
categorical_cols = ["city"]
numerical_cols = [
    "income",
    "credit_score",
    "loan_amount",
    "years_employed",
    "points"
]

# ================= PREPROCESSING =================

preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
        ("num", StandardScaler(), numerical_cols)
    ]
)

# ================= MODEL PIPELINE =================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(max_iter=1000))
    ]
)

# ================= TRAIN / TEST SPLIT =================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ================= TRAIN =================

model.fit(X_train, y_train)

# ================= EVALUATE =================

train_acc = accuracy_score(y_train, model.predict(X_train))
test_acc = accuracy_score(y_test, model.predict(X_test))

print(f"Training Accuracy: {train_acc:.2f}")
print(f"Testing Accuracy : {test_acc:.2f}")

# ================= SAVE MODEL =================

with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved as model.pkl")
