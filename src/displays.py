from customtkinter import *
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import random
import widgets
import sys
import json
import enum
import exceptions
import quiz
import languages

LANGUAGE_MANAGER = languages.LanguageManager()

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
		self.welcome_greeting = widgets.QuizWelcomeGreeting(
			self.win, welcome_message, LANGUAGE_MANAGER.get_language_word("by:").format(author)
		)

		self.welcome_greeting.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
		self.win.grid_columnconfigure(0, weight=1)

		description_label = CTkLabel(
			self.win, text=LANGUAGE_MANAGER.get_language_word("description"), text_font=("default", 16)
		)

		description_label.grid(row=1, column=0, padx=30, sticky="nw")
		description = self.data.get_quiz_info("description")
		self.win.grid_rowconfigure(1, weight=0)

		self.description_l = widgets.WrappedLabel(self.win, text=description)
		self.description_l.grid(row=2, column=0, sticky="new", padx=40, pady=10)
		self.win.grid_rowconfigure(2, weight=1)

		self.start_button = CTkButton(
			self.win, text=LANGUAGE_MANAGER.get_language_word("start"), command=self.start_quiz
		)

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

		self.data.construct_quiz_timeline()

		self.present_question()

	def present_question(self):
		self.question = self.data.get_current_question()
		self.question_header = widgets.QuestionHeader(self.win, self.question["main-text"], self.question["sub-text"])
		self.question_header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
		self.win.grid_columnconfigure(0, weight=1)

		if self.question["answer-type"] == "multiple-choice":
			options = self.question["options"]
		
		elif self.question["answer-type"] == "text":
			options = None
			
		self.question_input = widgets.QuestionInput(self.win, self.question["answer-type"], options)
		self.question_input.grid(row=1, column=0)
		self.win.grid_rowconfigure(1, weight=1)

		self.submit_button_t = StringVar()
		self.submit_button_t.set(LANGUAGE_MANAGER.get_language_word("submit"))
		self.submit_button = CTkButton(self.win, textvariable=self.submit_button_t, command=self.submit_answer)
		self.submit_button.grid(row=2, column=0, pady=10)
		self.win.grid_rowconfigure(2, weight=0)

	def submit_answer(self):
		correctness = self.data.check_and_count_answer(self.question_input.answer.get())

		self.question_input.draw_iscorrect(correctness)
		self.submit_button_t.set(LANGUAGE_MANAGER.get_language_word("next-question"))
		self.submit_button.configure(command = self.next_question)

	def next_question(self):
		last_question = self.data.next_question()
		if last_question == True:
			self.display_manager.jump_to_display(Displays.QUIZ_END.value, data=self.data)
			return

		self.refresh_question()

	def refresh_question(self):
		self.question = self.data.get_current_question()

		if self.question["answer-type"] == "multiple-choice":
			options = self.question["options"]
		
		elif self.question["answer-type"] == "text":
			options = None
			
		self.question_header.refresh_texts(self.question["main-text"], self.question["sub-text"])
		self.question_input.refresh_input(self.question["answer-type"], options)

		self.submit_button_t.set(LANGUAGE_MANAGER.get_language_word("submit"))
		self.submit_button.configure(command=self.submit_answer)

class QuizEnd():
	def __init__(self, window, display_manager, displayargs:dict):
		self.win = window
		self.display_manager = display_manager
		self.data = displayargs["data"]

		self.quiz_goodbye = widgets.QuizGoodbye(self.win, self.data.get_quiz_info("goodbye-message"))
		self.quiz_goodbye.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
		self.win.grid_columnconfigure(0, weight=1)
		self.win.grid_rowconfigure(0, weight=0)

		self.correct_anwers = CTkLabel(
			self.win, text=LANGUAGE_MANAGER.get_language_word("correct-answers").format(self.data.correct_answer_count)
		)
		self.correct_anwers.grid(row=1, column=0, padx=30, pady=5, sticky="nw")
		self.win.grid_rowconfigure(1, weight=0)

		self.incorrect_answers = CTkLabel(
			self.win, text=LANGUAGE_MANAGER.get_language_word("incorrect-answers").format(self.data.wrong_answer_count)
		)
		self.incorrect_answers.grid(row=2, column=0, padx=30, pady=5, sticky="nw")
		self.win.grid_rowconfigure(2, weight=0)

		self.win.grid_rowconfigure(3, weight=1)

		self.main_menu_button = CTkButton(
			self.win, text=LANGUAGE_MANAGER.get_language_word("main-menu"), command=self.return_to_main_menu
		)
		self.main_menu_button.grid(row=4, column=0, padx=10, pady=10)
		
	def return_to_main_menu(self):
		self.display_manager.jump_to_display(Displays.START_SCREEN.value)
		
DISPLAYS = [StartScreen, QuizWelcome, QuizPage, QuizEnd] #Constant with displays assigned to numbers