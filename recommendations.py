import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

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

courses, users = load_data()
courses = preprocess_data(courses)
course_vectors, vectorizer = vectorize_skills(courses)

def recommend_courses(user_skills, top_n=5):
    user_skills = ','.join([skill.lower().strip() for skill in user_skills.split(',')])
    user_vector = vectorizer.transform([user_skills])
    
    similarities = cosine_similarity(user_vector, course_vectors).flatten()
    
    recommended_indices = similarities.argsort()[-top_n:][::-1]
    recommended_courses = courses.iloc[recommended_indices]
    return recommended_courses[['course_title', 'platform']]
