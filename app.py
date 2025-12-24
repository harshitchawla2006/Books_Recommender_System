import streamlit as st
import pickle
import numpy as np
import pandas as pd
st.set_page_config(
    page_title="Book Recommender",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>

/* FORCE DARK BACKGROUND */
html, body, [class*="css"] {
    background-color: #020617 !important;
    color: #e5e7eb !important;
}

/* MAIN APP */
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a, #020617) !important;
}

/* TITLE */
h1 {
    text-align: center;
    font-weight: 800;
    color: #38bdf8 !important;
}

/* HEADINGS */
h2, h3 {
    color: #e5e7eb !important;
}

/* BOOK CARD */
.book-card {
    background: linear-gradient(145deg, #111827, #1f2937);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 12px 30px rgba(56,189,248,0.25);
    transition: all 0.35s ease;
    text-align: center;
}

/* HOVER EFFECT */
.book-card:hover {
    transform: scale(1.06);
    box-shadow: 0 20px 50px rgba(56,189,248,0.45);
}

/* BOOK IMAGE */
.book-card img {
    border-radius: 14px;
    margin-bottom: 12px;
}

/* BOOK TITLE */
.book-title {
    font-size: 15px;
    font-weight: 600;
    color: #f9fafb;
}

/* AUTHOR */
.book-author {
    font-size: 13px;
    color: #9ca3af;
}

/* SELECTBOX */
div[data-baseweb="select"] {
    background-color: #020617 !important;
    border-radius: 10px;
}

/* BUTTON */
button {
    background: linear-gradient(90deg, #38bdf8, #6366f1) !important;
    color: black !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    padding: 10px 26px !important;
    transition: 0.3s ease !important;
}

button:hover {
    transform: scale(1.07);
    box-shadow: 0 10px 30px rgba(99,102,241,0.6);
}

</style>
""", unsafe_allow_html=True)
st.markdown("<div></div>", unsafe_allow_html=True)


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

st.title("📚 Book Recommender System")
st.markdown("### Discover popular books & get smart recommendations")
st.subheader("🔥 Popular Books")

cols = st.columns(5)
for idx, col in enumerate(cols):
    with col:
        st.markdown(f"""
        <div class="book-card">
            <img src="{popular_df.iloc[idx]['Image-URL-M']}" width="100%">
            <div class="book-title">
                {popular_df.iloc[idx]['Book-Title'][:30]}
            </div>
            <div class="book-author">
                {popular_df.iloc[idx]['Book-Author']}
            </div>
        </div>
        """, unsafe_allow_html=True)
st.divider()
st.subheader("🎯 Recommend Similar Books")

selected_book = st.selectbox(
    "📖 Select a book you like",
    pt.index
)

if st.button("✨ Recommend"):
    with st.spinner("Finding books for you..."):
        recommendations = recommend(selected_book)

    cols = st.columns(5)
    for col, rec in zip(cols, recommendations):
        with col:
            st.markdown(f"""
            <div class="book-card">
                <img src="{rec[2]}" width="100%">
                <div class="book-title">
                    {rec[0][:30]}
                </div>
                <div class="book-author">
                    {rec[1]}
                </div>
            </div>
            """, unsafe_allow_html=True)
