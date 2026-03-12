import io
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

from PIL import ImageTk,Image

import modules as fn
import threading

scene_description = ""

headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}




def display_movie_details(event):
    """Displays selected movie details on the right panel."""
    selected_index = movie_listbox.curselection()
    if selected_index:
        selected_movie = movie_listbox.get(selected_index)
        movie_url = movie_urls.get(selected_movie, "URL not available")
        threading.Thread(target=fetch_movie_details, args=(selected_movie, movie_url), daemon=True).start()


def fetch_movie_details(selected_movie, movie_url):
    brief_description = fn.getdescsingle(movie_url)
    storyline = fn.get_movie_storyline(selected_movie)
    root.after(0, lambda: update_details(selected_movie, movie_url, brief_description, storyline))


def update_details(selected_movie, movie_url, brief_description, storyline):
    title_label.config(text=f"Title: {selected_movie}")
    link_label.config(text=f"IMDb Link: {movie_url}", fg="blue", cursor="hand2")
    description_label.config(text=f"Description: {brief_description}")
    storyline_label.config(text=f"Storyline: {storyline}")





def generate_dialogue():
    global scene_description
    numchars = characters_combobox.get()
    leng = dialogue_entry.get()
    if not leng.isdigit():
        messagebox.showwarning("Warning", "Please enter a valid number for dialogue length.")
        return
    leng = int(leng)
    selected_index = movie_listbox.curselection()
    if selected_index:
        selected_movie = movie_listbox.get(selected_index)
        scene_description, dialogue = fn.generatedialogue(numchars, leng, selected_movie)
        scrolled_text.insert(tk.END, scene_description+dialogue+ "\n\n")
    else:
        messagebox.showwarning("Warning", "Please select a movie from the list.")


def refresh_chat():
    scrolled_text.delete("1.0", tk.END)


def refresh_image():
    global generated_image_frame
    generated_image_frame.image_label.config(image='')
    generated_image_frame.image_label.image = None
    messagebox.showinfo("Image Cleared", "Image box cleared.")

def generate_image():
    global generated_image_frame
    location = location_entry.get()
    style = style_combobox.get()
    global scene_description
    if scene_description == "":
        messagebox.showwarning("Warning", "Please generate dialogue first.")
        return

    response = fn.generateimage(location, style, scene_description)
    scene_description = ""


    image = Image.open("image.png")
    image=ImageTk.PhotoImage(image)

    generated_image_frame.image_label = tk.Label(generated_image_frame, image=image)
    generated_image_frame.image_label.image=image
    generated_image_frame.image_label.pack()
    messagebox.showinfo("Image Generated", "Image generated successfully.")



root = tk.Tk()
root.title("IMDB Top 10 Movies")
root.geometry("900x500")

title = tk.Label(root, text="IMDB Top 10 Movies", font=("Arial", 20, "bold"))
title.pack(pady=10)

main_frame = tk.Frame(root)
main_frame.pack(padx=20, pady=10, expand=True, fill="both")

left_frame = tk.Frame(main_frame, bd=2, relief="sunken", width=150)
left_frame.pack(side="left", fill="y", padx=5, pady=5)

movie_listbox = tk.Listbox(left_frame, height=20, width=30)
movie_listbox.pack(side="left", fill="y", padx=5, pady=5)

movie_names = fn.scrapename()
scraped_urls = fn.scrapeurl()
movie_urls = {movie: url for movie, url in zip(movie_names, scraped_urls)}

for movie in movie_names:
    movie_listbox.insert(tk.END, movie)

right_frame = tk.Frame(main_frame, bd=2, relief="sunken", width=750)
right_frame.pack(side="right", expand=True, fill="both", padx=5, pady=5)

notebook = ttk.Notebook(right_frame)
notebook.pack(fill=tk.BOTH, expand=True)

movie_details_frame = ttk.Frame(notebook)
notebook.add(movie_details_frame, text="Movie Details")

generated_dialogue_frame = ttk.Frame(notebook)
notebook.add(generated_dialogue_frame, text="Generated Dialogue")

generated_image_frame = ttk.Frame(notebook)
generated_image_frame.image_label = tk.Label(generated_image_frame)
notebook.add(generated_image_frame, text="Generated Image")

title_label = tk.Label(movie_details_frame, text="Title: ", font=("Arial", 14, "bold"), wraplength=600)
title_label.pack(pady=5, anchor="w")

link_label = tk.Label(movie_details_frame, text="IMDb Link: ", font=("Arial", 12), fg="blue", cursor="hand2",
                      wraplength=600)
link_label.pack(pady=5, anchor="w")

description_label = tk.Label(movie_details_frame, text="Description: ", wraplength=600, justify="left")
description_label.pack(pady=5, anchor="w")

storyline_label = tk.Label(movie_details_frame, text="Storyline: ", wraplength=600, justify="left")
storyline_label.pack(pady=5, anchor="w")


def open_link(event):
    import webbrowser
    url = link_label.cget("text").replace("IMDb Link: ", "")
    if url != "IMDb Link: ":
        webbrowser.open(url)


link_label.bind("<Button-1>", open_link)
movie_listbox.bind("<<ListboxSelect>>", display_movie_details)

characters_label = tk.Label(generated_dialogue_frame, text="Number of Main Characters:", font=("Arial", 8))
characters_label.pack(pady=2, anchor="w")

characters_combobox = ttk.Combobox(generated_dialogue_frame, values=["2", "3", "4"], state="readonly", width=5)
characters_combobox.pack(pady=2, anchor="w")
characters_combobox.current(0)

length_label = tk.Label(generated_dialogue_frame, text="Length of Dialogue (max 1500 words):", font=("Arial", 8))
length_label.pack(pady=2, anchor="w")

dialogue_entry = tk.Entry(generated_dialogue_frame, font=("Arial", 8), width=10)
dialogue_entry.pack(pady=2, anchor="w")

generate_button = tk.Button(generated_dialogue_frame, text="Generate Dialogue", command=generate_dialogue)
generate_button.pack(pady=5)

refresh_button = tk.Button(generated_dialogue_frame, text="Refresh Chat", command=refresh_chat)
refresh_button.pack(pady=5)

scrolled_text = ScrolledText(generated_dialogue_frame, wrap=tk.WORD, width=60, height=15)
scrolled_text.pack(pady=5, expand=True, fill="both")

location_label = tk.Label(generated_image_frame, text="Location:", font=("Arial", 8))
location_label.pack(pady=2, anchor="w")

location_entry = tk.Entry(generated_image_frame, font=("Arial", 8), width=20)
location_entry.pack(pady=2, anchor="w")

style_label = tk.Label(generated_image_frame, text="Style:", font=("Arial", 8))
style_label.pack(pady=2, anchor="w")

style_combobox = ttk.Combobox(generated_image_frame, values=["Realistic", "Cartoon", "Marvel", "Futuristic"],
                              state="readonly", width=15)
style_combobox.pack(pady=2, anchor="w")
style_combobox.current(0)

generate_image_button = tk.Button(generated_image_frame, text="Generate Image", command=generate_image)
generate_image_button.pack(pady=5)

refresh_image_button = tk.Button(generated_image_frame, text="Refresh Image", command=refresh_image)
refresh_image_button.pack(pady=5)

root.mainloop()
