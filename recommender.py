import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


books = pd.read_csv("data/books.csv")
books['combined_features'] = books['title'].fillna('') + ' ' + books['authors'].fillna('')


tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(books['combined_features'])


cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


title_to_index = pd.Series(books.index, index=books['title'].str.strip().str.lower()).drop_duplicates()


tags = pd.read_csv("data/tags.csv")
book_tags = pd.read_csv("data/book_tags.csv")
book_tags_merged = book_tags.merge(tags, on='tag_id')
book_tags_merged['tag_name'] = book_tags_merged['tag_name'].str.lower()
book_genres = book_tags_merged.groupby('goodreads_book_id')['tag_name'].apply(set).reset_index()
book_id_to_tags = dict(zip(book_genres['goodreads_book_id'], book_genres['tag_name']))
books['genres'] = books['book_id'].map(book_id_to_tags)
books['genres'] = books['genres'].apply(lambda x: x if isinstance(x, set) else set())


def get_recommendations(book_title, top_n=5, min_rating=3.5, genre_filter=None):
    book_title = book_title.strip().lower()
    if book_title not in title_to_index:
        return []

    idx = title_to_index[book_title]
    input_book = books.iloc[idx]
    input_genres = input_book['genres']

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    recommendations = []
    for i, score in sim_scores[1:]:
        book = books.iloc[i]
        if book['average_rating'] < min_rating:
            continue
        if genre_filter and genre_filter.lower() not in book['genres']:
            continue

        overlap = input_genres.intersection(book['genres'])
        reason = f"shared genre: {', '.join(overlap)}" if overlap else f"similar themes as '{input_book['title']}'"

        recommendations.append({
            'title': book['title'],
            'author': book['authors'],
            'rating': book['average_rating'],
            'reason': reason
        })

        if len(recommendations) >= top_n:
            break

    return recommendations


def get_all_genres():
    all_genres = set()
    for gset in books['genres']:
        all_genres.update(gset)
    return sorted(all_genres)
