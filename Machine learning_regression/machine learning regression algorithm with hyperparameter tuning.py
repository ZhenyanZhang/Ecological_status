import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from joblib import dump

# loading data
data = pd.read_csv('data_for_ML.csv')

# defining X and y
X = data.iloc[:, 1:11]
print(X)
y_columns = data.columns[11:]

# models and hyperparameter
models = {
    'XGBoost': XGBRegressor(),
    'Random Forest': RandomForestRegressor(),
    'Linear Regression': LinearRegression(),
    'Lasso': Lasso(),
    'K Nearest Neighbors': KNeighborsRegressor()
}

param_grids = {
    'XGBoost': {
        'xgboost__n_estimators': [100, 200, 300, 500,600],
        'xgboost__max_depth': [3, 5, 7,9],
        'xgboost__learning_rate': [0.01, 0.1, 0.2,0.3]
    },
    'Random Forest': {
        'randomforest__n_estimators': [100, 200, 300, 500,600],
        'randomforest__max_depth': [None, 10, 20,30,40],
        'randomforest__min_samples_split': [2, 5]
    },
    'Linear Regression': {},
    'Lasso': {
        'lasso__alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10],
        'lasso__max_iter': [5000, 10000, 15000,30000]
    },
    'K Nearest Neighbors': {
        'knearestneighbors__n_neighbors': [3, 5, 7, 10],
        'knearestneighbors__weights': ['uniform', 'distance'],
        'knearestneighbors__metric': ['euclidean', 'manhattan']
    }
}



results = []
all_results = []
model_save_path = 'models'
os.makedirs(model_save_path, exist_ok=True)

# model training
for y_column in y_columns:
    print(y_column)
    y = data[y_column]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    for model_name, model in models.items():
        pipeline = Pipeline([('scaler', StandardScaler()), (model_name.lower().replace(' ', ''), model)])
        grid_search = GridSearchCV(pipeline, param_grids[model_name], cv=10, scoring='r2', refit=True, n_jobs=-1)
        grid_search.fit(X_train, y_train)

        # results saving
        cv_results = pd.DataFrame(grid_search.cv_results_)
        cv_results['model_name'] = model_name
        cv_results['target_variable'] = y_column
        all_results.append(cv_results)

        #obtining the best combination of hyperparameter
        best_params = grid_search.best_params_

        #valuating with test dataset
        y_pred_test = grid_search.predict(X_test)
        r2_test = r2_score(y_test, y_pred_test)

        # valuating with overall dataset
        y_pred_overall = grid_search.predict(X)
        r2_overall = r2_score(y, y_pred_overall)

        # 保存最佳模型
        model_filename = f"{model_save_path}/{y_column}_{model_name.replace(' ', '_')}_best_model.pkl"
        dump(grid_search.best_estimator_, model_filename)

        # 存储结果
        results.append({
            'Target Variable': y_column,
            'Model': model_name,
            'Best Parameters': str(best_params),
            'R2_overall': r2_overall,
            'R2_test': r2_test,
        })

# saving in Excel
results_df = pd.DataFrame(results)
with pd.ExcelWriter('hyperparameter_tuning.xlsx') as writer:
    results_df.to_excel(writer, index=False)

