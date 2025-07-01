import streamlit as st
from recommender import get_recommendations, get_all_genres

st.set_page_config(page_title="📚 Book Recommender", layout="centered")

st.title("📚 Smart Book Recommender")
st.markdown("Enter a book you like, and get intelligent, filtered suggestions!")

# Input: book name
book_input = st.text_input("🔍 Enter a book title", "")

# Input: rating filter
min_rating = st.slider("⭐ Minimum Average Rating", 1.0, 5.0, 3.5, step=0.1)

# Input: genre dropdown
genre_options = ["All"] + get_all_genres()
selected_genre = st.selectbox("🎭 Filter by Genre", genre_options)
genre_filter = None if selected_genre == "All" else selected_genre

# Show recommendations
if book_input:
    with st.spinner("🔎 Finding recommendations..."):
        recommendations = get_recommendations(book_input, min_rating=min_rating, genre_filter=genre_filter)

    if recommendations:
        st.subheader("✨ You may like:")
        for book in recommendations:
            st.markdown(f"""
                **📖 {book['title']}**  
                👤 {book['author']}  
                ⭐ {book['rating']}/5  
                💡 _Recommended because of {book['reason']}_
            """)
            st.markdown("---")
    else:
        st.warning("❌ Book not found or no results with current filters.")
