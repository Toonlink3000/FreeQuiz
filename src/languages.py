import json
import os
import logging

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
        self.scan_languages(os.path.dirname(__file__) + "/languages")
        self.set_language("default")

        self.set_language("default")

    def scan_languages(self, directory:str):
        for i in os.listdir(directory):
            if i.endswith(".json"):
                self.load_and_add_language(i[:-5], directory+"/"+i)

    def load_and_add_language(self, language_name:str, language_file:str):
        try:
            with open(language_file, "r") as file:
                self.languages[language_name] = json.load(file)

        except Exception as e:
            logging.error("Failed to load language: " + language_name)
            logging.error(e)

    def set_language(self, language_name:str):
        if language_name in self.languages.keys():
            self.current_language = language_name

        else:
            logging.error("Language not found: " + language_name)

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