import exceptions
import json

class Quiz():
	str_info = ["name", "author", "welcome-message", "organise", "description"]
	int_info = ["question-count"]

	def __init__(self):
		self.data = None

	def load_from_file(self, file_name:str):
		file = open(file_name, "r")
		self.data = json.loads(file.read())
		file.close()

	def load_from_string(self, text:str):
		self.data = json.loads(text)

	def get_question(self, question_number):
		pass 

	def get_quiz_info(self, data):
		# is string
		if data in self.str_info:
			if data in self.data.keys():
				return self.data[data]
			else:
				return "Data not found: {}".format(data)
		# is int
		elif data in self.int_info:
			if data in self.data.keys():
				return self.data[data]
			else:
				return -1
		# raise exception if invalid keyword
		else:
			print("farts")
			raise QuizInfoRequestInvalid