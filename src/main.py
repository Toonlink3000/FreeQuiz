from customtkinter import *
from tkinter.filedialog import *
import displays
import sys
import json

class App(CTk):
	def __init__(self):
		super().__init__()
		self.title("OpenQuiz")
		self.display_manager = displays.DisplayManager(self)
		self.display_manager.jump_to_display(0)

class Quiz():
	def __init__(self, win, quiz_data, display_manager):
		self.win = win
		self.data = quiz_data
		self.display_manager = display_manager

	def display_welcome(self):
		pass

	def start_quiz(self):
		self.clear_window()
		self.question_display = widgets.QuestionDisplay(self, quiz_data["name"], "hello world")
		self.question_display.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
		self.grid_columnconfigure(0, weight=1)

def main():
	app = App()
	app.mainloop()

if __name__ == '__main__':
	main()