import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder

# loading data
new_data = pd.read_excel('ssp585_2100.xlsx')

#pre-
new_data_for_prediction = new_data.iloc[:, 3:]


# loading model
model = joblib.load('XGBClassifier_best_model.pkl')

# rediction
predictions = model.predict(new_data_for_prediction)


# loading LabelEncoder
encoder = joblib.load('label_encoder.pkl')  # 确保这是训练时使用的同一个LabelEncoder
predictions_labels = encoder.inverse_transform(predictions)

#resuls saving
new_data['Predictions'] = predictions_labels
new_data.to_csv('ssp585_2100_predictions_results.csv', index=False)
