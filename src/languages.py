import json
import os

class LanguageManager():
    language_keys = [
        "open-quiz", 
        "quit", 
        "description", 
        "by:", 
        "start", 
        "enter-your-answer", 
        "submit",
        "next-question",
        "correct",
        "incorrect",
        "correct-answers",
        "incorrect-answers",
        "main-menu",
    ]

    def __init__(self):
        self.languages = {}
        self.load_and_add_language("default", os.path.dirname(__file__)+"/languages/default.json")

        self.set_language("default")

    def load_and_add_language(self, language_name:str, language_file:str):
        with open(language_file, "r") as file:
            self.languages[language_name] = json.load(file)

    def set_language(self, language_name:str):
        self.current_language = language_name

    def get_language_word(self, word:str):
        return self.languages[self.current_language][word]

    def validate_language(self, language_name:str):
        progress = 0
        
        for i in self.language_keys:
            if i in self.languages[language_name]:
                progress += 1

        if progress == len(self.language_keys):
            return True

        else:
            return False