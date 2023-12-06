import tkinter as tk
from tkinter import ttk
from logic import save_quiz_results_to_db, read_quiz_results_from_db, get_specialized_quiz_questions, get_general_quiz_questions
import ttkbootstrap as ttb

class QuizGUI:
    def __init__(self, root, show_main_menu, user_id):
        self.root = root
        self.user_id = user_id
        self.show_main_menu = show_main_menu

        self.style = ttk.Style(self.root)
        self.style.configure("Quiz.TFrame", foreground="#ecf0f1")  # Set background color using style

        self.quiz_frame = ttk.Frame(self.root, style="Quiz.TFrame")  # Use the configured style
        self.quiz_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.style.configure("Big.TButton", foreground="white", background="#3498db", font=("Helvetica", 14, "bold"))

        ttk.Button(self.quiz_frame, text="🔍 Ogólny Quiz", command=lambda: self.run_quiz("Quiz Ogólny", get_general_quiz_questions()), style="TButton").pack(pady=10)
        ttk.Button(self.quiz_frame, text="🔍 Specjalistyczny Quiz", command=lambda: self.run_quiz("Quiz Specjalistyczny", get_specialized_quiz_questions()), style="TButton").pack(pady=10)
        ttk.Button(self.quiz_frame, text="📊 Wyniki Quizów", command=self.display_quiz_results, style="TButton").pack(pady=10)
        ttk.Button(self.quiz_frame, text="🏠 Menu główne", command=self.destroy_and_show_main_menu, style="TButton").pack(pady=10)

        
    def run_quiz(self, quiz_name, quiz_questions):
        self.quiz_frame.destroy()
        self.quiz_frame = ttk.Frame(self.root, style="Quiz.TFrame")
        self.quiz_frame.place(relx=0.5, rely=0.5, anchor="center")

        selected_question = 0
        score = 0

        question_var = tk.StringVar()
        question_label = tk.Label(self.quiz_frame, textvariable=question_var, font=("Helvetica", 16, "bold"), wraplength=600, justify="center", padx=20, pady=20)
        question_label.pack(pady=20)

        answers_frame = ttk.Frame(self.quiz_frame)
        answers_frame.pack(pady=20)

        answer_var = tk.StringVar()

        def show_next_question():
            nonlocal selected_question, score

            if selected_question < len(quiz_questions):
                question_var.set(quiz_questions[selected_question]["Pytanie"])

                # Clear only widgets related to the current question
                for widget in answers_frame.winfo_children():
                    widget.destroy()
                
                radio_buttons = []

                for i, answer in enumerate(quiz_questions[selected_question]["Odpowiedzi"]):
                    answer_radio = tk.Radiobutton(
                        answers_frame,
                        text=answer,
                        variable=answer_var,
                        value=chr(ord("A") + i),
                        font=("Helvetica", 12),
                        pady=5,
                        indicatoron=0,
                        width=20,
                        selectcolor="#2ecc71",
                        background="#3498db",
                        anchor="w", padx=20)
                    answer_radio.pack(fill="both", padx=20, pady=5)

                    radio_buttons.append(answer_radio)

                global confirm_button
                confirm_button = tk.Button(self.quiz_frame, text="Potwierdź", command=lambda: process_answer(), font=("Helvetica", 14, "bold"), bg="#2ecc71", fg="white", padx=10, pady=10)
                confirm_button.pack(pady=20)

                answers_frame.radio_buttons = radio_buttons
                answer_var.set(None)

            elif selected_question == len(quiz_questions):
                save_quiz_results_to_db(self.user_id, quiz_name, score)
                self.quiz_frame.destroy()
                app = QuizGUI(self.root, self.show_main_menu, self.user_id)
                self.show_quiz_result(quiz_name, score, len(quiz_questions))

        def process_answer():
            nonlocal selected_question, score
            selected_answer = answer_var.get()

            if selected_answer is not None:
                correct_answer = quiz_questions[selected_question]["Poprawna odpowiedź"]
                if selected_answer == correct_answer:
                    score += 1
                selected_question += 1

            # Clear only widgets related to the current question
                for widget in answers_frame.winfo_children():
                    widget.destroy()

                confirm_button.destroy()  # Destroy the "Potwierdź" button

                show_next_question()

        show_next_question()

    def show_quiz_result(self, quiz_name, score, total_questions):
        result_window = tk.Toplevel(self.root)
        result_window.title(f"Twój wynik ({quiz_name})")

        result_label = tk.Label(result_window, text=f"Twój wynik ({quiz_name}): {score}/{total_questions}", font=("Helvetica", 14, "bold"))
        result_label.pack(pady=20)

        percentage = score / total_questions * 100
        meter = ttb.Meter(
            result_window,
            metersize=200,
            padding=20,
            amountused=percentage,
            amounttotal=100,
            textright="%",
            metertype = "semi",
            )
        meter.pack()

        confirm_button = tk.Button(result_window, text="OK", command=result_window.destroy)
        confirm_button.pack(pady=10)

        result_window.update_idletasks()
        width = result_window.winfo_width()
        height = result_window.winfo_height()
        x = (result_window.winfo_screenwidth() - width) // 2
        y = (result_window.winfo_screenheight() - height) // 2
        result_window.geometry(f"{width}x{height}+{x}+{y}")

        result_window.wait_window(result_window)

    def display_quiz_results(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Ostatnie Wyniki Quizów")

        results_label = tk.Label(result_window, text="Ostatnie 5 wyników quizów:", font=("Helvetica", 14, "bold"))
        results_label.pack(pady=10)

        quiz_results = read_quiz_results_from_db(self.user_id)

        for result in quiz_results[-5:]:
            quiz_name, score = result
            result_text = f"{quiz_name}: {score}/5"
            result_label = tk.Label(result_window, text=result_text, font=("Helvetica", 12))
            result_label.pack()

        confirm_button = tk.Button(result_window, text="OK", command=result_window.destroy)
        confirm_button.pack(pady=10)

        result_window.wait_window(result_window)

    def destroy_and_show_main_menu(self):
        self.quiz_frame.destroy()
        self.show_main_menu()

if __name__ == "__main__":
    root = tk.Tk()
    user_id = None
    # Ustawienie globalnego stylu dla przycisków
    app = QuizGUI(root, user_id)
    root.title("Aplikacja Quizów")
    root.geometry("800x600")
    root.mainloop()
