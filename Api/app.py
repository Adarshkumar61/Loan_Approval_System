# # import os
# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # import pickle
# # from fastapi.responses import HTMLResponse

# # app = FastAPI()

# # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# # MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
# # HTML_PATH = os.path.join(BASE_DIR, "front_end.html")

# # model = pickle.load(open(MODEL_PATH, "rb"))

# # class UserData(BaseModel):
# #     age: int
# #     income: int

# # @app.post("/predict")
# # def predict(data: UserData):
# #     prediction = model.predict([[data.age, data.income]])
# #     return {
# #         "loan_status": "Approved" if prediction[0] == 1 else "Rejected"
# #     }

# # @app.get("/")
# # def home():
# #     return {"message": "API is running"}

# # @app.get("/ui", response_class=HTMLResponse)
# # def serve_ui():
# #     with open(HTML_PATH, "r", encoding="utf-8") as f:
# #         return f.read()
# # To run the app, use the command:
# # uvicorn api_test.app:app --reload

# import os
# import pickle
# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.responses import HTMLResponse
# from fastapi.staticfiles import StaticFiles

# app = FastAPI()

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
# HTML_PATH = os.path.join(BASE_DIR, "front_end.html")

# model = pickle.load(open(MODEL_PATH, "rb"))

# # serve static files (background image later)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# class UserData(BaseModel):
#     age: int
#     income: int
#     credit_score: int

# @app.post("/predict")
# def predict(data: UserData):
#     pred = model.predict([[data.age, data.income, data.credit_score]])[0]
#     prob = model.predict_proba([[data.age, data.income, data.credit_score]])[0][1]

#     return {
#         "status": "Approved" if pred == 1 else "Rejected",
#         "confidence": round(prob * 100, 2)
#     }

# @app.get("/", response_class=HTMLResponse)
# def ui():
#     with open(HTML_PATH, "r", encoding="utf-8") as f:
#         return f.read()


# app.py



import os
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# ================= APP INIT =================
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
HTML_PATH = os.path.join(BASE_DIR, "front_end.html")
STATIC_PATH = os.path.join(BASE_DIR, "static")

# ================= LOAD MODEL (ONCE) =================
model = pickle.load(open(MODEL_PATH, "rb"))

# ================= STATIC FILES =================
# This will NOT crash even if bg.jpg is missing
if os.path.exists(STATIC_PATH):
    app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")

# ================= INPUT SCHEMA =================
class LoanInput(BaseModel):
    city: str
    income: float
    credit_score: int
    loan_amount: float
    years_employed: int
    points: float

# ================= PREDICTION API =================
@app.post("/predict")
def predict_loan(data: LoanInput):
    df = pd.DataFrame([data.dict()])

    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]

    return {
        "loan_status": "Approved" if prediction == 1 else "Rejected",
        "confidence": round(probability * 100, 2)
    }

# ================= UI ROUTE =================
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    if not os.path.exists(HTML_PATH):
        return "<h1>front_end.html not found</h1>"

    with open(HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()
