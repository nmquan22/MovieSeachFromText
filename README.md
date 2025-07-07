# Movie Recommendation System using TF-IDF & Streamlit

A simple content-based movie recommendation system that leverages **TF-IDF vectorization** and **cosine similarity** to match user queries with relevant movie overviews. Built with `scikit-learn`, `nltk`, and `Streamlit` for the frontend interface.

---

## Project Structure

```text
├── Data/                 # Folder containing movie data (JSON format)
├── Images/               # Folder for UI demo screenshots
├── index.py              # Script to generate inverted TF-IDF index
├── query.py              # Cosine similarity search logic
├── mainPage.py           # Streamlit frontend UI
├── preprocess.py         # Tokenization, stemming, and stopword removal
├── indexUpdate.json      # Generated index after vectorization
├── style.css             # Custom styling for Streamlit UI
```

---

## How to Run

### 1. Preprocess the Data
```bash
python preprocess.py
```
This will create the `Data/` folder with preprocessed movie overviews.

### 2. Generate TF-IDF Index
```bash
python index.py
```
This creates the file `indexUpdate.json` used for fast retrieval.

### 3. Launch the Web App
```bash
streamlit run mainPage.py
```
This will open a browser tab with your interactive movie recommender.

---

## Features

- Full-text search over movie overviews
- Tokenization, stemming, and stopword removal
- Cosine similarity ranking for most relevant results
- Sidebar filters: genre selection and rating sort
- Simple and clean UI built with Streamlit

---

## Demo

![image](Images/demo.png)

---

## Technologies Used

- Python 3.x
- scikit-learn
- nltk
- streamlit
- numpy
- JSON data handling

---

## Future Improvements

- Use embedding models like SBERT for better semantic matching
- Implement autocomplete or fuzzy search
- Add pagination and advanced filtering

---

## License
This project is for educational and demonstration purposes.
