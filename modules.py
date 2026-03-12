from dotenv import load_dotenv
import os
from google import genai as gen
import requests
from bs4 import BeautifulSoup
from google.genai import types
from imdb import Cinemagoer
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
from PIL import Image
import io

# Init################################
load_dotenv()
api_key = os.getenv("API_KEY")
client = gen.Client(api_key=api_key)
model = "gemini-2.0-flash"
vertexai.init(project="storied-polymer-459415-n0", location="us-central1")
imagen_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")


#####################################

def scrape():
    url = "https://www.imdb.com/chart/top/"
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.find_all("h3", {"class": "ipc-title__text"}, limit=11)
    urls = soup.find_all("a", {"class": "ipc-title-link-wrapper"}, limit=10)

    # IMDB Urls
    hrefs = [url.get('href').split('?')[0] for url in urls]
    hrefs = ["https://www.imdb.com" + href for href in hrefs]

    # Movie Titles
    movies.remove(movies[0])
    movie_titles = [movie.text.strip() for movie in movies]

    # Short description
    descs = getdesc(headers, hrefs)

    # Storyline
    strln = []
    for title in movie_titles:
        strln.append(get_movie_storyline(title))

    # Burda hepsini combine etme yerine tıklanan isiminki getirilebilir şuan hepsi bir mapte biraz yavas
    # Combine all
    combined_data = []
    for href, title, desc, strl in zip(hrefs, movie_titles, descs, strln):
        combined_data.append({
            "url": href,
            "title": title,
            "description": desc,
            "storyline": strl
        })
    return combined_data


def scrapeurl():
    url = "https://www.imdb.com/chart/top/"
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = soup.find_all("a", {"class": "ipc-title-link-wrapper"}, limit=10)

    # IMDB Urls
    hrefs = [url.get('href').split('?')[0] for url in urls]
    hrefs = ["https://www.imdb.com" + href for href in hrefs]

    return hrefs


def scrapename():
    url = "https://www.imdb.com/chart/top/"
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.find_all("h3", {"class": "ipc-title__text"}, limit=11)
    movies.remove(movies[0])
    movie_titles = [movie.text.strip() for movie in movies]

    return movie_titles


def getdesc(hrefs):
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    descs = []
    for href in hrefs:
        response = requests.get(href, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        description_tag = soup.find("p", {"class": "sc-191592d9-3 bmtkUm"})
        descs.append(description_tag.text.strip())

    return descs


def getdescsingle(url):
    headers = {
        "Accept-Language": "en-US,en;q=0.5",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    description_tags = soup.find("span", {"class": "sc-d6f3b755-0 erEDdh"})
    return description_tags.text.strip()

def get_movie_storyline(title):
    ia = Cinemagoer()
    movies = ia.search_movie(title)
    if movies:
        movie = ia.get_movie(movies[0].movieID)
    if 'plot outline' in movie:
        return movie['plot outline']
    return "No storyline available."


def generateimage(location, style, scene_description):
    # scene_description from generated dialogue
    prompt = f"Generate an image of a scene in {location} with a {style} style. The atmosphere is described as: {scene_description}"
    response = imagen_model.generate_images(prompt=prompt)

    return response[0].save("image.png")


def generatedialogue(numchars, leng, movie):
    # leng range [2,4]
    response = client.models.generate_content(
        model=model,
        contents=[
            f"Generate a dialogue inside in movie {movie} with {numchars} amount of characters talking,dialogue length is {leng},always explain the scene in the beginning,do not say okay etc."],
    )
    parts = response.text.split("\n\n", 1)
    scene_description = parts[0].strip() if len(parts) > 0 else "No scene description available."
    dialogue = parts[1].strip() if len(parts) > 1 else "No dialogue available."
    return scene_description, dialogue
