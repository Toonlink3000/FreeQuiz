from customtkinter import *
from customtkinter import CTkFont
#from tkinter import *

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
		self.quit_button = CTkButton(self, text=quit_text, command=lambda:parent.destroy())
		self.quit_button.grid(row=0, column=1, padx=10, pady=10)

class QuestionDisplay(CTkFrame):
	def __init__(self, parent, main_text, sub_text):
		super().__init__(parent)

		self.main_text_l = CTkLabel(self, text=main_text, font=("default", 30))
		self.main_text_l.grid(row=0, column=0, padx=20, pady=10)

		self.sub_text_l = CTkLabel(self, text=sub_text)
		self.sub_text_l.grid(row=1, column=0, pady=10)

		self.grid_columnconfigure(0, weight=1)

class QuizWelcomeGreeting(CTkFrame):
	def __init__(self, parent, quiz_name:str, author:str):
		super().__init__(parent)
		popo = CTkFont(size=30)
		self.quiz_name_l = CTkLabel(self, text=quiz_name, font=popo)
		self.author_l = CTkLabel(self, text=author)

		self.quiz_name_l.grid(row=0, column=0, padx=10, pady=10)
		self.author_l.grid(row=1, column=0, padx = 10, pady=10)

		self.grid_columnconfigure(0, weight=1)

class QuizGoodbye(CTkFrame):
	def __init__(self, parent, goodbye_message:str):
		super().__init__(parent)

		self.goodbye_message_l = CTkLabel(self, text=goodbye_message, font=("default", 30))
		self.goodbye_message_l.grid(row=0, column=0, padx=10, pady=10)

		self.grid_columnconfigure(0, weight=1)


class QuestionHeader(CTkFrame):
	def __init__(self, parent, main_text:str, sub_text:str):
		super().__init__(parent)
		self.main_text = StringVar()
		self.main_text.set(main_text)
		self.sub_text = StringVar()
		self.sub_text.set(sub_text)

		self.main_text_l = WrappedLabel(self, textvariable=self.main_text, font=("default", 30))
		self.sub_text_l = CTkLabel(self, textvariable=self.sub_text)

		self.main_text_l.grid(row=0, column=0, padx=10, pady=10)
		self.sub_text_l.grid(row=1, column=0, padx = 10, pady=10)

		self.grid_columnconfigure(0, weight=1)

	def refresh_texts(self, main_text:str, sub_text:str):
		self.main_text.set(main_text)
		self.sub_text.set(sub_text)

class QuestionInput(CTkFrame):
	def __init__(self, parent, question):
		super().__init__(parent)
		self.question = question
		self.question.assign_widget(self)

	def draw_answer_box(self):
		self.question.create_input()
		# self.answer = StringVar()
		# self.input_label = CTkLabel(self, text="Enter your answer: ")

	def draw_iscorrect(self):
		self.question.check_answer()

	def refresh_input(self, answer_type):

		self.answer_type = answer_type

		for i in self.grid_slaves():
			i.destroy()

		self.draw_answer_box()

class OptionsMenu(CTkFrame):
	def __init__(self, parent, language_texts, theme_texts, accent_texts):
		super().__init__(parent)
		# 0 is the descrition, 1 is the default value, the rest are the options
		self.language = StringVar()
		self.language.set(language_texts[1])

		self.theme = StringVar()
		self.theme.set(theme_texts[1])

		self.accent = StringVar()
		self.accent.set(accent_texts[1])

		self.language_l = CTkLabel(self, text=language_texts[0])
		self.language_l.grid(row=0, column=0, padx=10, pady=10)
		self.language_menu = CTkOptionMenu(self, self.language, *language_texts[2:])
		self.language_menu.grid(row=0, column=1, padx=10, pady=10)

		self.theme_l = CTkLabel(self, text=theme_texts[0])
		self.theme_l.grid(row=1, column=0, padx=10, pady=10)
		self.theme_menu = CTkOptionMenu(self, self.theme, *theme_texts[2:])
		self.theme_menu.grid(row=1, column=1, padx=10, pady=10)

		self.accent_l = CTkLabel(self, text=accent_texts[0])
		self.accent_l.grid(row=2, column=0, padx=10, pady=10)
		self.accent_menu = CTkOptionMenu(self, self.accent, *accent_texts[2:])
		self.accent_menu.grid(row=2, column=1, padx=10, pady=10)

		self.grid_columnconfigure(1, weight=1)
