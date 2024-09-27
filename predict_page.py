import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We'd love to assist you in predicting your salary! Please share the following details with us: """)

    countries = ("United States of America","Germany","Ukraine","United Kingdom of Great Britain and Northern Ireland","India","France","Canada","Brazil","Spain","Italy","Australia","Poland","Netherlands","Sweden")
    education = ("Bachelor's degree",
                "Master's degree",
                "Less than Bachelors"
                "Professional degree"
                "Associate degree")

    country = st.selectbox("Country",countries)
    education = st.selectbox("Education Level",education)
    experience = st.slider("Years of Experience", 0,55, 1)

    ok = st.button("Predict the Salary")
    if ok:
        x = np.array([[country, education, experience]])
        x[:,0] = le_country.transform(x[:,0])
        x[:,1] = le_education.transform(x[:,1])
        x = x.astype(float)

        salary = regressor.predict(x)
        st.subheader(f"The estimated Salary is ${salary[0]:.2f}")