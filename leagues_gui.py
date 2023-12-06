# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from logic import load_info, get_selected_league_info
import imageio

class LeaguesGUI:
    def __init__(self, root, show_main_menu):
        self.root = root
        self.show_main_menu = show_main_menu
        self.top_european_leagues_info = load_info("data/top_european_leagues_info.json")

        self.leagues_frame = ttk.Frame(self.root)
        self.leagues_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Utwórz Treeview z kolumnami
        self.treeview = ttk.Treeview(self.leagues_frame, columns=("Name", "Country", "Founded", "Teams"), show="headings")
        self.setup_treeview()
        self.treeview.grid(row=0, column=0, pady=10, padx=20, sticky="nsew")

        # DODAJE ZDJECIE DO TREEVIEW
        for league_info in self.top_european_leagues_info:
            img = Image.open("flags/flag_1.png")  # Zmień to, aby pobierać odpowiednie obrazy dla każdej ligi
            img = ImageTk.PhotoImage(img)

            tag = f"img_{id(img)}"  # Unikalny tag dla każdego obrazu
            self.treeview.insert("", "end", values=(f"{league_info['Nazwa ligi']}", league_info["Kraj"], league_info["Rok założenia"], league_info["Liczba drużyn"]), tags=(tag,))
            self.treeview.tag_configure(tag, image=img)

        self.scrollbar = ttk.Scrollbar(self.leagues_frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.grid(row=0, column=1, pady=10, sticky="ns")

        # Zmiana kursora
        self.treeview.bind("<Enter>", lambda event: self.treeview.config(cursor="hand2"))
        self.treeview.bind("<Leave>", lambda event: self.treeview.config(cursor=""))

        # Przycisk stylizowany
        search_button = ttk.Button(self.leagues_frame, text="🔍 Wybierz", command=self.show_selected_league_gif)
        search_button.grid(row=1, column=0, pady=10)
        search_button_style = ttk.Style()
        search_button_style.configure("SearchButton.TButton", foreground="white", background="#27ae60", font=("Helvetica", 10, "bold"))
        search_button["style"] = "SearchButton.TButton"

        main_menu_button = ttk.Button(self.leagues_frame, text="🏠 Menu główne", command=self.destroy_and_show_main_menu)
        main_menu_button.grid(row=2, column=0, pady=10)
        main_menu_button_style = ttk.Style()
        main_menu_button_style.configure("MainMenuButton.TButton", foreground="white", background="#e74c3c", font=("Helvetica", 10, "bold"))
        main_menu_button["style"] = "MainMenuButton.TButton"

        # Dodaj atrybut do przechowywania referencji do etykiety z obrazem GIF
        self.gif_label = None

    def setup_treeview(self):
        self.treeview.heading("Name", text="Nazwa ligi")
        self.treeview.heading("Country", text="Kraj")
        self.treeview.heading("Founded", text="Założona")
        self.treeview.heading("Teams", text="Liczba drużyn")

        

    def destroy_and_show_main_menu(self):
        # Usuń wszystkie widgety z ramki
        for widget in self.leagues_frame.winfo_children():
            widget.destroy()

        # Pokaż menu główne
        self.show_main_menu()

    def show_selected_league_gif(self):
        selected_item = self.treeview.selection()

        if selected_item:
            # Uzyskaj indeks wybranej ligi
            selected_row = self.treeview.index(selected_item)

            # Uzyskaj nazwę pliku GIF dla wybranej ligi (zmień na odpowiednią nazwę pliku)
            gif_filename = f"ligi_gify/lig_{selected_row + 1}.gif"

            # Wyświetl plik GIF
            self.display_gif(gif_filename)
        else:
            messagebox.showwarning("Błąd", "Wybierz ligę z listy.")

    def display_gif(self, gif_filename):
        # Wczytaj plik GIF przy użyciu modułu Pillow
        gif_reader = imageio.get_reader(gif_filename)
        gif_frames = [ImageTk.PhotoImage(Image.fromarray(frame)) for frame in gif_reader]

        # Usuń poprzednią etykietę z obrazem GIF, jeśli istnieje
        if self.gif_label:
            self.gif_label.destroy()

        # Utwórz etykietę do wyświetlania pliku GIF
        self.gif_label = tk.Label(self.root)
        self.gif_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Wyświetl animację
        self.animate_gif(0, len(gif_frames), gif_frames)

    def animate_gif(self, count, total_frames, frames):
        new_image = frames[count]
        self.gif_label.configure(image=new_image)
        count += 1
        if count == total_frames:
            self.gif_label.destroy()
            return

        # Kontynuuj animację
        self.root.after(50, lambda: self.animate_gif(count, total_frames, frames))
