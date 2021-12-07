from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render_template(name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(searchpath=folder)
    raw_template = env.get_template(name=name)
    return raw_template.render(**kwargs)


