import qtype_base
from customtkinter import *
from customtkinter import CTkFont

class MultipleChoice(base.QuestionType):
	required_info = {
		"answer": int,
		"options": list
	}

	default_values = {
		"answer": 0,
		"options": ["Undefined"]
	}

	def __init__(self, info, point_callback):
		super().__init__()
		self.point_callback = point_callback
		self.data = info

	def create_input(self) -> None:
		self.input_var = StringVar()
		options = self.data["options"]

		#create a list of radio buttons for each option
		self.input_label = CTkLabel(self.widget, text=self.language_manager.get_language_word("enter-your-answer"))
		self.input_label.grid(row=0, column=0, padx=10, pady=10)
		self.input = []
		for i, option in enumerate(options):
			self.input.append(CTkRadioButton(self.widget, text=option, variable=self.input_var, value=option))
			self.input[i].grid(row=i+1, column=0, padx=10, pady=10, sticky="w")

		self.total_length = len(options) + 1

	def check_answer(self) -> str:
		if self.input_var.get() == self.data["answer"]:
			# Add points to total
			self.point_callback(1)
			result = self.language_manager.get_language_word("correct")

		else:
			self.point_callback(-1)
			result = self.language_manager.get_language_word("incorrect")

		self.correctness_label = CTkLabel(self.widget, text=result)
		self.correctness_label.grid(row=2, column=0)

type_class = MultipleChoice