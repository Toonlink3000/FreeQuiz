from customtkinter import *
from tkinter import *

class WrappedLabel(CTkLabel):
	def __init__(self, parent, **kwargs):
		super().__init__(master=parent, **kwargs)
		self.bind('<Configure>', lambda e: self.configure(wraplength=self.winfo_width()))

class ControlButtons(CTkFrame):
	def __init__(self, parent, open_quiz, open_text, quit_text):
		super().__init__(parent)
		self.parent = parent

		self.open_button = CTkButton(self, text=open_text, command=open_quiz)
		self.open_button.grid(row=0, column=0, padx=10, pady=10)
		self.quit_button = CTkButton(self, text=quit_text, command=lambda:sys.exit())
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

class QuizGoodbye(CTkFrame):
	def __init__(self, parent, goodbye_message:str):
		super().__init__(parent)

		self.goodbye_message_l = CTkLabel(self, text=goodbye_message, text_font=("default", 30))
		self.goodbye_message_l.grid(row=0, column=0, padx=10, pady=10)

		self.grid_columnconfigure(0, weight=1)


class QuestionHeader(CTkFrame):
	def __init__(self, parent, main_text:str, sub_text:str):
		super().__init__(parent)
		self.main_text = StringVar()
		self.main_text.set(main_text)
		self.sub_text = StringVar()
		self.sub_text.set(sub_text)

		self.main_text_l = WrappedLabel(self, textvariable=self.main_text, text_font=("default", 20))
		self.sub_text_l = CTkLabel(self, textvariable=self.sub_text)

		self.main_text_l.grid(row=0, column=0, padx=10, pady=10)
		self.sub_text_l.grid(row=1, column=0, padx = 10, pady=10)

		self.grid_columnconfigure(0, weight=1)

	def refresh_texts(self, main_text:str, sub_text:str):
		self.main_text.set(main_text)
		self.sub_text.set(sub_text)

class QuestionInput(CTkFrame):
	def __init__(self, parent, answer_type, options):
		super().__init__(parent)
		self.answer_type = answer_type
		if answer_type != "text":
			self.options = options
		self.draw_answer_box()

	def draw_answer_box(self):
		self.answer = StringVar()
		self.input_label = CTkLabel(self, text="Enter your answer: ")
		match self.answer_type:
			case "text":
				self.input = CTkEntry(self, textvariable=self.answer)
				self.input_label.grid(row=0, column=0, padx=10, pady=10)
				self.input.grid(row=1, column=0, padx=10, pady=10)
				self.total_length = 2

			case "multiple-choice":
				#create a list of radio buttons for each option
				self.input_label.grid(row=0, column=0, padx=10, pady=10)
				self.input = []
				for i, option in enumerate(self.options):
					self.input.append(CTkRadioButton(self, text=option, variable=self.answer, value=option))
					self.input[i].grid(row=i+1, column=0, padx=10, pady=10, sticky="w")

				self.total_length = len(self.options) + 1
				
			case "true-false":
				pass

	def draw_iscorrect(self, correct:str):
		self.iscorrect = CTkLabel(self, text=correct)
		self.iscorrect.grid(row=self.total_length, column=0, padx=10, pady=10)

	def refresh_input(self, answer_type, options):

		self.answer_type = answer_type
		self.options = options

		for i in self.grid_slaves():
			i.destroy()

		self.draw_answer_box()
