from customtkinter import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import widgets
import sys
import json
import enum
import exceptions
import quiz

class Displays(enum.Enum):
	START_SCREEN = 0
	QUIZ_WELCOME = 1
	QUIZ_PAGE = 2
	QUIZ_END = 3

class DisplayManager():
	def __init__(self, window):
		self.current_display = 0
		self.window = window

	def jump_to_display(self, display:int, **displayargs):
		last_display = self.current_display
		self.current_display = display
		self.open_display = None
		self.clear_window()
		try:
			self.open_display = DISPLAYS[self.current_display](self.window, self, displayargs)
		except exceptions.QuizDataNotProvided:
			showerror("QuizDataNotProvided Error","Quiz data was not provided to the display: {} from diplay {}".format(Displays(display).name, Displays(last_display).name))
			sys.exit()
	def clear_window(self):
		widget_list =  self.window.winfo_children()
		for item in widget_list:
			item.destroy()

class StartScreen():
	def __init__(self, window, display_manager, displayargs:dict):
		window.control_buttons = widgets.ControlButtons(window, self.open_quiz)
		window.control_buttons.grid(row=2, column=0, pady=50)
		window.title_text = CTkLabel(text="FreeQuiz", text_font=("default", -70))
		window.title_text.grid(row=0, column=0, pady=50)

		window.grid_columnconfigure(0, weight=1)
		window.grid_rowconfigure(1, weight=1)
		self.display_manager = display_manager

	def open_quiz(self):
		file_name = askopenfilename(filetypes=(("FreeQuiz quiz file", "*.qwz"), ("JSON files", "*.json"), ("All files", "*")))
		if file_name == ():
			return
		data = quiz.Quiz()
		data.load_from_file(file_name)
		self.display_manager.jump_to_display(Displays.QUIZ_WELCOME.value, data=data)


class QuizWelcome():
	def __init__(self, window, display_manager, displayargs:dict):
		self.display_manager = display_manager
		if "data" in displayargs.keys():
			self.data = displayargs["data"]
		else:
			raise exceptions.QuizDataNotProvided

		self.win = window
		welcome_message = self.data.get_quiz_info("welcome-message")
		author = self.data.get_quiz_info("author")
		self.welcome_greeting = widgets.QuizWelcomeGreeting(self.win, welcome_message, "by: {}".format(author))
		self.welcome_greeting.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
		self.win.grid_columnconfigure(0, weight=1)

		description_label = CTkLabel(self.win, text="Description: ", text_font=("default", 16))
		description_label.grid(row=1, column=0, padx=30, sticky="nw")
		description = self.data.get_quiz_info("description")
		self.win.grid_rowconfigure(1, weight=0)

		self.description_l = widgets.WrappedLabel(self.win, text=description)
		self.description_l.grid(row=2, column=0, sticky="new", padx=40, pady=10)
		self.win.grid_rowconfigure(2, weight=1)

		self.start_button = CTkButton(self.win, text="Start", command=self.start_quiz)
		self.start_button.grid(row=3, column=0, padx=10, pady=10)

	def start_quiz(self):
		self.display_manager.jump_to_display(Displays.QUIZ_PAGE.value, data=self.data)

class QuizPage():
	def __init__(self, window, display_manager, displayargs:dict):
		self.display_manager = display_manager
		self.win = window

		if "data" in displayargs.keys():
			self.data = displayargs["data"]
		else:
			raise exceptions.QuizDataNotProvided

		self.question_count = self.data.get_quiz_info("question-count")
		self.organise = self.data.get_quiz_info("organise")

	def present_question():
		pass

	def next_question():
		pass

	def check_answer():
		pass
		
class QuizEnd():
	def __init__(self, window, display_manager, displayargs:dict):
		pass

DISPLAYS = [StartScreen, QuizWelcome, QuizPage, QuizEnd] #Constant with displays assigned to numbers