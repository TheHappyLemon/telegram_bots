from exceptions import *
from json import load as jLoad

class Lang_class:
    def __init__(self):
        # language_lsit = {'EN' : 'path_to_EN_json'}
        self.language_list = []
        self.languages = {}

    def initialize(self, languages : list):
        self.language_list = languages
        self.__load_all__()

    def __str__(self):
        return f"Lang_class!\nlanguages_list={str(self.language_list)}\nlanguages={str(self.languages)}"

    def __load_all__(self):
        if len(self.language_list) == 0:
            raise NoLanguageFound
        for lang in self.language_list:
            self.load(lang, self.language_list[lang])

    def load(self, lang : str, path : str, force_reload : bool = False):
        if lang not in self.languages or force_reload:
            with open(path, 'r') as file:
                data = jLoad(file)
                self.languages[lang] = data

    def reload(self, lang : str, path : str):
        self.load(lang, path, True)

    def get_text(self, language : str, path : str):
        if language not in self.language_list:
            raise LanugageNotSupported
        if self.languages == {}:
            raise NoLanguageFound
        current = self.languages[language]
        keys = path.split('.')
        try:
            for key in keys:
                current = current[key]
            return current
        except KeyError:
            # Lol?
            raise PhraseNotFound

# language instance
global lang_instance
lang_instance = Lang_class()

# notification options. Make them global, so they are calculated once a day
global day_0
global day_1
global day_2
global day_3
global week_1
global week_2
global month_1
