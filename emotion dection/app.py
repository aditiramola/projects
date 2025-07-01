import pandas as pd
data=pd.read_csv(r"C:\Users\ramol\emotion_dataset.csv")
data['text']
data.isnull()
data.isnull().sum()
df=data.dropna()
df.to_csv('emotion_preprocessed_dataset.csv', index=False)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import accuracy_score, classification_report

df = pd.read_csv('emotion_preprocessed_dataset.csv')

texts = df['text']
labels = df['Emotion'] 

tfidf = TfidfVectorizer(min_df=500, max_df=0.8, ngram_range=(1, 2))

# Fit and transform the text data to get the TF-IDF feature matrix
features = tfidf.fit_transform(texts)

# Apply Truncated SVD to reduce the dimensionality of the feature matrix
svd = TruncatedSVD(n_components=20)  
normalizer = Normalizer(copy=False)
lsa = make_pipeline(svd, normalizer)

# Fit and transform the features with the pipeline
reduced_features = lsa.fit_transform(features)

# Convert the reduced feature matrix to a DataFrame
df_reduced = pd.DataFrame(reduced_features)

# Display the first few rows of the reduced features DataFrame
print(df_reduced.head())

X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

model = CatBoostClassifier(
    iterations=80, 
    learning_rate=0.1,
    depth=5,
    loss_function='MultiClass',
    eval_metric='Accuracy',
    early_stopping_rounds=50,  
    
)

# Train the model
model.fit(X_train, y_train, eval_set=(X_test, y_test), plot=True)
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")
result=classification_report(y_test, y_pred,zero_division=0)
print(result)

def predict_emotion(text_input):
    # Transform user input using the same TF-IDF vectorizer
    text_features = tfidf.transform([text_input])

    # Predict the emotion using the loaded model
    emotion_prediction = model.predict(text_features)
    
    # Output the result
    print(f"Predicted Emotion: {emotion_prediction[0]}")

# Prompt user for the number of sentences
n = int(input("Enter number of sentences: ")) 
# Loop to get input and make predictions
for i in range(n):
    user_input = input("Please enter sentence to predict the emotion: ")
    predict_emotion(user_input)
