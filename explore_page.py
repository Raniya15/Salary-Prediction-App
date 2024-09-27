import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def cleaned_cat(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else: 
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def clean_ed_level(ed_level):
    ed_level = ed_level.strip() 
    if "Bachelor" in ed_level:
        return "Bachelor's degree"
    elif "Master" in ed_level:
        return "Master's degree"
    elif "Professional" in ed_level:
        return "Professional degree"
    elif "Associate" in ed_level:
        return "Associate degree"
    else:
        return "Less than Bachelors"

@st.cache_data  #To prevent execution again and again
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[['Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedCompYearly']]
    df.rename(columns={'ConvertedCompYearly': 'Salary'}, inplace=True)
    df = df.dropna() 
    df = df[df['Employment'].str.contains('Employed, full-time')]
    country_map = cleaned_cat(df['Country'].value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary']<= 250000]
    df = df[df['Salary']>=10000]
    df = df[df['Country']!='Other']
    df['YearsCodePro'].replace('Less than 1 year', 0.5, inplace=True)
    df['EdLevel'] = df['EdLevel'].apply(clean_ed_level)
    df['YearsCodePro'] = pd.to_numeric(df['YearsCodePro'], errors='coerce')
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2024""")

    data = df['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']  # Custom color palette
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90, colors=colors, explode=[0.05]*len(data))
    ax1.set_title("Data Distribution by Countries", fontsize=14, weight='bold')  # Title for better clarity
    ax1.axis("equal")  # Equal aspect ratio ensures the pie is drawn as a circle
    st.pyplot(fig1)

    st.write("""### Average Salary based on Country""")
    data = df.groupby(['Country'])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("""### Average Salary based on Experience""")
    data = df.groupby(['YearsCodePro'])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)