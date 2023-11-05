import base
from customtkinter import *
from customtkinter import CTkFont

class Text(base.QuestionType):
	required_info = {
		"case-sensitive": bool,
		"answer": str
	}

	default_values = {
		"case-sensitive": True,
		"answer": "undefined"
	}

	def __init__(self, info, point_callback):
		super().__init__()
		self.point_callback = point_callback
		self.data = info

	def create_input(self) -> None:
		self.input_var = StringVar()

		self.input_label = CTkLabel(self.widget, text=self.language_manager.get_language_word("enter-your-answer"))
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

type_class = Text