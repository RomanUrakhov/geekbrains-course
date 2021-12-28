from abc import ABC, abstractmethod
from typing import List

from jsonpickle import dumps, loads

"""
Реализация стратегий логирования в консоль или в файл
"""


class ILogger(ABC):
    @abstractmethod
    def log(self, text):
        raise NotImplementedError


class ConsoleLogger(ILogger):
    def log(self, text):
        print(text)


class FileLogger(ILogger):
    def __init__(self, filename='log.log'):
        self.filename = filename

    def log(self, text):
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')


"""
Реализация Observer для оповещения о заполнении формы обратной связи
"""


class FeedbackNotifier(ABC):
    @abstractmethod
    def notify(self, feedback):
        raise NotImplementedError


class EmailNotifier(FeedbackNotifier):
    def notify(self, feedback):
        print(f'[MAIL NOTIFICATION]: you have new feedback from {feedback.email}')


class SmsNotifier(FeedbackNotifier):
    def notify(self, feedback):
        print(f'[SMS NOTIFICATION]: you have new feedback from {feedback.email}')


class NewFeedbackTopic:
    def __init__(self):
        self.observers: List[FeedbackNotifier] = []

    def notify(self, feedback):
        for obs in self.observers:
            obs.notify(feedback)


class JSONSerializer:
    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


