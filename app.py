import streamlit as st
import pickle
import numpy as np
import pandas as pd
popular_df = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    data = []
    for i in similar_items:
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        temp_df = temp_df.drop_duplicates('Book-Title')

        data.append([
            temp_df['Book-Title'].values[0],
            temp_df['Book-Author'].values[0],
            temp_df['Image-URL-M'].values[0]
        ])
    return data
st.set_page_config(page_title="Book Recommender", layout="wide")

st.title("📚 Book Recommender System")
st.markdown("### Popular books & Personalized recommendations")
st.subheader("🔥 Popular Books")

cols = st.columns(5)
for idx, col in enumerate(cols):
    with col:
        st.image(popular_df.iloc[idx]['Image-URL-M'])
        st.text(popular_df.iloc[idx]['Book-Title'][:30])
        st.caption(popular_df.iloc[idx]['Book-Author'])

st.divider()
st.subheader("🎯 Recommend Similar Books")

selected_book = st.selectbox(
    "Choose a book",
    pt.index
)

if st.button("Recommend"):
    recommendations = recommend(selected_book)

    cols = st.columns(5)
    for col, rec in zip(cols, recommendations):
        with col:
            st.image(rec[2])
            st.text(rec[0][:30])
            st.caption(rec[1])
