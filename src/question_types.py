from customtkinter import *
from customtkinter import CTkFont
#from tkinter import *

class QuestionType():
	def assign_widget(self, widget):
		self.widget = widget

	def assign_language_manager(self, language_manager):
		self.language_manager = language_manager

	def destroy_input(self):
		try:
			widget_list =  self.widget.winfo_children()
			for item in widget_list:
				item.destroy()

		except:
			print("Error: the question holder", self.__name__, "was not assigned a widget.")

	def check_and_correct_info(self):
		#try:
		for info in self.data.keys():
			validity = False
			for i in self.required_info.keys():
				if info == i:
					validity = True
					break

			if validity == False:
				self.data[info] = self.default_values[info]

			# Check if correct type
			if type(self.data[info]) != self.required_info[info]:
				self.data[info] = self.default_values[info]
		"""except Exception as e:
			undef = "false"
			if hasattr(self, "data") == False:
				undef = "data"

			elif hasattr(self, "required_info") == False:
				undef = "required_info"

			else:
				undef = e
			print("In question type:", type(self).__name__, undef, "is not defined")"""

class Text(QuestionType):
	required_info = {
		"case-sensitive": bool,
		"answer": str,
		"main-text": str,
		"sub-text": str,
		"answer-type": str
	}

	default_values = {
		"case-sensitive": True,
		"answer": "undefined",
		"main-text": "Undefined",
		"sub-text": "Undefined",
		"answer-type": "Undefined"
	}

	def __init__(self, info, point_callback):
		self.point_callback = point_callback
		self.data = info

	def create_input(self) -> None:
		self.input_var = StringVar()

		self.input_label = CTkLabel(self.widget, text="Enter your answer: ")
		self.input = CTkEntry(self.widget, textvariable=self.input_var)
		self.input_label.grid(row=0, column=0, padx=10, pady=10)
		self.input.grid(row=1, column=0, padx=10, pady=10)
		self.total_length = 2

	def check_answer(self) -> str:
		result = ""
		if self.input_var.get() == self.data["answer"]:
			# Add points to total
			self.point_callback(1)
			result = self.language_manager.get_language_word("correct")

		else:
			self.point_callback(-1)
			result = self.language_manager.get_language_word("incorrect")

		self.correctness_label = CTkLabel(self.widget, text=result)
		self.correctness_label.grid(row=2, column=0)

class MultipleChoice(QuestionType):
	required_info = {
		"answer": int,
		"options": list
	}
	default_values = {
		"answer": 0,
		"options": ["Undefined"]
	}
	
	def __init__(self):
		pass

	def create_input(self):
		pass

	def check_answer(self) -> int:
		pass

	def destroy_input(self):
		pass

class TrueFalse(QuestionType):
	required_info = {
		"answer": list,
		"questions": list,
	}

	default_values = {
		"answer": [False],
		"questions": ["Undefined"]
	}
	
	def __init__(self):
		pass

	def create_input(self):
		pass

	# return the points to add
	def check_answer(self) -> int:
		pass

	def destroy_input(self):
		pass

QUESTION_TYPES = {
	"text": Text,
	"multiple-choice": MultipleChoice,
	"true-false": TrueFalse
}