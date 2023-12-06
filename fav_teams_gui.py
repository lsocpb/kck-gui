import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from logic import save_favorite_team, get_current_favorite_team, get_last_results

class FavTeamsGUI:
    def __init__(self, root, show_main_menu ,user_id):
        self.root = root
        self.user_id = user_id
        self.current_favorite_team = get_current_favorite_team(user_id)
        self.show_main_menu = show_main_menu

        self.style = ttk.Style(self.root)
        self.style.configure("TButton", 
                             foreground = "white",
                             borderwidth=0,
                             relief="flat",
                             padding=(5, 5))

        self.teams_frame = ttk.Frame(self.root, style="Teams.TFrame")
        self.teams_frame.place(relx=0.5, rely=0.5, anchor="cente")

        self.selected_row_favorite_teams = 0
        self.selected_row_team = 0
        self.rows_per_page = 15
        self.page = 0

        ttk.Button(self.teams_frame, text = "Wybierz ulubioną drużynę", command= lambda: self.select_favorite_team(), style="TButton").pack(pady=10)

    def display_favorite_teams_menu(self):
        self.clear_frame()

        title_label = ttk.Label(self.teams_frame, text=f"TWOJA ULUBIONA DRUŻYNA: {self.current_favorite_team}")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))


        menu_options = ["Wybierz ulubioną drużynę", "Sprawdź ostatnie wyniki", "Powrót"]

        for i, option in enumerate(menu_options):
            button = ttk.Button(self.teams_frame, text=option, command=lambda option=option: self.handle_menu_option(option))
            button.grid(row=i + 3, column=1, pady=5, padx=10)

    def handle_menu_option(self, option):
        if option == "Wybierz ulubioną drużynę":
            self.select_favorite_team()
        elif option == "Sprawdź ostatnie wyniki":
            self.display_last_results()
        elif option == "Powrót":
            self.destroy_and_show_main_menu()

    def select_favorite_team(self):
        self.clear_frame()

        available_teams = ["FC BARCELONA", "REAL MADRYT", "BAYERN MONACHIUM", "MANCHESTER UNITED", "MANCHESTER CITY", "CHELSEA FC", "BORUSSIA DORTMUND",
                           "AC MILAN", "INTER MEDIOLAN", "JUVENTUS TURYN", "PARIS SAINT-GERMAIN", "LIVERPOOL FC", "ARSENAL FC", "TOTTENHAM HOTSPUR", "ATLETICO MADRYT", "WIECZYSTA KRAKOW"]
        
        num_columns=5

        for i, team in enumerate(available_teams[self.page * self.rows_per_page: (self.page + 1) * self.rows_per_page], start=1):
            team_color = team.lower().replace(" ", "_")
            image_path = f"team_colors/{team_color}.png"

            try:
                image = Image.open(image_path)
                image = image.resize((100, 103), Image.BILINEAR)
                photo = ImageTk.PhotoImage(image)
            except FileNotFoundError:
                photo = None

            if photo:
                row_position = (i - 1) // num_columns
                col_position = (i - 1) % num_columns
                button = ttk.Button(self.teams_frame, image=photo, compound="center", style=f"TButton", command=lambda team=team: self.save_favorite_team(team))
                button_style = ttk.Style()
                button_style.configure("Teams.TButton", 
                             background = "white",
                             borderwidth=0,
                             relief="flat",
                             padding=(5, 5))
                button["style"] = "Teams.TButton" 
                button.image = photo
                button.config(compound="left", image=photo)
                button.grid(row=row_position, column=col_position, pady=5)

        self.style.configure("BackButton.TButton", background="#e74c3c", font=("Helvetica", 10, "bold"))
        back_button = ttk.Button(self.teams_frame, text="Powrót", command=self.display_favorite_teams_menu, style="BackButton.TButton")
        back_button.grid(row=len(available_teams[self.page * self.rows_per_page: (self.page + 1) * self.rows_per_page]) + 2, column=2, pady=5)

    def save_favorite_team(self, team):
        save_favorite_team(self.user_id, team)
        self.current_favorite_team = get_current_favorite_team(self.user_id)
        self.display_favorite_teams_menu()

    def display_last_results(self):
        self.clear_frame()

        results_data = get_last_results(self.user_id)

        if isinstance(results_data, str):
            result_label = ttk.Label(self.teams_frame, text=results_data)
            result_label.grid(row=3, column=1, pady=10)
        else:
            team_name_label = ttk.Label(self.teams_frame, text=f"Ostatnie wyniki dla {results_data['team_name']}:")
            team_name_label.grid(row=3, column=1, pady=5)

            for i, result in enumerate(results_data["results"], start=1):
                outcome_color = "green" if result["color"] == "RED" else "red"
                if result["color"] == "YELLOW":
                    outcome_color = "yellow"

                self.style.configure(f"ResultLabel{i}.TLabel", foreground=outcome_color)
                result_label = ttk.Label(self.teams_frame, text=f"{result['opponent']}: {result['score']} ({result['outcome']})", style=f"ResultLabel{i}.TLabel")
                result_label.grid(row=i + 3, column=1, pady=5)

        self.style.configure("BackButton.TButton", background="#e74c3c", font=("Helvetica", 10, "bold"))
        back_button = ttk.Button(self.teams_frame, text="Powrót", command=self.display_favorite_teams_menu, style="BackButton.TButton")
        back_button.grid(row=5 + len(results_data["results"]), column=1, pady=5)

    def clear_frame(self):
        for widget in self.teams_frame.winfo_children():
            widget.destroy()

    def destroy_and_show_main_menu(self):
        self.clear_frame()
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    user_id = "example_user_id"  # Replace with actual user_id
    app = FavTeamsGUI(root, user_id)
    root.mainloop()
