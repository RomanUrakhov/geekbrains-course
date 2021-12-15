from flex_framework.template_manager import render_template
from flex_framework.request import BaseRequest

from repository import list_articles, list_courses, get_my_favourites


def index(request: BaseRequest):
    articles = list_articles()
    return '200 OK', render_template('index.html', articles=articles)


def all_courses(request: BaseRequest):
    courses = list_courses()
    return '200 OK', render_template('courses.html', courses=courses)


def advanced_courses(request: BaseRequest):
    courses = list_courses(category='advanced')
    return '200 OK', render_template('courses.html', courses=courses)


def my_favourites(request: BaseRequest):
    if request.headers.get('Custom-Authorized'):
        favourites = get_my_favourites()
        return '200 OK', render_template('favourites.html', favourites=favourites)
    return '403 Forbidden', 'Unauthorized error'


def extra_materials(request: BaseRequest):
    print(request)
    return '200 OK', 'extra materials page'


def feedback(request: BaseRequest):
    if request.method == 'GET':
        return '200 OK', render_template('feedback.html')
    elif request.method == 'POST':
        data = request.get_form_data()
        print(data)
        return '200 OK', render_template('feedback.html')
