import xgboost as xgb
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import numpy as np

# loading model
model = joblib.load('XGBClassifier_best_model.pkl')

# calculated the importance of environmental variables
feature_importances = model.feature_importances_
features = model.get_booster().feature_names #for xgboost

importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': feature_importances
}).sort_values(by='Importance', ascending=False)

print(importance_df)

# visualization
plt.figure(figsize=(10, 8))
plt.barh(np.arange(len(features)), importance_df['Importance'][::-1], align='center')
plt.yticks(np.arange(len(features)), importance_df['Feature'][::-1])
plt.xlabel('Relative Importance')
#plt.title('Feature Importance')
plt.show()
