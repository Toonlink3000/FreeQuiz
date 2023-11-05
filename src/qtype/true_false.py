import qtype_base
from customtkinter import *
from customtkinter import CTkFont

#TODO
class TrueFalse(base.QuestionType):
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

type_class = TrueFalse