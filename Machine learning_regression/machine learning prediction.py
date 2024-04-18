import pandas as pd
from joblib import load

# loading data
new_data = pd.read_excel('data_2023.xlsx')

with open('model_paths.txt', 'r') as file:
    target_identifiers = [line.strip() for line in file.readlines()]

predictions = pd.DataFrame(new_data.iloc[:, :13])

# prediction for each microbial indices
for identifier in target_identifiers:
    print(identifier)
    model_path = f'models/{identifier}_Random_Forest_best_model.pkl'
    model = load(model_path)  # loading models
    X_new = new_data.iloc[:, 3:13]
    print(X_new)
    predictions[identifier] = model.predict(X_new)
    print(predictions)

# saving results
predictions.to_csv('predictions_2023_RF.csv', index=False)
