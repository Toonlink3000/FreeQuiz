
class QuizDataNotProvided(Exception):
	def __str__(self):
		return "Quiz data provided to quiz object is invalid."

class QuizInfoRequestInvalid(Exception):
	def __str__(self):
		return "Quiz info keyword provided to quiz object is invalid"