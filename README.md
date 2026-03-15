# DeepWatch - Bycatch Risk Prediction
## [DeepWatch Link](https://deepwatch.onrender.com)


## Overview

This tool uses a Gradient Boosting Classifier to predict bycatch probability based on:
- Geographic location (latitude/longitude)
- Environmental conditions (sea surface temperature, ocean currents)
- Temporal factors (time of day)
- Fishing operation details (target species, migration patterns, species fate)

## Machine Learning Model
### Data
**Simulated Data** - Due to limitations of features within open-source datasets, a dataset was simulated with slight noise to train a model for future use in actual datasets.

#### Features Used (9 total)
1. Latitude
2. Longitude
3. Sea Surface Temperature
4. Current Speed
5. Current Direction (encoded)
6. Hour of Day
7. Migration Pattern (encoded)
8. Target Species (encoded)
9. Species Fate (encoded)

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

### Risk Classification
- **High Risk**: Probability ≥ 65%
- **Low Risk**: Probability < 65%

## Tech Stack
### All hosted on Render

### Backend
**FastAPI Backend**
- Getting values from input fields in the frontend
- Applying the machine learning algorithm to get the probability
- Providing this output to the frontend

### Frontend
**Simple HTML/CSS/JS frontend**
- Landing page with information about the DepepWatch initiative
- Risk Predictor page with all input fields and submission field. Outputs percentage on bars and metrics from the model.
