import exceptions
import json
import random

class Quiz():
	str_info = ["name", "author", "welcome-message", "organise", "description"]
	int_info = ["question-count"]

	correct_string = "Correct!"
	incorrect_string = "Incorrect 😞"

	def __init__(self):
		self.data = None

	def load_from_file(self, file_name:str):
		file = open(file_name, "r")
		self.data = json.loads(file.read())
		file.close()

	def load_from_string(self, text:str):
		self.data = json.loads(text)

	def construct_quiz_timeline(self):
		organise = self.get_quiz_info("organise")
		question_count = self.get_quiz_info("question-count")

		self.quiz_timeline = [None] * question_count
		for i in range(0, question_count):
			self.quiz_timeline[i] = i
			
		if organise == "random":
			self.quiz_timeline = random.choice(self.quiz_timeline)

		self.current_question = 0
		self.correct_answer_count = 0
		self.wrong_answer_count = 0

	def get_current_question(self):
		current_q_num = str(self.quiz_timeline[self.current_question])
		return self.data[current_q_num]

	def next_question(self) -> bool:
		self.current_question += 1
		if self.current_question == len(self.quiz_timeline):
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
		if answer == self.data[str(self.current_question)]["answer"]:
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
			raise QuizInfoRequestInvalid