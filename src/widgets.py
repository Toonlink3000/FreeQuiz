from customtkinter import *
from tkinter import *

class WrappedLabel(CTkLabel):
	def __init__(self, parent, **kwargs):
		super().__init__(master=parent, **kwargs)
		self.bind('<Configure>', lambda e: self.configure(wraplength=self.winfo_width()))

class ControlButtons(CTkFrame):
	def __init__(self, parent, open_quiz):
		super().__init__(parent)
		self.parent = parent

		self.open_button = CTkButton(self, text="Open a quiz", command=open_quiz)
		self.open_button.grid(row=0, column=0, padx=10, pady=10)
		self.quit_button = CTkButton(self, text="Quit", command=lambda:sys.exit())
		self.quit_button.grid(row=0, column=1, padx=10, pady=10)

class QuestionDisplay(CTkFrame):
	def __init__(self, parent, main_text, sub_text):
		super().__init__(parent)

		self.main_text_l = CTkLabel(self, text=main_text, text_font=("default", 30))
		self.main_text_l.grid(row=0, column=0, padx=20, pady=10)

		self.sub_text_l = CTkLabel(self, text=sub_text)
		self.sub_text_l.grid(row=1, column=0, pady=10)

		self.grid_columnconfigure(0, weight=1)

class QuizWelcomeGreeting(CTkFrame):
	def __init__(self, parent, quiz_name:str, author:str):
		super().__init__(parent)

		self.quiz_name_l = CTkLabel(self, text=quiz_name, text_font=("default", 30))
		self.author_l = CTkLabel(self, text=author)

		self.quiz_name_l.grid(row=0, column=0, padx=10, pady=10)
		self.author_l.grid(row=1, column=0, padx = 10, pady=10)

		self.grid_columnconfigure(0, weight=1)