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
import logging
import themes

LANGUAGE_MANAGER = languages.LanguageManager()

class Displays(enum.Enum):
	START_SCREEN = 0
	QUIZ_WELCOME = 1
	QUIZ_PAGE = 2
	QUIZ_END = 3
	OPTIONS_MENU = 4

class DisplayManager():
	def __init__(self, window):
		self.current_display = 0
		self.window = window
		self.theme_manager = themes.ThemeManager()

	def jump_to_display(self, display:int, **displayargs):
		last_display = self.current_display
		self.current_display = display
		self.open_display = None
		self.clear_window()
		try:
			self.open_display = DISPLAYS[self.current_display](self.window, self, displayargs)
		except exceptions.QuizDataNotProvided:
			showerror("QuizDataNotProvided Error", "Quiz data was not provided to the display: {} from diplay {}".format(Displays(display).name, Displays(last_display).name))
			sys.exit()
	def clear_window(self):
		widget_list =  self.window.winfo_children()
		for item in widget_list:
			item.destroy()

class StartScreen():
	def __init__(self, window, display_manager, displayargs:dict):
		self.control_buttons = widgets.ControlButtons(
			window, self.open_quiz, LANGUAGE_MANAGER.get_language_word("open-quiz"), LANGUAGE_MANAGER.get_language_word("quit")
		)
		self.control_buttons.grid(row=2, column=0, pady=50)
		self.title_text = CTkLabel(window, text="FreeQuiz", font=("default", -70))
		self.title_text.grid(row=0, column=0, pady=50)

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
			logging.error("Quiz data was not provided to the display: {}".format(Displays(self.display_manager.current_display).name))
			sys.exit()

		self.win = window
		welcome_message = self.data.get_quiz_info("welcome-message")
		author = self.data.get_quiz_info("author")
		self.welcome_greeting = widgets.QuizWelcomeGreeting(
			self.win, welcome_message, LANGUAGE_MANAGER.get_language_word("by:").format(author)
		)

		self.welcome_greeting.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
		self.win.grid_columnconfigure(0, weight=1)

		description_label = CTkLabel(
			self.win, text=LANGUAGE_MANAGER.get_language_word("description"), font=("default", 16)
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
			logging.error("Quiz data was not provided to the display: {}".format(Displays(self.display_manager.current_display).name))
			sys.exit()
			
		self.data.construct_quiz_timeline()

		self.present_question()

	def present_question(self):
		self.question = self.data.get_current_question()
		self.question.assign_language_manager(LANGUAGE_MANAGER)
		
		self.question_header = widgets.QuestionHeader(self.win, self.question.data["main-text"], self.question.data["sub-text"])
		self.question_header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
		self.win.grid_columnconfigure(0, weight=1)
			
		self.question_input = widgets.QuestionInput(self.win, self.question)
		self.question_input.grid(row=1, column=0)
		self.question_input.draw_answer_box()
		self.win.grid_rowconfigure(1, weight=1)

		self.submit_button_t = StringVar()
		self.submit_button_t.set(LANGUAGE_MANAGER.get_language_word("submit"))
		self.submit_button = CTkButton(self.win, textvariable=self.submit_button_t, command=self.submit_answer)
		self.submit_button.grid(row=2, column=0, pady=10)
		self.win.grid_rowconfigure(2, weight=0)

	def submit_answer(self):
		self.question_input.draw_iscorrect()
		self.submit_button_t.set(LANGUAGE_MANAGER.get_language_word("next-question"))
		self.submit_button.configure(command = self.next_question)

	def next_question(self):
		last_question = self.data.next_question()
		if last_question == True:
			self.display_manager.jump_to_display(Displays.QUIZ_END.value, data=self.data)
			return

		self.refresh_question()

	def refresh_question(self):
		self.question.destroy_input()

		self.question = self.data.get_current_question()
		self.question.assign_widget(self)

		self.question_header.refresh_texts(self.question.data["main-text"], self.question.data["sub-text"])
		self.question_input.refresh_input(self.question.data["answer-type"])

		self.submit_button_t.set(LANGUAGE_MANAGER.get_language_word("submit"))
		self.submit_button.configure(command=self.submit_answer)

class QuizEnd():
	def __init__(self, window, display_manager, displayargs:dict):
		self.win = window
		self.display_manager = display_manager
		try:
			self.data = displayargs["data"]

		except:
			logging.error("Quiz data was not provided to the display: {}".format(Displays(self.display_manager.current_display).name))
			sys.exit()

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
		
class OptionsMenu():
	def __init__(self, window, display_manager, displayargs:dict):
		self.win = window
		self.display_manager = display_manager

		lang = [
			LANGUAGE_MANAGER.get_language_word("options-language"),
			LANGUAGE_MANAGER.get_current_language()
		]
		lang.extend(LANGUAGE_MANAGER.get_all_languages())

		theme = [
			LANGUAGE_MANAGER.get_language_word("options-theme"),
			self.display_manager.theme_manager.theme, 
		]
		theme.extend(self.display_manager.theme_manager.available_themes)

		accent = [
			LANGUAGE_MANAGER.get_language_word("options-accent-colour"),
			self.display_manager.theme_manager.accent_colour,
		]
		accent.extend(self.display_manager.theme_manager.available_accent_colours)

		self.options_menu = widgets.OptionsMenu(self.win, lang, theme, accent)
		self.options_menu.grid(row = 1, column=0, )
		self.save_button = CTkButton(
			self.win, text=LANGUAGE_MANAGER.get_language_word("save"), command=self.save
		)
		self.save_button.grid(row=2, column=0)
		self.exit_button = CTkButton(
			self.win, text=LANGUAGE_MANAGER.get_language_word("exit"), command=self.exit
		)
		self.save_button.grid(row=2, column=1)

	def save(self):
		self.display_manager.jump_to_display(Displays.START_SCREEN.value)

	def exit(self):
		self.display_manager.jump_to_display(Displays.START_SCREEN.value)

DISPLAYS = [StartScreen, QuizWelcome, QuizPage, QuizEnd, OptionsMenu] #Constant with displays assigned to numbers