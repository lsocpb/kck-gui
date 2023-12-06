# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from logic import get_selected_news, get_news_data
class NewsGUI:
    def __init__(self, root, show_main_menu):
        self.root = root
        self.show_main_menu = show_main_menu

        self.style = ttk.Style(self.root)
        self.style.configure("News.TFrame", foreground="#ecf0f1")  # Set background color using style

        self.news_frame = ttk.Frame(self.root, style="News.TFrame")  # Use the configured style
        self.news_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.treeview = ttk.Treeview(self.news_frame, columns=("Title", "Author", "Date"), show="headings")
        self.setup_treeview()
        self.treeview.pack(pady=20, padx=10, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.news_frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(pady=20, fill="y")

        ttk.Button(self.news_frame, text="🔍 Pokaż Treść", command=self.show_selected_news, style="Accent.TButton").pack(pady=10)
        ttk.Button(self.news_frame, text="🏠 Menu główne", command=self.destroy_and_show_main_menu, style="Accent.TButton").pack(pady=10)

        # Pobierz aktualności od razu po inicjalizacji
        self.show_news()

    def setup_treeview(self):
        self.treeview.heading("Title", text="Tytuł")
        self.treeview.heading("Author", text="Autor")
        self.treeview.heading("Date", text="Data")
        self.treeview.column("Title", width=500)
        self.treeview.column("Author", width=150)
        self.treeview.column("Date", width=100)

    def show_news(self):
        news_data = get_news_data()

        if news_data:
            self.treeview.delete(*self.treeview.get_children())  # Wyczyść poprzednie wpisy

            for news_item in news_data:
                title = news_item.get("Tytuł", "")
                author = news_item.get("Autor", "")
                date = news_item.get("Data dodania", "")
                self.treeview.insert("", "end", values=(title, author, date))

            self.show_frame(self.news_frame)
        else:
            messagebox.showinfo("Brak Aktualności", "Brak aktualności do wyświetlenia.")

    def show_selected_news(self):
        selected_item = self.treeview.selection()

        if selected_item:
            selected_news = get_selected_news(get_news_data(), self.treeview.index(selected_item))
            if selected_news:
                NewsInfoPopup(self.root, selected_news).run()
            else:
                messagebox.showwarning("Błąd", "Wybierz newsa z listy.")
        else:
            messagebox.showwarning("Błąd", "Wybierz newsa z listy.")

    def show_frame(self, frame):
        frame.tkraise()

    def destroy_and_show_main_menu(self):
        # Usuń wszystkie widgety z ramki
        for widget in self.news_frame.winfo_children():
            widget.destroy()

        # Pokaż menu główne
        self.show_main_menu()

class NewsInfoPopup:
    def __init__(self, root, news_info):
        self.root = root
        self.news_info = news_info

        self.popup = tk.Toplevel(root)
        self.popup.title(news_info.get("Tytuł", "Brak tytułu"))

        # Ustaw większą szerokość dla okna popup
        self.popup.geometry("600x400")

        # Tworzenie etykiety do wyświetlenia treści
        content_label = tk.Label(self.popup, text=news_info.get("Tresc", "Brak treści"), wraplength=550, justify="left", font=("Helvetica", 12))
        content_label.pack(padx=10, pady=10)

    def run(self):
        self.root.wait_window(self.popup)

if __name__ == "__main__":
    root = tk.Tk()

    # Ustawienie globalnego stylu dla przycisków
    style = ttk.Style(root)
    style.configure("Accent.TButton", foreground="white", background="#3498db", font=("Helvetica", 10, "bold"))

    app = NewsGUI(root, None)  # None, ponieważ nie potrzebujemy show_main_menu dla tego przykładu
    root.title("Kreatywna Aplikacja Newsów")
    root.geometry("1000x600")  # Zwiększ szerokość okna
    root.mainloop()
