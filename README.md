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
**Gradient Boosting Classifier** - An ensemble method that builds multiple decision trees sequentially, with each tree correcting errors from previous ones. An efficient and fast algorithm that provides high accuracy as opposed to some more complex algorithms that have a boot time greater than what is allowed for the Render free plan.

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

## Inspiration

Sea turtles and dolphins are really cute. Thousands of them are also needlessly killed every day.

Commercial fishermen often end up catching marine animals they didn't intend to catch, such as sea turtles, dolphins, seals, sharks, and juvenile fish, discarding them after catching them. This is  **bycatch**. A prominent issue, bycatch, threatens endangered species and destroys marine ecosystems. Currently, there are organizations that are helping fisheries manage unwanted catch, but our machine learning approach assesses risk levels of bycatch for anyone with just a click of a button.

## Challenges we ran into

Finding a real-world dataset with the combination of features we needed was genuinely difficult. Most publicly available bycatch datasets are either poorly formatted, heavily aggregated, or restricted to categorical variables that cannot support numerical model training. We simulated our training data from known IOTC catch patterns, which gave us clean numerical inputs but introduced overfitting risk, since validation was performed on data drawn from the same distribution. We were deliberate about acknowledging this limitation and structured the model to be straightforwardly retrained once real observational data becomes available.

## Accomplishments we are proud of

Within a single day, we built a functioning end-to-end system: a trained machine learning model, a REST API backend, and an interactive frontend, all connected and deployed to the web. The fact that a fisherman can open a browser, enter their fishing conditions, and receive a data-driven risk assessment in under a second felt like a genuine proof of concept for what accessible, practical environmental intelligence could look like in the real world.

## What we learned

We learned how to architect a full-stack machine learning application from scratch, covering data simulation, model training, API design with FastAPI, frontend integration, and cloud deployment on Render. We also developed a clearer understanding of the real-world constraints around environmental datasets and why domain-specific data collection is often the hardest part of any conservation-focused machine learning project. Working under time pressure using GitHub reinforced the value of clean separation between system components so teammates could build in parallel without blocking each other.

