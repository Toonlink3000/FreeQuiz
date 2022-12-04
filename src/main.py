from customtkinter import *
from tkinter import messagebox
import traceback
import displays
import argparse

parser = argparse.ArgumentParser(description="FreeQuiz")
parser.add_argument("-l", "--language", help="Set the language of the program", default="default")
args = parser.parse_args()


class App(CTk):
	def __init__(self):
		super().__init__()
		displays.LANGUAGE_MANAGER.set_language(args.language)
	
		self.title("FreeQuiz")
		self.display_manager = displays.DisplayManager(self)
		self.display_manager.jump_to_display(0)

def main():
		app = App()
		app.mainloop()

if __name__ == '__main__':
	main()
