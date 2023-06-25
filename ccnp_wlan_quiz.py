import csv
import random
import tkinter as tk
from tkinter import messagebox

class Quiz:
    def __init__(self, quiz_file):
        self.questions = []
        self.choices = []
        self.answers = []
        self.explanations = []
        self.load_quiz(quiz_file)
        self.shuffle_questions()
        self.current_question = 0
        self.score = 0

    def load_quiz(self, quiz_file):
        with open(quiz_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                question, choices, answer, explanation = row
                self.questions.append(question)
                self.choices.append(choices.split('|'))
                self.answers.append(answer)
                self.explanations.append(explanation)

    def shuffle_questions(self):
        combined = list(zip(self.questions, self.choices, self.answers, self.explanations))
        random.shuffle(combined)
        self.questions, self.choices, self.answers, self.explanations = zip(*combined)

    def check_answer(self, user_answer):
        if user_answer.lower() == self.answers[self.current_question].lower():
            self.score += 1
            explanation = self.explanations[self.current_question]
            messagebox.showinfo("Correct", f"Your answer is correct!\n\nExplanation:\n{explanation}")
        else:
            messagebox.showinfo("Incorrect", f"Your answer is incorrect. The correct answer is: {self.answers[self.current_question]}")
        self.current_question += 1
        if self.current_question == len(self.questions):
            self.show_result()
        else:
            self.show_question()

    def show_question(self):
        question_label.config(text=self.questions[self.current_question])
        for idx, choice in enumerate(self.choices[self.current_question]):
            choice_buttons[idx].config(text=choice)
            choice_buttons[idx].deselect()  # Reset the selection
        submit_button.config(state=tk.DISABLED)  # Disable the submit button until a choice is selected

    def show_result(self):
        messagebox.showinfo("Quiz Result", f"You scored {self.score}/{len(self.questions)}")
        window.destroy()

def submit_answer():
    selected = selected_choice.get()
    if selected == -1:
        messagebox.showinfo("Error", "Please select an answer.")
    else:
        user_answer = choice_buttons[selected]['text']
        quiz.check_answer(user_answer)

def enable_submit_button():
    selected = selected_choice.get()
    if selected != -1:
        submit_button.config(state=tk.NORMAL)  # Enable the submit button when a choice is selected
    else:
        submit_button.config(state=tk.DISABLED)  # Disable the submit button if no choice is selected

# Create the main window
window = tk.Tk()
window.title("Quiz")
window.geometry("400x300")

# Create question label
question_label = tk.Label(window, text="Question", wraplength=300)
question_label.pack(pady=10)

# Create choice buttons
choice_buttons = []
selected_choice = tk.IntVar()
for i in range(4):
    choice_button = tk.Radiobutton(window, text="", variable=selected_choice, value=i, command=enable_submit_button)
    choice_button.pack(pady=5)
    choice_buttons.append(choice_button)

# Create submit button
submit_button = tk.Button(window, text="Submit", command=submit_answer, state=tk.DISABLED)
submit_button.pack(pady=10)

# Load the quiz
quiz = Quiz("quiz.csv")
quiz.show_question()

# Start the main event loop
window.mainloop()
