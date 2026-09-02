from flask import Flask, request, jsonify, render_template, send_from_directory
import numpy as np
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score
import xgboost as xgb
from sklearn.ensemble import AdaBoostClassifier  # Add this import
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

app = Flask(__name__)

# Load models
with open('ml model/logreg_model.pkl', 'rb') as f:
    logreg_model = pickle.load(f)
with open('ml model/svm_model.pkl', 'rb') as f:
    svm_model = pickle.load(f)
with open('ml model/knn_model.pkl', 'rb') as f:
    knn_model = pickle.load(f)
with open('ml model/rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)
with open('ml model/dt_model.pkl', 'rb') as f:
    dt_model = pickle.load(f)
with open('ml model/gb_model.pkl', 'rb') as f:
    gb_model = pickle.load(f)
xgb_model = xgb.XGBClassifier()
xgb_model.load_model('ml model/xgb_model.json')
with open('ml model/adaboost_model.pkl', 'rb') as f:  # Add this line
    adaboost_model = pickle.load(f)


# Load your dataset
df = pd.read_csv('dataset/test-2.csv')
X = df.drop('Class', axis=1)
y = df['Class']

# Calculate accuracy for each model using the entire dataset
model_accuracies = {
    'logreg': accuracy_score(y, logreg_model.predict(X)),
    'svm': accuracy_score(y, svm_model.predict(X)),
    'knn': accuracy_score(y, knn_model.predict(X)),
    'rf': accuracy_score(y, rf_model.predict(X)),
    'dt': accuracy_score(y, dt_model.predict(X)),
    'gb': accuracy_score(y, gb_model.predict(X)),
    'xgb': accuracy_score(y, xgb_model.predict(X)),
    'adaboost': accuracy_score(y, adaboost_model.predict(X)),
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/visualizations.html')
def visualizations():
    return render_template('visualizations.html')

@app.route('/analysis.html')
def analysis():
    return render_template('analysis.html')

@app.route('/amount-trends.html')
def amount_trends():
    return render_template('amount-trends.html')

@app.route('/feature.html')
def feature():
    return render_template('feature.html')

@app.route('/theory.html')
def theory():
    return render_template('theory.html')

@app.route('/model.html')
def model():
    return render_template('model.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    features_df = prepare_features(features)  # Add this line
    model_name = data.get('model', 'logreg')
    
    # Convert to DataFrame with proper column names
    feature_names = ['id'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    features_df = pd.DataFrame(features, columns=feature_names)
    
    # Get model
    if model_name == 'svm':
        model = svm_model
    elif model_name == 'knn':
        model = knn_model
    elif model_name == 'rf':
        model = rf_model
    elif model_name == 'dt':
        model = dt_model
    elif model_name == 'gb':
        model = gb_model
    elif model_name == 'xgb':
        model = xgb_model
    elif model_name == 'adaboost':
        model = adaboost_model
    else:
        model = logreg_model

    # Use DataFrame for prediction
    pred = model.predict(features_df)[0]  # Use features_df instead of features
    if hasattr(model, "predict_proba"):
        prob = model.predict_proba(features_df)[0, 1]  # Use features_df
    else:
        prob = float(model.decision_function(features_df)[0])  # Use features_df
    
    acc = model_accuracies.get(model_name, model_accuracies['logreg'])
    return jsonify({'prediction': int(pred), 'probability': float(prob), 'accuracy': float(acc)})

@app.route('/predict_weighted', methods=['POST'])
def predict_weighted():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    model1_name = data.get('model1', 'rf')
    model2_name = data.get('model2', 'xgb')
    
    models = {
        'logreg': logreg_model, 'svm': svm_model, 'knn': knn_model,
        'rf': rf_model, 'dt': dt_model, 'gb': gb_model,
        'xgb': xgb_model, 'adaboost': adaboost_model
    }
    
    model1 = models.get(model1_name, rf_model)
    model2 = models.get(model2_name, xgb_model)
    
    # Get accuracies as weights
    acc1 = model_accuracies.get(model1_name, 0.99)
    acc2 = model_accuracies.get(model2_name, 0.99)
    total_acc = acc1 + acc2
    weight1 = acc1 / total_acc
    weight2 = acc2 / total_acc
    
    # Get predictions
    prob1 = model1.predict_proba(features)[0, 1] if hasattr(model1, "predict_proba") else 0.5
    prob2 = model2.predict_proba(features)[0, 1] if hasattr(model2, "predict_proba") else 0.5
    
    # Weighted average
    weighted_prob = (prob1 * weight1) + (prob2 * weight2)
    weighted_pred = int(weighted_prob > 0.5)
    
    return jsonify({
        'weighted_prediction': weighted_pred,
        'weighted_probability': float(weighted_prob),
        'weights': {'model1': float(weight1), 'model2': float(weight2)},
        'individual_results': {
            'model1': {'probability': float(prob1), 'accuracy': float(acc1)},
            'model2': {'probability': float(prob2), 'accuracy': float(acc2)}
        }
    })

@app.route('/predict_sequential', methods=['POST'])
def predict_sequential():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    model1_name = data.get('model1', 'rf')
    model2_name = data.get('model2', 'xgb')
    threshold = data.get('threshold', 0.7)
    
    models = {
        'logreg': logreg_model, 'svm': svm_model, 'knn': knn_model,
        'rf': rf_model, 'dt': dt_model, 'gb': gb_model,
        'xgb': xgb_model, 'adaboost': adaboost_model
    }
    
    model1 = models.get(model1_name, rf_model)
    model2 = models.get(model2_name, xgb_model)
    
    # First model prediction
    prob1 = model1.predict_proba(features)[0, 1] if hasattr(model1, "predict_proba") else 0.5
    pred1 = int(prob1 > 0.5)
    
    # If first model is uncertain, use second model
    if prob1 < threshold and prob1 > (1 - threshold):
        prob2 = model2.predict_proba(features)[0, 1] if hasattr(model2, "predict_proba") else 0.5
        final_prob = prob2
        final_pred = int(prob2 > 0.5)
        model_used = model2_name
    else:
        final_prob = prob1
        final_pred = pred1
        model_used = model1_name
    
    return jsonify({
        'final_prediction': final_pred,
        'final_probability': float(final_prob),
        'model_used': model_used,
        'first_model_prob': float(prob1),
        'threshold': threshold
    })

@app.route('/predict_ensemble', methods=['POST'])
def predict_ensemble():
    data = request.json
    features = np.array(data['features']).reshape(1, -1)
    model1_name = data.get('model1', 'rf')
    model2_name = data.get('model2', 'xgb')
    
    # Convert to DataFrame with proper column names
    feature_names = ['id'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    features_df = pd.DataFrame(features, columns=feature_names)
    
    # Get models
    models = {
        'logreg': logreg_model, 'svm': svm_model, 'knn': knn_model,
        'rf': rf_model, 'dt': dt_model, 'gb': gb_model,
        'xgb': xgb_model, 'adaboost': adaboost_model
    }
    
    model1 = models.get(model1_name, rf_model)
    model2 = models.get(model2_name, xgb_model)
    
    # Get predictions from both models using DataFrame
    pred1 = model1.predict(features_df)[0]
    pred2 = model2.predict(features_df)[0]
    
    # Get probabilities using DataFrame
    prob1 = model1.predict_proba(features_df)[0, 1] if hasattr(model1, "predict_proba") else 0.5
    prob2 = model2.predict_proba(features_df)[0, 1] if hasattr(model2, "predict_proba") else 0.5
    
    # Ensemble methods
    voting_pred = int((pred1 + pred2) >= 1)  # Majority vote
    avg_prob = (prob1 + prob2) / 2  # Average probability
    max_prob = max(prob1, prob2)  # Maximum probability
    
    # Get accuracies
    acc1 = model_accuracies.get(model1_name, 0.99)
    acc2 = model_accuracies.get(model2_name, 0.99)
    avg_acc = (acc1 + acc2) / 2
    
    return jsonify({
        'ensemble_prediction': voting_pred,
        'average_probability': float(avg_prob),
        'max_probability': float(max_prob),
        'model1': {'prediction': int(pred1), 'probability': float(prob1), 'accuracy': float(acc1)},
        'model2': {'prediction': int(pred2), 'probability': float(prob2), 'accuracy': float(acc2)},
        'ensemble_accuracy': float(avg_acc)
    })

# Add route for service worker
@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

# Add route for manifest
@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

# Add route for offline page
@app.route('/offline.html')
def offline():
    return render_template('offline.html')

@app.route('/privacy-policy.html')
def privacy_policy():
    return render_template('privacy-policy.html')

@app.route('/terms-conditions.html')
def terms_conditions():
    return render_template('terms-conditions.html')

def prepare_features(features_array):
    """Convert numpy array to DataFrame with proper feature names"""
    feature_names = ['id'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
    return pd.DataFrame(features_array, columns=feature_names)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)


