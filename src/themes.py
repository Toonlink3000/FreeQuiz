import customtkinter

class ThemeManager():
	available_themes = [
		"system"
		"dark"
		"light"
	]

	available_accent_colours = [
		"blue",
		"dark-blue",
		"green"
	]
	
	def __init__(self):
		self.theme = "system"
		self.accent_colour = "blue"

	def set_theme(self, theme="system", accent="blue"):
		self.theme = theme
		self.accent_colour = accent
		customtkinter.set_appearance_mode(theme)
		customtkinter.set_default_color_mode(accent)
