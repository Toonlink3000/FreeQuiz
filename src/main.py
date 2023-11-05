from customtkinter import *
from tkinter import messagebox
import traceback
import displays
import argparse
import question_types

parser = argparse.ArgumentParser(description="FreeQuiz")
parser.add_argument("-l", "--language", help="Set the language of the program", default="default")
args = parser.parse_args()


class App(CTk):
	def __init__(self):
		super().__init__()
		self.geometry("640x480")
		displays.LANGUAGE_MANAGER.set_language(args.language)
	
		self.title("FreeQuiz")
		self.display_manager = displays.DisplayManager(self)
		self.display_manager.jump_to_display(0)

def main():
		#scan question types
		question_types.scan_type_plugins()

		app = App()
		app.mainloop()

if __name__ == '__main__':
	print(get_appearance_mode())
	main()
