import json
import os
import logging
import locale

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
        "save",
        "exit",

        "options-title",
        "options-language",
        "options-theme",
        "options-theme-light",
        "options-theme-dark",
        "options-theme-system",
        "options-accent-colour"
        "options-accent-colour-blue",
        "options-accent-colour-green",
    ]

    available_languages = {}

    def __init__(self):
        self.languages = {}
        self.scan_languages(os.path.dirname(__file__) + "/languages")
        self.set_language("default")

    def scan_languages(self, directory:str):
        for i in os.listdir(directory):
            if i.endswith(".json"):
                self.load_language_to_list(i[:-5], directory+"/"+i)

    def load_language_to_list(self, language_name:str, language_file:str):
        self.available_languages[language_name] = language_file
        print(language_name)

    def load_and_add_language(self, language_name:str):
        try:
            with open(self.available_languages[language_name], "r") as file:
                self.languages[language_name] = json.load(file)

        except Exception as e:
            logging.error("Failed to load language: " + language_name)
            logging.error(e)

    def set_language(self, language_name:str):
        if language_name in self.available_languages.keys():
            self.current_language = language_name
            self.load_and_add_language(language_name)

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

    def get_all_languages(self):
        return self.languages.keys()

    def get_current_language(self):
        return self.current_language