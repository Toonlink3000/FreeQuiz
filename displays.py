from customtkinter import *
from tkinter import *


class DisplayManager():
	def __init__(self, window):
		self.current_display = 0
		self.window = window

	def jump_to_display(self, display:int, **displayargs):
		self.clear_window()
		DISPLAYS[self.current_display](display, displayargs)


	def clear_window(self):
		widget_list =  self.window.winfo_children()
		for item in widget_list:
			item.destroy()

class StartScreen():
	def __init__(self, window, displayargs:dict):
		pass

class QuizWelcome():
	def __init__(self, window, displayargs:dict):
		pass

class QuizPage():
	def __init__(self, window, displayargs:dict):
		pass
		
class QuizEnd():
	def __init__(self, window, displayargs:dict):
		pass

DISPLAYS = [StartScreen, QuizWelcome, QuizPage, QuizEnd] #Constant with displays assigned to numbers