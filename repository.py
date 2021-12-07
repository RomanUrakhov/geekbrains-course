from typing import List
from datetime import date


def list_articles() -> List[dict]:
    return [
        {
            'id': 'A',
            'name': 'Data Visualization Interfaces in Python With Dash',
            'created_date': date(2021, 11, 30)
        },
        {
            'id': 'B',
            'name': 'Python Community Interview With Eric Wastl',
            'created_date': date(2021, 11, 22)
        },
        {
            'id': 'C',
            'name': 'Securely Deploy a Django App With Gunicorn, Nginx, & HTTPS',
            'created_date': date(2021, 11, 15)
        }
    ]


def list_courses(category='all') -> List[dict]:
    courses = [
        {
            'id': 'D',
            'name': 'Writing Idiomatic Python',
            'category': 'beginner',
            'author': 'Martin Breuss',
            'videos': [
                {
                    'id': 'E',
                    'name': 'Writing Idiomatic Python (Overview)',
                    'duration': 5
                },
                {
                    'id': 'F',
                    'name': 'The Zen of Python',
                    'duration': 1.42
                }
            ]
        },
        {
            'id': 'G',
            'name': 'Pass by Reference in Python: Best Practices',
            'category': 'advanced',
            'author': 'Howard Francis',
            'videos': [
                {
                    'id': 'H',
                    'name': 'Pass by Reference in Python: Best Practices (Overview)',
                    'duration': 2.58
                },
                {
                    'id': 'I',
                    'name': 'Parameter Passing',
                    'duration': 3.53
                }
            ]
        },
        {
            'id': 'J',
            'name': 'Using the Python return Statement Effectively',
            'category': 'beginner',
            'author': 'Howard Francis',
            'videos': [
                {
                    'id': 'K',
                    'name': 'Using the Python return Statement Effectively',
                    'duration': 1.17
                },
                {
                    'id': 'L',
                    'name': 'Reviewing Python Functions',
                    'duration': 2.46
                },
                {
                    'id': 'M',
                    'name': 'Using Implicit Returns in Functions',
                    'duration': 3.15
                }
            ]
        },
    ]
    return courses if category == 'all' else [course for course in courses if course['category'] == category]


def get_my_favourites():
    return [
        {'id': 'C', 'name': 'Securely Deploy a Django App With Gunicorn, Nginx, & HTTPS'},
        {'id': 'J', 'name': 'Using the Python return Statement Effectively'}
    ]
