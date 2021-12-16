from flex_framework.template_manager import render_template
from flex_framework.request import BaseRequest

from repository import list_articles, list_courses, get_my_favourites


def index(request: BaseRequest):
    materials = {'articles': list_articles(), 'courses': list_courses()}
    return '200 OK', render_template('index.html', materials=materials)


def all_courses(request: BaseRequest):
    courses = list_courses()
    return '200 OK', render_template('courses.html', category='all', additional_categories=['advanced'],
                                     courses=courses)


def advanced_courses(request: BaseRequest):
    category = 'advanced'
    courses = list_courses(category=category)
    return '200 OK', render_template('courses.html', category=category, courses=courses)


def articles(request: BaseRequest):
    articles = list_articles()
    return '200 OK', render_template('articles.html', articles=articles)


def my_favourites(request: BaseRequest):
    if request.headers.get('Custom-Authorized'):
        favourites = get_my_favourites()
        return '200 OK', render_template('favourites.html', favourites=favourites)
    return '403 Forbidden', 'Unauthorized error'


def feedback(request: BaseRequest):
    if request.method == 'GET':
        return '200 OK', render_template('feedback.html')
    elif request.method == 'POST':
        data = request.get_form_data()
        print(data)
        return '200 OK', render_template('feedback.html')
