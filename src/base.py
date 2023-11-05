GLOBAL_QUESTION_INFO = {
	"main-text": str,
	"sub-text": str,
	"answer-type": str
}
GLOBAL_DEFAULT_INFO = {
	"main-text": "Undefined",
	"sub-text": "Undefined",
	"answer-type": "Undefined"
}

class QuestionType():
	def __init__(self):
		self.required_info.update(GLOBAL_QUESTION_INFO)
		self.default_values.update(GLOBAL_DEFAULT_INFO)

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