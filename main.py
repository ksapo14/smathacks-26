"""
Bycatch Risk Prediction — FastAPI Backend
-----------------------------------------
Requirements: pip install fastapi uvicorn pandas scikit-learn openpyxl

Run:          uvicorn main:app --reload
API docs:     http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import warnings

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# MODEL TRAINING (runs once on startup)
# ---------------------------------------------------------------------------

DATA_PATH  = "bycatch_dataset.xlsx"
SHEET_NAME = "Bycatch_Data"
SEED       = 42

FEATURE_COLS = [
    "Latitude (\u00b0)", "Longitude (\u00b0)", "Sea Surface Temp (\u00b0C)",
    "Current Speed (kn)", "dir_enc", "Hour of Day (0\u201323)",
    "mig_enc", "sp_enc", "fate_enc",
]

def build_model():
    df = pd.read_excel(DATA_PATH, sheet_name=SHEET_NAME)
    df["label"] = (df["Bycatch Present"] == "Present").astype(int)

    encoders = {}
    for col, new_col in [
        ("Current Direction", "dir_enc"),
        ("Migration Pattern", "mig_enc"),
        ("Target Species",    "sp_enc"),
        ("Species Fate",      "fate_enc"),
    ]:
        le = LabelEncoder()
        df[new_col] = le.fit_transform(df[col])
        encoders[col] = le

    X = df[FEATURE_COLS].values
    y = df["label"].values
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)

    model = GradientBoostingClassifier(
        n_estimators=200, learning_rate=0.1, max_depth=4,
        min_samples_split=10, subsample=0.8, random_state=SEED,
    )
    model.fit(X_train, y_train)
    return model, encoders

print("Training model...")
MODEL, ENCODERS = build_model()
print("Model ready.")

# ---------------------------------------------------------------------------
# VALID CATEGORIES (returned to the UI for dropdowns)
# ---------------------------------------------------------------------------

VALID = {
    "current_dir": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
    "migration":   ["Northward", "Southward", "Eastward", "Westward", "Stationary"],
    "species":     ["Yellowfin Tuna", "Bigeye Tuna", "Wahoo", "Mahi-Mahi", "Striped Marlin"],
    "fate":        ["Kept", "Discarded"],
}

# ---------------------------------------------------------------------------
# FASTAPI APP
# ---------------------------------------------------------------------------

app = FastAPI(title="Bycatch Risk API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (your HTML UI) from a 'static' folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# ---------------------------------------------------------------------------
# REQUEST / RESPONSE SCHEMAS
# ---------------------------------------------------------------------------

class PredictRequest(BaseModel):
    lat:           float = Field(..., ge=-35,  le=35,  example=5.0)
    lon:           float = Field(..., ge=40,   le=160, example=65.0)
    sst:           float = Field(..., ge=5,    le=35,  example=28.2)
    current_speed: float = Field(..., ge=0,    le=10,  example=2.1)
    current_dir:   str   = Field(...,                  example="NE")
    hour:          int   = Field(..., ge=0,    le=23,  example=6)
    migration:     str   = Field(...,                  example="Northward")
    species:       str   = Field(...,                  example="Yellowfin Tuna")
    fate:          str   = Field(...,                  example="Kept")

class PredictResponse(BaseModel):
    probability: float
    risk_label:  str
    risk_pct:    str

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.get("/")
def serve_ui():
    """Serve the HTML frontend."""
    return FileResponse("static/index.html")


@app.get("/options")
def get_options():
    """Return valid dropdown values for the UI."""
    return VALID


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """Run a single bycatch risk prediction."""
    def encode(col, val):
        le = ENCODERS[col]
        return int(le.transform([val])[0]) if val in le.classes_ else 0

    X_new = np.array([[
        req.lat, req.lon, req.sst, req.current_speed,
        encode("Current Direction", req.current_dir),
        req.hour,
        encode("Migration Pattern", req.migration),
        encode("Target Species",    req.species),
        encode("Species Fate",      req.fate),
    ]])

    prob = float(MODEL.predict_proba(X_new)[0, 1])

    return PredictResponse(
        probability = round(prob, 4),
        risk_label  = "High Risk" if prob >= 0.5 else "Low Risk",
        risk_pct    = f"{prob:.1%}",
    )