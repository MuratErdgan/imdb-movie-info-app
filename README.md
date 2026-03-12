# IMDb Movie Explorer 🎬

A Python desktop application that retrieves movie data from IMDb, displays it through a Tkinter graphical interface, and generates AI-based movie dialogues and scene images.

## Features
- Displays IMDb Top 10 movies
- Shows movie description and storyline
- Opens the IMDb page link of the selected movie
- Generates AI-based movie dialogues using Gemini API
- Creates scene images from the generated dialogue using Google's Imagen model
- User-friendly Tkinter GUI interface

## Technologies Used
Python, Tkinter, BeautifulSoup, Requests, IMDbPY (Cinemagoer), Google Gemini API, Google Imagen API, Vertex AI, Pillow

## How It Works
The application scrapes the IMDb Top 10 movie list and displays it in a Tkinter interface. When a movie is selected, its description and storyline are retrieved and shown. Users can generate AI-based dialogue scenes for the selected movie and create scene images based on the generated dialogue.

## Installation
pip install requests beautifulsoup4 pillow python-dotenv imdbpy google-generativeai

## Run
python main.py

## Project Structure
main.py – Tkinter GUI  
modules.py – scraping, API calls, and AI generation  
image.png – generated image output  
.env – API key configuration
