from datetime import datetime

from app import app, logger
from app.patterns.behavioral import EmailNotifier, SmsNotifier, JSONSerializer
from app.patterns.structural import profile
from flex_framework.template_manager import render_template
from flex_framework.request import BaseRequest
from app.patterns.creational import FlexEngine

from app.repository import list_articles, list_courses, get_my_favourites

engine = FlexEngine()

sms_notifier = SmsNotifier()
email_notifier = EmailNotifier()
engine.observers.extend([sms_notifier, email_notifier])


@app.route('/')
@profile
def index(request: BaseRequest):
    logger.log('Open index page')
    return '200 OK', render_template('index.html', materials=engine.materials)


@app.route('/courses/')
@app.route('/courses/all')
def all_courses(request: BaseRequest):
    courses = list_courses()
    return '200 OK', render_template('courses.html', category='all', additional_categories=['advanced'],
                                     courses=courses)


@app.route('/courses/advanced')
def advanced_courses(request: BaseRequest):
    category = 'advanced'
    courses = list_courses(category=category)
    return '200 OK', render_template('courses.html', category=category, courses=courses)


@app.route('/articles/')
def articles(request: BaseRequest):
    articles = list_articles()
    return '200 OK', render_template('articles.html', articles=articles)


@app.route('/favourites/')
def my_favourites(request: BaseRequest):
    if request.headers.get('Custom-Authorized'):
        favourites = get_my_favourites()
        return '200 OK', render_template('favourites.html', favourites=favourites)
    return '403 Forbidden', 'Unauthorized error'


@app.route('/feedback/')
def feedback(request: BaseRequest):
    if request.method == 'GET':
        return '200 OK', render_template('feedback.html')
    elif request.method == 'POST':
        data = request.get_form_data()
        engine.process_feedback(name=data['name'], email=data['email'], text=data['message'])
        return '200 OK', render_template('feedback.html')


@app.route('/tags/')
def tags(request: BaseRequest):
    if request.method == 'GET':
        return '200 OK', render_template('tags.html', tags=engine.tags)
    elif request.method == 'POST':
        form_data = request.get_form_data()
        tag_name = form_data['name']
        existing_tag = engine.get_tag_by_name(tag_name)
        if not existing_tag:
            tag = engine.create_tag(tag_name)
            engine.tags.append(tag)
        return '200 OK', render_template('tags.html', tags=engine.tags)


@app.route('/add-material/')
def add_material(request: BaseRequest):
    if request.method == 'GET':
        return '200 OK', render_template('add_material.html', tags=engine.tags)
    elif request.method == 'POST':
        form_data = request.get_form_data()
        if 'name' not in form_data or 'author' not in form_data or 'material_type' not in form_data:
            return '400 BAD REQUEST', 'Not all fields are provided'
        material_type = form_data.get('material_type')
        name = form_data['name']
        author = form_data['author']
        created = datetime.now()
        tags_name_list = form_data.get('tags', [])
        # TODO: придумать как переписать get_form_data для парсинга multiple полей формы (например, tags)
        tags_name_list = [tags_name_list] if not isinstance(tags_name_list, list) else tags_name_list
        related_tags = []
        for tag_name in tags_name_list:
            tag = engine.get_tag_by_name(name=tag_name)
            related_tags.append(tag)
        material = engine.create_material(material_type, name, author, created, related_tags)
        engine.materials.append(material)
        return '200 OK', render_template('index.html', materials=engine.materials)


@app.route('/copy-material/')
def copy_material(request: BaseRequest):
    material_name = request.args.get('name')
    if material_name:
        material = engine.get_material_by_name(material_name)
        new_name = f"copy of {material.name}"
        new_material = material.clone()
        new_material.name = new_name
        engine.materials.append(new_material)
        return '200 OK', render_template('index.html', materials=engine.materials)
    return '400 BAD REQUEST', "Can't copy material without specifying a source 'name'"


@app.route('/materials/')
def material_list(request: BaseRequest):
    material_tags = request.args.get('tags')
    if material_tags:
        material_tags = material_tags.split(',')
        related_materials = []
        for tag in material_tags:
            related_materials.extend(engine.get_materials_by_tag(tag_name=tag))
        related_materials = list(set(related_materials))
    else:
        material_tags = []
        related_materials = engine.materials
    return '200 OK', render_template('materials.html', related_tags=material_tags, materials=related_materials)


@app.route('/api/feedback/')
def json_data(request: BaseRequest):
    feedback_list = engine.feedback_list
    return '200 OK', JSONSerializer(feedback_list).save()
