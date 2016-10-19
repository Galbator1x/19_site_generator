import os
import json

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from markdown import markdown


PATH_TO_CONFIG = 'config.json'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_config():
    if not os.path.exists(PATH_TO_CONFIG):
        return None
    with open(PATH_TO_CONFIG) as file_handle:
        return json.load(file_handle)


def get_filename_without_extention(path):
    return os.path.splitext(os.path.basename(path))[0]


def remove_old_articles(config):
    path_to_articles = 'templates'
    articles = os.listdir(path_to_articles)
    config_articles = get_html_articles_config(config)
    config_articles = [os.path.basename(article['source']) for article in config_articles]
    for article in articles:
        if article not in config_articles and not article.startswith('base'):
            os.remove(os.path.join(path_to_articles, article))


def get_html_articles_config(config):
    articles = config['articles']
    for article in articles:
        filename = get_filename_without_extention(article['source'])
        output_path = os.path.join('templates', '{}.html'.format(filename))
        article['source'] = output_path
    return articles


def generate_site(config):
    path_to_templates = 'templates'
    env = Environment()
    env.loader = FileSystemLoader(path_to_templates)

    for article in config['articles']:
        path_to_article = os.path.join('articles', article['source'])
        with open(path_to_article) as file_handle:
            file = file_handle.read()
            md = markdown(file)
            md = ''.join(('{% extends "base_page.html" %}{% block article %}',
                          md,
                          '{% endblock %}'))

        template = env.from_string(md)
        template = template.render(title=article['title'])

        filename = get_filename_without_extention(path_to_article)
        output_path = os.path.join(path_to_templates, '{}.html'.format(filename))
        article['source'] = output_path
        with open(output_path, 'w') as file_handle:
            file_handle.write(template)

    template_path = 'base_index.html'
    template = env.get_template(template_path)
    template = template.render(topics=config['topics'],
                               articles=get_html_articles_config(config))
    index_out_path = 'index.html'
    with open(index_out_path, 'w') as file_handle:
        file_handle.write(template)


if __name__ == '__main__':
    config = load_config()
    if config is None:
        exit(1)

    generate_site(config)
    remove_old_articles(config)
