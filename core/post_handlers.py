import html
import re
import feedparser
import settings
from .models import Post, db


def post_handler(name, readable):
    settings.POST_CATEGORIES[name] = {'readable': readable}

    def resulting_func(func):
        settings.POST_CATEGORIES[name]['handler'] = func
        return func

    return resulting_func


def _already_exists(category, link):
    return db.session.query(
        Post.query.filter_by(category=category).filter(Post.data.contains(link)).exists()
    ).scalar()


def _fetch_rss(url, category, limit=10):
    feed = feedparser.parse(url)
    added = 0
    for entry in feed.entries[:limit]:
        title = entry.get('title', '').strip()
        link = entry.get('link') or entry.get('id', '')
        summary = entry.get('summary', '').strip()

        if not link or _already_exists(category, link):
            continue

        data = f'**[{title}]({link})**'
        if summary:
            clean = re.sub(r'<[^>]+>', '', html.unescape(summary)).strip()
            if clean:
                data += f'\n\n{clean[:300]}'

        post = Post(category=category, data=data)
        db.session.add(post)
        added += 1

    if added:
        db.session.commit()


@post_handler('bbc', 'Новости BBC')
def posts_bbc():
    _fetch_rss('https://feeds.bbci.co.uk/russian/rss.xml', 'bbc')


@post_handler('remontka', 'Статьи Remontka.pro')
def posts_remontka():
    _fetch_rss('https://remontka.pro/feed/', 'remontka')


@post_handler('habr', 'Статьи на Хабре')
def posts_habr():
    _fetch_rss('https://habr.com/ru/rss/articles/', 'habr')


@post_handler('hell-0', 'Обновления сайта')
def posts_hello():
    pass
