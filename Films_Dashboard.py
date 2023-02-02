import streamlit as st  # web development
import numpy as np  # np.mean, np.random
import pandas as pd  # read csv, df manipulation
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
import matplotlib.pyplot as plt

st.set_page_config(page_title='Films Dashboard', page_icon='🎥', layout='wide')


@st.cache
def load_data():
    df = pd.read_csv(r"C:\Users\SOS2023\OneDrive\Desktop\NetflixOriginals.csv")
    y = df['year'].unique()
    g = df['Genre1'].unique()
    l = df['Language'].unique()
    return df, g, y, l


df, genre, year, languages = load_data()

with st.sidebar:
    annee_choisie = st.selectbox(label="Choisissez une année :", options=year)
    any_year = st.checkbox(label='Any year')

    language_choisi = st.selectbox(label="Choisissez une langue", options=languages)
    genre_choisi = st.selectbox(label="Choisissez ce que vous plait", options=genre)
# -- Apply the year filter given by the user
if any_year:
    filtered_df = df[(df['Genre1'] == genre_choisi)]
else:
    filtered_df = df[(df['year'] == annee_choisie) | (df['Genre1'] == genre_choisi)]
# -- Apply the continent filter
filtered_df = filtered_df[filtered_df['Language'] == language_choisi]


def top_rank():
    top_film = filtered_df[filtered_df['IMDB Score'] == filtered_df['IMDB Score'].max()]
    return top_film


st.metric("Top Ranked Film", str(filtered_df['Title'][0:1]), float(filtered_df['IMDB Score'][0:1]))

col2, col3 = st.columns(2)
col2.metric("Gender", genre_choisi, "📃")
col3.metric("Runtime", filtered_df['Runtime'][0:1])

# dashboard title
st.title("Top Netflix Originals Films Dashboard")
filtered_df.shape

# -- Apply the year filter given by the user
if any_year:
    filtered_df = df[(df['Language'] == language_choisi) | (df['Genre1'] == genre_choisi)]
else:
    filtered_df = df[(df['year'] == annee_choisie) | (df['Genre1'] == genre_choisi)]
# -- Apply the continent filter
filtered_df = filtered_df[filtered_df['Language'] == language_choisi]

fig_bars = px.bar(filtered_df, x='IMDB Score', y='Title', orientation='h')
st.write(fig_bars)
tab1, tab2, tab3 = st.tabs(["Films by Score", "Films", "Gender distribution"])

with tab1:
    st.bar_chart(data=filtered_df, x='Title', y='IMDB Score', use_container_width=True)

with tab2:
    genre_dist = df.groupby(by=["Genre1"]).count()

    pie_fig = genre_dist.plot(kind="pie", subplots=True,
                            title="Distribution by gender",)

with tab3:
    fig1, ax1 = plt.subplots()
    ax1 = filtered_df['Genre1'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
    st.pyplot(fig1)
    plt.legend()