from customtkinter import *
from tkinter.filedialog import *
import widgets
from displays import DisplayManager
import sys
import json

class App(CTk):
	def __init__(self):
		super().__init__()
		self.title("OpenQuiz")
		self.display_manager = 
		self.show_start_screen()

	def show_start_screen(self):
		self.control_buttons = widgets.ControlButtons(self, self.open_quiz)
		self.control_buttons.grid(row=2, column=0, pady=50)
		self.title_text = CTkLabel(text="OpenQuiz", text_font=("default", -70))
		self.title_text.grid(row=0, column=0, pady=50)

		self.grid_columnconfigure(0, weight=1)
		self.grid_rowconfigure(1, weight=1)

	def open_quiz(self):
		file_name = askopenfilename(filetypes=(("OpenQuiz quiz file", "*.qwz"), ("JSON files", "*.json"), ("All files", "*")))
		file = open(file_name, "r")
		data = json.loads(file.read())
		file.close()
		self.quiz = Quiz(self, data)
		self.quiz.start_quiz()

class Quiz():
	def __init__(self, win, quiz_data, display_manager):
		self.win = win
		self.data = quiz_data
		self.display_manager = display_manager

	def display_welcome(self):

	def start_quiz(self)
		self.clear_window()
		self.question_display = widgets.QuestionDisplay(self, quiz_data["name"], "hello world")
		self.question_display.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
		self.grid_columnconfigure(0, weight=1)



def main():
	try:
		app = App()
		app.mainloop()

	except Exception as exc:
		pass

if __name__ == '__main__':
	main()