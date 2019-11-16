import os
import random

try:
    import local_settings.config as config
except ModuleNotFoundError:
    import prod_settings.config as config


def get_random_article():
    article_files = os.listdir(config.ARTICLES_PATH)
    article_file = random.choice(article_files)
    with open(os.path.join(config.ARTICLES_PATH, article_file), 'r') as f:
        article_text = f.read()
    return article_text
