import exceptions
import json
import random

class Quiz():
	str_info = [
		"name", 
		"author", 
		"welcome-message", 
		"organise", 
		"description", 
		"goodbye-message", 
	]

	int_info = [
		"question-count",
		"required-question-count"
	]

	correct_string = "Correct!"
	incorrect_string = "Incorrect 😞"

	question_params = [
		"main-text",
		"sub-text",
		"answer-type",
		"answer",
		"case-sensitive"
	]

	default_question_values = {
		"main-text": "Undefined question",
		"sub-text": "Undefined question",
		"answer-type": "text",
		"answer": "undefined",
		"case-sensitive": False,
	}

	default_quiz_values = {
		"name": "Unspecified",
		"author":"Unspecified",
		"welcome-message": "welcome",
		"organise": "ordered",
		"description": "A FreeQuiz project",
		"goodbye_mesage": "Goodbye!",
		"question-count": 0,
		"required-question-count": -1
	}

	def __init__(self):
		self.data = None

	def load_from_file(self, file_name:str):
		with open(file_name, "r") as file:
			self.data = json.loads(file.read())
		self.validate_quiz()

	def load_from_string(self, text:str):
		self.data = json.loads(text)

		self.validate_quiz()

	def construct_quiz_timeline(self):
		organise = self.get_quiz_info("organise")
		question_count = self.get_quiz_info("question-count")

		self.quiz_timeline = [None] * question_count
		for i in range(0, question_count):
			self.quiz_timeline[i] = i
			
		if organise == "random":
			random.shuffle(self.quiz_timeline)

		self.current_question = 0
		self.correct_answer_count = 0
		self.wrong_answer_count = 0
		required = self.get_quiz_info("required-question-count")
		
		if required > 0:
			self.length = required

		else:
			self.length = len(self.quiz_timeline)

	def get_current_question(self):
		current_q_num = str(self.quiz_timeline[self.current_question])
		return self.data[current_q_num]

	def next_question(self) -> bool:
		print("called next_question")
		self.current_question += 1
		if self.current_question >= self.length:
			return True

		else:
			return False

	def check_and_count_answer(self, answer):
		answer = self.check_answer(answer)
		if answer == True:
			self.correct_answer_count += 1
			return self.correct_string
		else:
			self.wrong_answer_count += 1
			return self.incorrect_string
		
	def check_answer(self, answer:str) -> str:
		if not self.data[str(self.current_question)]["case-sensitive"]:
			mod_answer = answer.lower()
			mod_canswer = self.data[str(self.current_question)]["answer"].lower()

		else:
			mod_answer = answer
			mod_canswer = self.data[str(self.current_question)]["answer"]

		if mod_answer == mod_canswer:
			return True
		else:
			return False

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

	def validate_quiz(self):
		progress = 0
		for i in self.str_info:
			if i in self.data.keys():
				progress += 1

		for i in self.int_info:
			if i in self.data.keys():
				progress += 1

		for i in range(0, self.data["question-count"]):
			self.validate_and_correct_quiz_questions(i)

		self.validate_and_correct_quiz_info()

		if progress == len(self.str_info) + len(self.int_info):
			return True
		else:
			return False

	def validate_and_correct_quiz_questions(self, quesion_num):
		for i in self.question_params:
			if i not in self.data[str(quesion_num)].keys():
				self.data[str(quesion_num)][i] = self.default_question_values[i]

	def validate_and_correct_quiz_info(self):
		for i in self.str_info:
			if i not in self.data.keys():
				self.data[i] = self.default_quiz_values[i]

		for i in self.int_info:
			if i not in self.data.keys():
				self.data[i] = self.default_quiz_values[i]
