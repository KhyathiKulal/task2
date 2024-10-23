import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load datasets
def load_data():
    courses = pd.read_csv('courses.csv')
    users = pd.read_csv('users.csv')
    return courses, users

def preprocess_data(courses):
    courses['skills'] = courses['skills'].apply(lambda x: ','.join([skill.lower().strip() for skill in x.split(',')]))
    return courses

def vectorize_skills(courses):
    vectorizer = TfidfVectorizer(tokenizer=lambda x: x.split(','))
    course_vectors = vectorizer.fit_transform(courses['skills'])
    return course_vectors, vectorizer

if __name__ == "__main__":
    courses, users = load_data()
    courses = preprocess_data(courses)
    course_vectors, vectorizer = vectorize_skills(courses)
    print(course_vectors.shape)
