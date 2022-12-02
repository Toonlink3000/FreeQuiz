from customtkinter import *
from tkinter import messagebox
import traceback
import displays


class App(CTk):
	def __init__(self):
		super().__init__()
		self.title("FreeQuiz")
		self.display_manager = displays.DisplayManager(self)
		self.display_manager.jump_to_display(0)

class Quiz():
	def __init__(self, win, quiz_data, display_manager):
		self.win = win
		self.data = quiz_data
		self.display_manager = display_manager

	def display_welcome(self):
		pass

	def start_quiz(self): #testinfg
		self.clear_window()

def main():
	try:
		app = App()
		app.mainloop()

	except:
		messagebox.showerror("Caught error",traceback.format_exc())

if __name__ == '__main__':
	main()