import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO

URL_BASE = "https://wallhaven.cc/api/v1/search"

class bgManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Bg Manager")

        # Configurar la barra de búsqueda
        self.search_frame = ttk.Frame(root)
        self.search_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Etiqueta "Search Topic"
        self.query_label = ttk.Label(self.search_frame, text="Search Topic:")
        self.query_label.grid(row=0, column=0, padx=5, pady=5)

        # Campo de entrada
        self.query_entry = ttk.Entry(self.search_frame, width=50)
        self.query_entry.grid(row=0, column=1, padx=5, pady=5)

        # Botón "Search"
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.images_frame = ttk.Frame(root)
        self.images_frame.grid(row=1, column=0, padx=10, pady=10)

    def search(self):
        query = self.query_entry.get()
        print(f"Search query: {query}")
        params = {
            'q': query,  
            }
        response = requests.get(URL_BASE, params=params)
        if response.status_code == 200:
            data = response.json()
            listOfPaths = []
            for x in data['data']:
                listOfPaths.append(x['path'])
            self.display_images(listOfPaths)
            for path in listOfPaths:
                print(path)
        else:
            print(f"Error en la solicitud: {response.status_code}")    
    
    def display_images(self, image_urls):
        for widget in self.images_frame.winfo_children():
                widget.destroy()

        for i, image_url in enumerate(image_urls[:9]):  # Mostrar hasta 9 imágenes
            response = requests.get(image_url)
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image = image.resize((200, 200), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            image_label = ttk.Label(self.images_frame, image=photo)
            image_label.image = photo  # Guardar una referencia para evitar la recolección de basura
            image_label.grid(row=i//3, column=i%3, padx=10, pady=10)



if __name__ == "__main__":
    root = tk.Tk()
    app = bgManager(root)
    root.mainloop()