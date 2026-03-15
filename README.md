# Bycatch Risk Prediction API

A machine learning-powered FastAPI backend that predicts the risk of bycatch (unintended catch of marine species) in fishing operations based on environmental and operational parameters.

## 📋 Overview

This API uses a Gradient Boosting Classifier to predict bycatch probability based on:
- Geographic location (latitude/longitude)
- Environmental conditions (sea surface temperature, ocean currents)
- Temporal factors (time of day)
- Fishing operation details (target species, migration patterns, species fate)

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

1. **Clone or download this project**

2. **Install dependencies**
   ```bash
   pip install fastapi uvicorn pandas scikit-learn openpyxl
   ```

3. **Prepare your data**
   - Ensure `bycatch_dataset.xlsx` is in the project root
   - The Excel file should have a sheet named `Bycatch_Data`

4. **Create a `static` folder for the frontend**
   ```bash
   mkdir static
   ```
   Place your `index.html` (web interface) in this folder.

### Running the Server

```bash
uvicorn main:app --reload
```

The API will start at: `http://127.0.0.1:8000`

- **Web Interface**: http://127.0.0.1:8000
- **Interactive API Docs**: http://127.0.0.1:8000/docs
- **Alternative Docs**: http://127.0.0.1:8000/redoc

## 📊 Data Requirements

Your Excel file (`bycatch_dataset.xlsx`) must contain the following columns:

### Required Columns

| Column Name | Type | Description |
|------------|------|-------------|
| `Latitude (°)` | Float | Geographic latitude (-35 to 35) |
| `Longitude (°)` | Float | Geographic longitude (40 to 160) |
| `Sea Surface Temp (°C)` | Float | Water temperature (5 to 35°C) |
| `Current Speed (kn)` | Float | Ocean current speed (0 to 10 knots) |
| `Current Direction` | String | One of: N, NE, E, SE, S, SW, W, NW |
| `Hour of Day (0–23)` | Integer | Time of fishing operation (0-23) |
| `Migration Pattern` | String | Northward, Southward, Eastward, Westward, Stationary |
| `Target Species` | String | Yellowfin Tuna, Bigeye Tuna, Wahoo, Mahi-Mahi, Striped Marlin |
| `Species Fate` | String | Kept or Discarded |
| `Bycatch Present` | String | "Present" or "Absent" (target variable) |

## 🔌 API Endpoints

### 1. GET `/`
Serves the HTML frontend interface.

**Response**: HTML page

---

### 2. GET `/options`
Returns valid values for dropdown fields in the UI.

**Response**:
```json
{
  "current_dir": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"],
  "migration": ["Northward", "Southward", "Eastward", "Westward", "Stationary"],
  "species": ["Yellowfin Tuna", "Bigeye Tuna", "Wahoo", "Mahi-Mahi", "Striped Marlin"],
  "fate": ["Kept", "Discarded"]
}
```

---

### 3. POST `/predict`
Predicts bycatch risk for given parameters.

**Request Body**:
```json
{
  "lat": 5.0,
  "lon": 65.0,
  "sst": 28.2,
  "current_speed": 2.1,
  "current_dir": "NE",
  "hour": 6,
  "migration": "Northward",
  "species": "Yellowfin Tuna",
  "fate": "Kept"
}
```

**Validation Rules**:
- `lat`: -35 to 35
- `lon`: 40 to 160
- `sst`: 5 to 35
- `current_speed`: 0 to 10
- `hour`: 0 to 23
- Categorical fields must match allowed values

**Response**:
```json
{
  "probability": 0.7234,
  "risk_label": "High Risk",
  "risk_pct": "72.3%"
}
```

## 🤖 Machine Learning Model

### Algorithm
**Gradient Boosting Classifier** - An ensemble method that builds multiple decision trees sequentially, with each tree correcting errors from previous ones.

### Model Configuration
```python
n_estimators=200      # 200 decision trees
learning_rate=0.1     # Step size for corrections
max_depth=4           # Maximum tree depth
min_samples_split=10  # Minimum samples to split a node
subsample=0.8         # 80% data sampling per tree
random_state=42       # Reproducible results
```

