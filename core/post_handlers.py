import settings
from .models import Post, db


def post_handler(name, readable):
    settings.POST_CATEGORIES[name] = {
        'readable': readable,
    }

    def resulting_func(func):
        settings.POST_CATEGORIES[name]['handler'] = func
        return func

    return resulting_func

@post_handler('remontka', 'Статьи Remontka.pro')
def posts_remontka():
    pass

@post_handler('bbc', 'Новости BBC')
def posts_bbc():
    pass

@post_handler('hell-0', 'Обновления сайта')
def posts_hello():
    post = Post(category='hell-0', data='Посты обновлены!')
    db.session.add(post)
    db.session.commit()