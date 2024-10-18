import streamlit as st
import re
import pyperclip

st.set_page_config(page_title="Tokenization, Stemming, and Stopword Removal", page_icon="📒", layout="centered")
st.title("Tokenization, Stemming, and Stopword Removal")

tokens = []
st.subheader("Raw Text")
raw_text = st.text_area("Enter raw text here:")

def tokenize(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    tokens = text.split()
    return tokens

if st.button("Apply Text"):
    tokens = tokenize(raw_text)

# Info box for tokenization results
st.subheader("Tokenization")
with st.expander("Tokenization Steps"):
    st.write("1. Remove non-alphabetic characters")
    st.write("2. Convert text to lowercase")
    st.write("3. Split text into tokens")
with st.expander("Tokenization Result"):
    for token in tokens:
        st.text(token)

# Text box for stopwords input
st.subheader("Stopword Removal")
if "default_stopwords" not in st.session_state:
    st.session_state.default_stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

if "stopwords_text" not in st.session_state:
    st.session_state.stopwords_text = ' '.join(st.session_state.default_stopwords)

stopwords_text = st.text_area("Enter stopwords here (separated by spaces):", value=st.session_state.stopwords_text)
if st.button("Apply Stopwords"):
    st.session_state.stopwords_text = stopwords_text
    stopwords = stopwords_text.split()
    stopwords = [w for w in stopwords if w]

stopwords = st.session_state.stopwords_text.split()
stopwords = [w for w in stopwords if w]
with st.expander("Stopwords"):
    for stopword in stopwords:
        st.text(stopword)
    stopwords_str = ' '.join(stopwords)
    if st.button("Copy"):
        pyperclip.copy(stopwords_str)

with st.expander("Stopword Removal Result"):
    filtered_tokens = [token for token in tokenize(raw_text) if token not in stopwords]
    for token in filtered_tokens:
        st.text(token)

# Text box for stemmer input
from porterStemmer import porter_stemmer
if (raw_text):
    st.subheader("Stemming")
    with st.expander("Stemming Result"):
        stemmed_tokens = [porter_stemmer(token) for token in filtered_tokens]
        for token in stemmed_tokens:
            st.text(token)