### Training Process
1. **Data Loading**: Reads Excel file
2. **Label Creation**: Converts "Present"/"Absent" to 1/0
3. **Encoding**: Transforms categorical variables (direction, species, etc.) to numeric
4. **Train/Test Split**: 80% training, 20% testing (stratified)
5. **Model Training**: Fits Gradient Boosting model
6. **Persistence**: Stores model and encoders in memory

### Features Used (9 total)
1. Latitude
2. Longitude
3. Sea Surface Temperature
4. Current Speed
5. Current Direction (encoded)
6. Hour of Day
7. Migration Pattern (encoded)
8. Target Species (encoded)
9. Species Fate (encoded)

## 📁 Project Structure

```
bycatch-risk-api/
├── main.py                    # FastAPI backend (this file)
├── bycatch_dataset.xlsx       # Training data
├── static/
│   └── index.html            # Web interface
├── README.md                  # This file
└── requirements.txt           # (Optional) Dependency list
```

## 🛠️ Technical Details

### CORS Configuration
The API allows cross-origin requests from any domain (`allow_origins=["*"]`). For production, restrict this to your specific domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Label Encoding
Categorical variables are converted to integers using scikit-learn's `LabelEncoder`:
- **Current Direction**: N→0, NE→1, E→2, etc.
- **Migration Pattern**: Northward→0, Southward→1, etc.
- **Target Species**: Yellowfin Tuna→0, Bigeye Tuna→1, etc.
- **Species Fate**: Kept→0, Discarded→1

Encoders are saved and reused for predictions to ensure consistency.

### Risk Classification
- **High Risk**: Probability ≥ 50%
- **Low Risk**: Probability < 50%

## 🧪 Testing the API

### Using cURL
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "lat": 5.0,
    "lon": 65.0,
    "sst": 28.2,
    "current_speed": 2.1,
    "current_dir": "NE",
    "hour": 6,
    "migration": "Northward",
    "species": "Yellowfin Tuna",
    "fate": "Kept"
  }'
```

### Using Python
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={
        "lat": 5.0,
        "lon": 65.0,
        "sst": 28.2,
        "current_speed": 2.1,
        "current_dir": "NE",
        "hour": 6,
        "migration": "Northward",
        "species": "Yellowfin Tuna",
        "fate": "Kept"
    }
)

print(response.json())
```

### Using the Interactive Docs
Visit http://127.0.0.1:8000/docs and use the built-in "Try it out" feature.

## ⚠️ Error Handling

The API automatically validates inputs and returns clear error messages:

- **Invalid numeric range**: Returns 422 with details
- **Missing required field**: Returns 422 with field name
- **Invalid categorical value**: Defaults to first encoder class (graceful degradation)

## 🔄 Model Retraining

The model trains automatically when the server starts. To retrain with new data:

1. Update `bycatch_dataset.xlsx`
2. Restart the server: `uvicorn main:app --reload`

For continuous operation, consider implementing:
- Periodic retraining schedules
- Model versioning
- A/B testing between model versions

## 📈 Performance Considerations

- **Startup time**: ~2-5 seconds (model training)
- **Prediction latency**: <10ms per request
- **Concurrent requests**: FastAPI handles async requests efficiently
- **Memory usage**: Model + encoders ~10-50 MB depending on data size

## 🚧 Production Deployment

For production use, consider:

1. **Use a production server**:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Environment variables** for configuration:
   ```python
   import os
   DATA_PATH = os.getenv("DATA_PATH", "bycatch_dataset.xlsx")
   ```

3. **Logging** for monitoring:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

4. **HTTPS** with reverse proxy (nginx/Apache)

5. **Rate limiting** to prevent abuse

6. **Model persistence** (save to disk, load on startup)

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contribution guidelines here]

## 📧 Contact

[Add contact information here]

---

**Note**: This is a demonstration/educational project. For real-world marine conservation applications, consult with marine biologists and validate the model with domain experts.
