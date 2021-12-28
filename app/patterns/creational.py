from copy import deepcopy
from datetime import datetime
from typing import List

from app.patterns.behavioral import ConsoleLogger, ILogger, NewFeedbackTopic, SmsNotifier, EmailNotifier

"""
Singleton
"""


class Singleton(type):
    __instance = {}

    def __call__(cls, *args, **kwargs):
        name = ''
        if args:
            name = args[0]
        if kwargs and 'name' in kwargs:
            name = kwargs['name']
        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class FlexLogger(metaclass=Singleton):
    def __init__(self, name='root', logging_strategy: ILogger = ConsoleLogger()):
        self.__formatting = "[LOG {}]: {}"
        self.name = name
        self.logging_strategy = logging_strategy

    def log(self, text):
        formatted_text = self.__formatting.format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), text)
        self.logging_strategy.log(formatted_text)


"""
Prototype
"""


class MaterialPrototype:
    def clone(self):
        return deepcopy(self)


class Material(MaterialPrototype):
    def __init__(self, name, author, created, tags: list):
        self.name = name
        self.author = author
        self.created = created
        self.tags = tags
        for tag in tags:
            tag.materials.append(self)

    def __eq__(self, other):
        if isinstance(other, Material):
            return self.name == other.name and self.author == other.author
        return NotImplemented

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.name, self.author))


class Article(Material):
    pass


class Course(Material):
    pass


"""
Factory method
"""


class MaterialFactory:
    material_types = {
        'article': Article,
        'course': Course
    }

    @classmethod
    def create(cls, type_name, name, author, created, tags):
        material_type = cls.material_types.get(type_name)
        if not material_type:
            raise NotImplementedError
        return material_type(name, author, created, tags)


class Tag:
    def __init__(self, name):
        self.name = name
        self.materials = []

    def number_of_materials(self):
        result = len(self.materials)
        return result


class Feedback:
    def __init__(self, username, email, text):
        self.username = username
        self.email = email
        self.text = text


class FlexEngine(NewFeedbackTopic):
    def __init__(self):
        self.materials = []
        self.tags = []
        self.feedback_list: List[Feedback] = []
        super().__init__()

    def process_feedback(self, name, email, text):
        feedback = Feedback(name, email, text)
        self.feedback_list.append(feedback)
        self.notify(feedback)
        return feedback

    @staticmethod
    def create_tag(name):
        return Tag(name)

    def get_tag_by_name(self, name):
        for tag in self.tags:
            if tag.name == name:
                return tag
        return None

    @staticmethod
    def create_material(type_, name, author, created, tags: list) -> Material:
        return MaterialFactory.create(type_, name, author, created, tags)

    def get_material_by_name(self, name) -> Material:
        for material in self.materials:
            if material.name == name:
                return material
        return None

    def get_materials_by_tag(self, tag_name) -> list:
        tag = self.get_tag_by_name(name=tag_name)
        if not tag:
            return []
        return tag.materials
