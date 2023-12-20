# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from logic import get_selected_news, get_news_data
from PIL import Image, ImageTk
import os
class NewsGUI:
    def __init__(self, root, show_main_menu):
        self.root = root
        self.show_main_menu = show_main_menu

        self.style = ttk.Style(self.root)
        self.style.configure("News.TFrame", foreground="#ecf0f1")

        self.news_frame = ttk.Frame(self.root, style="News.TFrame")
        self.news_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.treeview = ttk.Treeview(self.news_frame, columns=("Title", "Author", "Date"), show="headings")
        self.setup_treeview()
        self.treeview.pack(pady=20, padx=10, fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.news_frame, orient="vertical", command=self.treeview.yview)
        self.scrollbar.pack(pady=20, fill="y")

        ttk.Button(self.news_frame, text="🔍 Pokaż Treść", command=self.show_selected_news, style="Accent.TButton").pack(pady=10)
        ttk.Button(self.news_frame, text="🏠 Menu główne", command=self.destroy_and_show_main_menu, style="Accent.TButton").pack(pady=10)

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
            self.treeview.delete(*self.treeview.get_children())

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
                NewsInfoPopup(self.root, selected_news, self.treeview, selected_item).run()
            else:
                messagebox.showwarning("Błąd", "Wybierz newsa z listy.")
        else:
            messagebox.showwarning("Błąd", "Wybierz newsa z listy.")

    def show_frame(self, frame):
        frame.tkraise()

    def destroy_and_show_main_menu(self):
        for widget in self.news_frame.winfo_children():
            widget.destroy()

        self.show_main_menu()

class NewsInfoPopup:
    def __init__(self, root, news_info, treeview, selected_item):
        self.root = root
        self.news_info = news_info
        self.treeview = treeview
        self.selected_item = selected_item


        self.popup = tk.Toplevel(root)
        self.popup.title(news_info.get("Tytuł", "Brak tytułu"))

        self.popup.geometry("800x600")

        self.popup.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_position = (screen_width - 800) // 2
        y_position = (screen_height - 600) // 2

        self.popup.geometry(f"800x600+{x_position}+{y_position}")

        image_path = f"news_imgs/news_{self.treeview.index(self.selected_item) + 1}.png"
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((500, 200), Image.BICUBIC)
            photo = ImageTk.PhotoImage(image)

            image_label = tk.Label(self.popup, image=photo)
            image_label.image = photo
            image_label.pack(padx=10, pady=10)

        content_text = tk.Text(self.popup, wrap="word", font=("Helvetica", 12))
        content_text.insert(tk.END, news_info.get("Treść", "Brak treści"))
        content_text.config(state=tk.DISABLED)
        content_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.popup, command=content_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        content_text.config(yscrollcommand=scrollbar.set)

        close_button = tk.Button(self.popup, text="Zamknij", command=self.popup.destroy)
        close_button.pack(pady=10)

    def run(self):
        self.root.wait_window(self.popup)

if __name__ == "__main__":
    root = tk.Tk()

    style = ttk.Style(root)
    style.configure("Accent.TButton", foreground="white", background="#3498db", font=("Helvetica", 10, "bold"))

    app = NewsGUI(root, None) 
    root.title("Kreatywna Aplikacja Newsów")
    root.geometry("1000x600")
    root.mainloop()
