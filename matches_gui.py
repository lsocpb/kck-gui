# matches_gui.py
import tkinter as tk
from tkinter import ttk, messagebox
from logic import get_active_matches

class MatchesGUI:
    def __init__(self, root, show_main_menu):
        self.root = root
        self.show_main_menu = show_main_menu

        self.matches_frame = ttk.Frame(self.root)
        self.matches_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.canvas = tk.Canvas(self.matches_frame, bg="#ecf0f1", width=400, height=200, highlightthickness=0)
        self.canvas.pack(pady=20)

        ttk.Button(self.matches_frame, text="🔍 Pobierz Mecze", command=self.show_active_matches).pack(pady=10)
        ttk.Button(self.matches_frame, text="🏠 Menu główne", command=self.destroy_and_show_main_menu).pack(pady=10)

    def show_active_matches(self):
        active_matches = get_active_matches()

        if active_matches:
            self.draw_matches(active_matches)
            self.show_frame(self.matches_frame)
        else:
            messagebox.showinfo("Brak Meczów", "Brak aktualnych meczów do wyświetlenia.")

    def draw_matches(self, matches):
        self.canvas.delete("all")

        header = tk.Label(self.matches_frame, text="Aktualne mecze", font=("Helvetica", 16), bg="#3498db", fg="white")
        header_window = self.canvas.create_window(300, 30, anchor="center", window=header)

        y_position = 80

        for match in matches:
            match_label = tk.Label(self.matches_frame, text=match, font=("Helvetica", 12), bg="#ecf0f1", fg="#2c3e50")
            match_window = self.canvas.create_window(300, y_position, anchor="center", window=match_label)

            y_position += 40

        self.animate_matches(header_window, match_window)

    def animate_matches(self, header_window, match_window):
        self.canvas.itemconfig(header_window, state="hidden")
        self.canvas.itemconfig(match_window, state="hidden")

        for i in range(10):
            self.canvas.after(i * 100, lambda i=i: self.canvas.itemconfig(header_window, state="normal"))
            self.canvas.after(i * 100, lambda i=i: self.canvas.itemconfig(match_window, state="normal"))

    def show_frame(self, frame):
        frame.tkraise()

    def destroy_and_show_main_menu(self):
        # Usuń wszystkie widgety z ramki
        for widget in self.matches_frame.winfo_children():
            widget.destroy()

        # Pokaż menu główne
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    app = MatchesGUI(root, None)  # None, ponieważ nie potrzebujemy show_main_menu dla tego przykładu
    root.mainloop()
