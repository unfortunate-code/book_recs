import streamlit as st
import pandas as pd
import requests

books = {
    "Comedy": [("The Hitchhiker's Guide to the Galaxy", "Douglas Adams"), ("Anxious People", "Fredrik Backman"), ("A dirty job", "Christopher Moore")],
    "Fantasy": [("The Name of the Wind", "Patrick Rothfuss"), ("Stardust", "Neil Gaiman")],
    "Thriller": [("Simply Lies", "David Baldacci"), ("Blindsighted", "Karin Slaughter")],
    "Non fiction": [("Sapiens", "Yuval Noah Harari"), ("Gut", "Giulia Enders")]
}

st.title("Find your next read!")

def get_book_data(title, author):
    api_key = "AIzaSyAWz2wr5tiLv6jFBt1L6Koit6sKDUhwJUs"
    query = f"{title}+inauthor:{author}"
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    description = data["items"][0]["volumeInfo"]["description"]
    pageCount = data["items"][0]["volumeInfo"]["pageCount"]
    thumbnail = data["items"][0]["volumeInfo"]["imageLinks"]["thumbnail"]
    return description, pageCount, thumbnail

# Category Selection
genre = st.selectbox("Choose your Genre:", ["", "Comedy", "Fantasy", "Thriller", "Non fiction"])

if genre != "":
    st.subheader(f"Some recommendations in {genre}")
    for title, author in books[genre]:
        st.write(f"<u><b>{title} by {author}</b></u>", unsafe_allow_html=True)
        description, pageCount, thumbnail = get_book_data(title, author)
        st.image(thumbnail)
        st.write(f"{description[:500]}...")
        st.write(f"Page Count: {pageCount}")
        amazon_link = f"https://www.amazon.in/s?k={title.replace(' ', '+')}+by+{author.replace(' ', '+')}"
        st.markdown(f"[Buy on Amazon.in]({amazon_link})")
        if st.button(f"Read '{title}'"):
            requests.post('https://ntfy.sh/ani_book_rec', data=f'Selected {title} by {author}')
            st.success("Notification sent!")
        st.write("----")

