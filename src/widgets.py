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

class QuestionHeader(CTkFrame):
	def __init__(self, parent, main_text:str, sub_text:str):
		super().__init__(parent)
		self.main_text = StringVar()
		self.main_text.set(main_text)
		self.sub_text = StringVar()
		self.sub_text.set(sub_text)

		self.main_text_l = WrappedLabel(self, text=main_text, text_font=("default", 20))
		self.sub_text_l = CTkLabel(self, text=sub_text)

		self.main_text_l.grid(row=0, column=0, padx=10, pady=10)
		self.sub_text_l.grid(row=1, column=0, padx = 10, pady=10)

		self.grid_columnconfigure(0, weight=1)

	def refresh_texts(self, main_text:str, sub_text:str):
		self.main_text.set(main_text)
		self.sub_text.set(sub_text)

class QuestionInput(CTkFrame):
	def __init__(self, parent, answer_type):
		super().__init__(parent)

		match answer_type:
			case "text":
				self.drawinput_text()

	def drawinput_text(self):
		self.answer = StringVar()
		self.input_label = CTkLabel(self, text="Enter your answer: ")
		self.input = CTkEntry(self, textvariable=self.answer)

		self.input_label.grid(row=0, column=0, padx=10, pady=10)
		self.input.grid(row=1, column=0, padx=10, pady=10)

	def draw_iscorrect(self, correct:str):
		self.corectness_label = CTkLabel(self, text=correct)
		self.corectness_label.grid(row=2, column=0, pady=10)

	def refresh_input(self, answer_type):
		self.answer.set("")
		self.corectness_label.destroy()
