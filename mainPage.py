import streamlit as st
import requests
import json
from query import search
with open('./style.css') as f:
    css = f.read()
    print("CSS")

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
def fetchProducts(query):
    with open("indexUpdate.json", "r", encoding="utf-8") as file:
        index = json.load(file)
    vocabulary = list(index.keys())
    products = []
    query = query.split()
    for token in query.items():
        if token in vocabulary:
            products.append(token)
    return products

with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    
    # Title
    st.markdown("<div class='sidebar-title'>Categories</div>", unsafe_allow_html=True)
    categories = ["Popular", "Top Rated", "Upcoming"]
    for category in categories:
        st.markdown(f"<div class='sidebar-item'>{category}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Genres
    st.markdown("<div class='sidebar-title'>Genres</div>", unsafe_allow_html=True)
    genres = ["All"] + ["Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Fantasy"]
    selected_genre = st.selectbox("Filter by Genre", genres, index=0)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Sort by Rating
    st.markdown("<div class='sidebar-title'>Sort by Rating</div>", unsafe_allow_html=True)
    sort_order = st.radio("Sort Order", ["Normal","Highest First", "Lowest First"], index=0)
    
    st.markdown("</div>", unsafe_allow_html=True)


st.title("Movie Recommandation")
query = st.text_input("Search for movie")
print(query)
if query:
    products = []
    result_files = []
    results = search(query)
    if results:
        for rank, (doc_id, score) in enumerate(results, start=1):
            print(f"{rank}. Document: {doc_id}, Similarity Score: {score:.4f}")
            result_files.append(doc_id)
    else:
        st.markdown("Your search did not match any documents.")
    for file_name in result_files:
        try:
            file_name = "./Data/" + file_name
            with open(file_name, "r", encoding="utf-8") as json_file:
                product_data = json.load(json_file)
                # Append the product data from the file to the products list
                products.append({
                    "title": product_data.get("Series_Title", "No Title"),
                    "images": product_data.get("Poster_Link","https://via.placeholder.com/150"),
                    "category": product_data.get("Overview", "Unknown"),
                    "imdb":product_data.get("IMDB_Rating",0),
                    "genre": product_data.get("Genre","None"),
                    "auther": product_data.get("Director","None")
                })
        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON in file: {file_name}")

    # Filter by Genre
    if selected_genre != "All":
        products = [movie for movie in products if selected_genre.lower() in movie["genre"].lower()]
    
    # Sort by Rating
    if sort_order != "Normal":
        reverse_order = True if sort_order == "Highest First" else False
        products = sorted(products, key=lambda x: x["imdb"], reverse=reverse_order)

    columns_per_row = 3
    for row_start in range(0, len(products), columns_per_row):
        cols = st.columns(columns_per_row)
        for col, item in zip(cols, products[row_start:row_start + columns_per_row]):
            with col:
                st.subheader(item["title"])
                image_url = "https://via.placeholder.com/150"
                st.markdown(f"""
                    <div class="card">
                        <img src={item['images']} alt="Avatar" style="width:100%">
                        <div class="container">
                            <h4><b>IMDB_rating:{item['imdb']}</b></h4>
                            <p>{item['category']}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)