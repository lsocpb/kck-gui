import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from logic import login
from leagues_gui import LeaguesGUI
from matches_gui import MatchesGUI
from news_gui import NewsGUI
from quiz_gui import QuizGUI
from fav_teams_gui import FavTeamsGUI
import webbrowser

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Hub")

        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", foreground="#333")

        self.root.geometry("1600x1000")

        self.image_path = "img/soccer.png"
        self.image = Image.open(self.image_path)
        self.image = self.image.resize((200, 200), Image.BICUBIC)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label = ttk.Label(self.root, image=self.photo)
        self.image_label.place(relx=0.1, rely=0.17, anchor="w")

        self.title_image_path = "img/title.png"
        self.title_image = Image.open(self.title_image_path)
        self.title_image = self.title_image.resize((1024, 146), Image.BICUBIC)
        self.title_photo = ImageTk.PhotoImage(self.title_image)
        self.title_image_label = ttk.Label(self.root, image=self.title_photo)
        self.title_image_label.place(relx=0.23, rely=0.20, anchor="w")

        self.login_frame = ttk.Frame(self.root)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.login_frame, text="Login:", font=("Helvetica", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(self.login_frame, font=("Helvetica", 14))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.login_frame, text="Hasło:", font=("Helvetica", 14)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(self.login_frame, show="*", font=("Helvetica", 14))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(self.login_frame, text="Zaloguj", command=self.login, style="TButton").grid(row=2, column=0, columnspan=2, pady=10)

        self.facebook_icon = ImageTk.PhotoImage(Image.open('socials/facebook.png'))
        self.linkedin_icon = ImageTk.PhotoImage(Image.open('socials/linkedin.png'))
        self.github_icon = ImageTk.PhotoImage(Image.open('socials/github.png'))

        self.facebook_button = ttk.Button(self.root, image=self.facebook_icon, command=lambda: webbrowser.open('https://www.facebook.com/'), style = "Social.TButton")
        self.facebook_button["style"] = "Social.TButton"
        self.linkedin_button = ttk.Button(self.root, image=self.linkedin_icon, command=lambda: webbrowser.open('https://www.linkedin.com/in/'), style = "Social.TButton" )
        self.linkedin_button["style"] = "Social.TButton"
        self.github_button = ttk.Button(self.root, image=self.github_icon, command=lambda: webbrowser.open('https://github.com/lsocpb'), style = "Social.TButton")
        self.github_button["style"] = "Social.TButton"


        self.create_footer()


    def create_footer(self):
        button_style = ttk.Style()
        button_style.configure("Social.TButton", 
                             background = "white",
                             borderwidth=0,
                             relief="flat",
                             padding=(5, 5))

        self.facebook_button.place(relx=0.43, rely=0.8)
        self.linkedin_button.place(relx=0.48, rely=0.8)
        self.github_button.place(relx=0.53, rely=0.8)

    def hide_footer(self):
        self.facebook_button.place_forget()
        self.linkedin_button.place_forget()
        self.github_button.place_forget()

    def show_footer(self):
        self.facebook_button.place(relx=0.43, rely=0.8)
        self.linkedin_button.place(relx=0.48, rely=0.8)
        self.github_button.place(relx=0.53, rely=0.8)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_id = login(username, password)

        if user_id is not None:
            self.user_id = user_id
            self.show_main_menu()
        else:
            messagebox.showerror("Błąd logowania", "Nieprawidłowy login lub hasło")

    def show_main_menu(self):
        self.login_frame.destroy()
        self.current_view = None

        self.main_menu_frame = ttk.Frame(self.root)
        self.main_menu_frame.place(relx=0.5, rely=0.5, anchor="center")

        options = ["Informacje o ligach", "Mecze", "Aktualności", "Quizy piłkarskie", "Ulubione drużyny", "Wyjście"]

        for i, option in enumerate(options):
            btn = tk.Button(self.main_menu_frame, 
                            text=option, 
                            command=lambda option=option: self.show_option(option), 
                            font=("Helvetica", 14, "bold"), 
                            bg="#2ecc71", 
                            fg="white", 
                            padx=10, 
                            width=20,
                            height=1,
                            pady=5)
            btn.grid(row=i, column=0, pady=2, padx=20)
            btn.lift()

        self.image_label.place(relx=0.1, rely=0.17, anchor="w")
        self.title_image_label.place(relx=0.23, rely=0.20, anchor="w")
        self.show_footer()

    def show_option(self, option):
        if option == "Informacje o ligach":
            self.hide_footer()
            self.show_leagues_menu()
        if option == "Mecze":
            self.hide_footer()
            self.show_maches_menu()
        if option == "Aktualności":
            self.hide_footer()
            self.show_news_menu()
        if option == "Quizy piłkarskie":
            self.hide_footer()
            self.show_quiz_menu()
        if option == "Ulubione drużyny":
            self.hide_footer()
            self.show_fav_teams_menu()
        if option == "Wyjście":
            self.root.destroy()

    def show_leagues_menu(self):
        self.main_menu_frame.destroy()
        LeaguesGUI(self.root, self.show_main_menu)

    def show_maches_menu(self):
        self.main_menu_frame.destroy()
        MatchesGUI(self.root, self.show_main_menu)
    
    def show_news_menu(self):
        self.image_label.place_forget()
        self.title_image_label.place_forget()
        self.main_menu_frame.destroy()
        NewsGUI(self.root, self.show_main_menu)
    
    def show_quiz_menu(self):
        self.image_label.place_forget()
        self.title_image_label.place_forget()
        self.main_menu_frame.destroy()
        QuizGUI(self.root, self.show_main_menu, self.user_id)

    def show_fav_teams_menu(self):
        self.main_menu_frame.destroy()
        FavTeamsGUI(self.root, self.show_main_menu, self.user_id)
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
