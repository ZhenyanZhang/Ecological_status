import joblib
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import os

# loading data
train_df = pd.read_csv('RANDOM_sampled_dataset.csv')
test_df = pd.read_csv('remaining_dataset.csv')

# pre-
X_train = train_df.iloc[:, :25]
y_train = train_df.iloc[:, 25]
print(y_train)
X_test = test_df.iloc[:, :25]
y_test = test_df.iloc[:, 25]

# Converting string labels to integer
encoder = LabelEncoder()
y_train = encoder.fit_transform(y_train)
joblib.dump(encoder, 'label_encoder.pkl')  # 保存到磁盘
y_test = encoder.transform(y_test)

# hyperparameter tuning
models = {
    'RandomForestClassifier': (RandomForestClassifier(), {
        'n_estimators': [10, 50, 100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10]
    }),
    'SVC': (SVC(), {
        'C': [0.1, 1, 10],
        'kernel': ['linear', 'rbf'],
        'gamma': ['scale', 'auto', 0.01, 0.1]
    }),
    'LogisticRegression': (LogisticRegression(), {
        'C': [0.1, 1, 10, 100]
    }),
    'XGBClassifier': (XGBClassifier(), {
        'n_estimators': [10, 50, 100, 200],
        'max_depth': [3, 6, 9, 12],
        'learning_rate': [0.01, 0.1, 0.2, 0.3]
    })
}

results_best = []
output_folder = 'models'

# 使用ExcelWriter保存结果到Excel
with pd.ExcelWriter('model_performance.xlsx') as writer:
    for model_name, (model, params) in models.items():
        clf = GridSearchCV(model, params, cv=10, scoring='accuracy', n_jobs=-1,verbose=2)
        clf.fit(X_train, y_train)

        #results saving
        results_df = pd.DataFrame(clf.cv_results_)
        important_columns = [col for col in results_df.columns if 'param_' in col or col in ['mean_test_score']]
        results_df = results_df[important_columns]
        results_df.columns = [col.replace('param_', '') for col in results_df.columns]
        results_df.rename(columns={'mean_test_score': 'Accuracy'}, inplace=True)
        results_df.to_excel(writer, sheet_name=model_name, index=False)

        #evaluation for the best model under each algorithm with test dataset
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        best_params = clf.best_params_
        best_params['Accuracy'] = acc
        best_params['Model'] = model_name
        print(best_params)
        results_best.append(best_params)

        #best model saving
        best_model_path = os.path.join(output_folder, f'{model_name}_best_model.pkl')
        pd.to_pickle(clf.best_estimator_, best_model_path)

# results saving
results_best = pd.DataFrame(results_best)
results_best.to_csv('BEST_model_performance_ON_TEST.csv', index=False)

