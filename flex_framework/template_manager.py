from jinja2 import FileSystemLoader
from jinja2.environment import Environment


# TODO: сделать поиск папки templates независимым от ее вложенности в другие папки (например, app/templates)
def render_template(name, folder='app/templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(searchpath=folder)
    raw_template = env.get_or_select_template(name)
    return raw_template.render(**kwargs)
