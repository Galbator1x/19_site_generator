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


def get_path_to_article_html(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    return os.path.join('templates', '{}.html'.format(filename))


def get_articles_config_with_html_paths(config):
    articles = config['articles']
    for article in config['articles']:
        article['source'] = get_path_to_article_html(article['source'])
    return articles


def remove_old_articles(config):
    path_to_articles = 'templates'
    articles = os.listdir(path_to_articles)
    config_articles = get_articles_config_with_html_paths(config)
    config_articles = [os.path.basename(article['source']) for article in config_articles]
    for article in articles:
        if article not in config_articles and not article.startswith('base'):
            os.remove(os.path.join(path_to_articles, article))


def load_file(path):
    with open(path) as file_handle:
        return file_handle.read()


def save_template(template, path):
    with open(path, 'w') as file_handle:
        file_handle.write(template)


def render_article_template(markdown, env, **kwargs):
    markdown = ''.join(('{% extends "base_page.html" %}{% block article %}',
                        markdown,
                        '{% endblock %}'))
    template = env.from_string(markdown)
    return template.render(kwargs)


def render_index_template(path, env, **kwargs):
    template = env.get_template(path)
    return template.render(kwargs)


def generate_site(config):
    path_to_templates = 'templates'
    path_to_articles = 'articles'
    index_path = 'base_index.html'
    index_out_path = 'index.html'
    env = Environment()
    env.loader = FileSystemLoader(path_to_templates)

    for article in config['articles']:
        path_to_article = os.path.join(path_to_articles, article['source'])
        md = load_file(path_to_article)
        template = markdown(md)
        template = render_article_template(template, env, title=article['title'])
        save_template(template, get_path_to_article_html(path_to_article))

    template = render_index_template(index_path, env, topics=config['topics'],
                                     articles=get_articles_config_with_html_paths(config))
    save_template(template, index_out_path)


if __name__ == '__main__':
    config = load_config()
    if config is None:
        print('config.json does not exists.')
        exit(1)

    generate_site(config)
    remove_old_articles(config)
