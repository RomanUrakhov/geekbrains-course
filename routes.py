from flex_framework.template_manager import render_template

from repository import list_articles, list_courses, get_my_favourites


def index(request):
    articles = list_articles()
    return '200 OK', render_template('index.html', articles=articles)


def all_courses(request):
    courses = list_courses()
    return '200 OK', render_template('courses.html', courses=courses)


def advanced_courses(request):
    courses = list_courses(category='advanced')
    return '200 OK', render_template('courses.html', courses=courses)


def my_favourites(request):
    if request['authorized']:
        favourites = get_my_favourites()
        return '200 OK', render_template('favourites.html', favourites=favourites)
    return '403 Forbidden', 'Unauthorized error'


def extra_materials(request):
    print(request)
    return '200 OK', 'extra materials page'
