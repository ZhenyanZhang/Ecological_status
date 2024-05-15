import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc, confusion_matrix
from sklearn.preprocessing import label_binarize
from itertools import cycle

# loading data
test_df = pd.read_csv('RANDOM2_remaining_dataset.csv')
X_test = test_df.iloc[:, :10]
y_test = test_df.iloc[:, 10]

# loading LabelEncoder
encoder = joblib.load('label_encoder.pkl')
y_test = encoder.transform(y_test)

# loading model
model = joblib.load('XGBClassifier_best_model.pkl')

# prediction with the model for test dataset
y_pred = model.predict(X_test)

# calculation for confusion matrix
cm = confusion_matrix(y_test, y_pred)
cm_percentage = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

plt.figure(figsize=(8, 6))
plt.imshow(cm_percentage, interpolation='nearest', cmap=plt.cm.Blues)
#plt.title('Confusion Matrix in Percentage')
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=90)
plt.yticks(tick_marks, classes)

plt.tight_layout()
plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.savefig('confusion_matrix_percentage.pdf', format='pdf')
plt.show()
