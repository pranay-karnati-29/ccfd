import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb

# Load your dataset
df = pd.read_csv('dataset/creditcard_2023.csv')
X = df.drop('Class', axis=1)
y = df['Class']

# Logistic Regression
# logreg_model = LogisticRegression(max_iter=1000, class_weight='balanced')
# logreg_model.fit(X, y)
# with open('ml model/logreg_model.pkl', 'wb') as f:
#     pickle.dump(logreg_model, f)

# SVM
# svm_model = SVC(probability=True)
# svm_model.fit(X, y)
# with open('ml model/svm_model.pkl', 'wb') as f:
#     pickle.dump(svm_model, f)

# KNN
# knn_model = KNeighborsClassifier(n_neighbors=5)
# knn_model.fit(X, y)
# with open('ml model/knn_model.pkl', 'wb') as f:
#     pickle.dump(knn_model, f)

# Random Forest
# rf_model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
# rf_model.fit(X, y)
# with open('ml model/rf_model.pkl', 'wb') as f:
#     pickle.dump(rf_model, f)

# Decision Tree
# dt_model = DecisionTreeClassifier(class_weight='balanced', random_state=42)
# dt_model.fit(X, y)
# with open('ml model/dt_model.pkl', 'wb') as f:
#     pickle.dump(dt_model, f)

# Gradient Boosting
# gb_model = GradientBoostingClassifier(n_estimators=100, random_state=42)
# gb_model.fit(X, y)
# with open('ml model/gb_model.pkl', 'wb') as f:
#     pickle.dump(gb_model, f)

# AdaBoost
# adaboost_model = AdaBoostClassifier()
# adaboost_model.fit(X, y)
# with open('ml model/adaboost_model.pkl', 'wb') as f:
#     pickle.dump(adaboost_model, f)

# XGBoost
# xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
# xgb_model.fit(X, y)
# with open('ml model/xgb_model.pkl', 'wb') as f:
#     pickle.dump(xgb_model, f)


# XGBoost - Save as JSON
# xgb_model = xgb.XGBClassifier(use_label_encoder=False, eval_metric='logloss')
# xgb_model.fit(X, y)
# xgb_model.save_model('ml model/xgb_model.json')

print("All models have been trained and saved in the 'ml model' directory.")