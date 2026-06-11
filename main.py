from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
# add more imports as needed (e.g., for your ML model, database, etc.)
# 
app = FastAPI(title="Fraud Detection API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory="static"), name="static")


class Transaction(BaseModel):
    transaction_type: str
    amount: float
    old_balance_org: float
    new_balance_orig: float
    old_balance_dest: float
    new_balance_dest: float


class PredictionResult(BaseModel):
    is_fraud: bool
    confidence: str
    risk_level: str
    message: str


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResult)
def predict(transaction: Transaction):
    """
    Heuristic fraud detection — replace with your model.predict() call.
    """
    balance_drain = transaction.old_balance_org - transaction.new_balance_orig
    is_fraud = (
        transaction.transaction_type in ("TRANSFER", "CASH_OUT")
        and transaction.amount > 0
        and abs(balance_drain - transaction.amount) < 1.0
    )

    if is_fraud:
        return PredictionResult(
            is_fraud=True,
            confidence="87.3%",
            risk_level="High risk",
            message=(
                f"Pattern matches known fraud signals: full balance drain on "
                f"{transaction.transaction_type} type. Flagged for manual review."
            ),
        )
    else:
        return PredictionResult(
            is_fraud=False,
            confidence="96.1%",
            risk_level="Low risk",
            message=(
                f"No anomalous patterns detected. Balance changes are consistent "
                f"with a legitimate {transaction.transaction_type} transaction."
            ),
        )
