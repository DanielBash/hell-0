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


@post_handler('arxiv_ai', 'arXiv: AI / ML')
def posts_arxiv_ai():
    _fetch_rss('http://export.arxiv.org/rss/cs.AI', 'arxiv_ai')


@post_handler('arxiv_physics', 'arXiv: Physics')
def posts_arxiv_physics():
    _fetch_rss('http://export.arxiv.org/rss/physics', 'arxiv_physics')


@post_handler('nature', 'Nature News')
def posts_nature():
    _fetch_rss('https://www.nature.com/nature.rss', 'nature')


@post_handler('science_mag', 'Science Magazine')
def posts_science_mag():
    _fetch_rss('https://www.science.org/rss/news_current.xml', 'science_mag')


@post_handler('phys_org', 'Phys.org')
def posts_phys_org():
    _fetch_rss('https://phys.org/rss-feed/', 'phys_org')


@post_handler('nplus1', 'N+1 (наука)')
def posts_nplus1():
    _fetch_rss('https://nplus1.ru/rss', 'nplus1')


@post_handler('naked_science', 'Naked Science')
def posts_naked_science():
    _fetch_rss('https://naked-science.ru/feed', 'naked_science')


@post_handler('hackernews', 'Hacker News')
def posts_hackernews():
    _fetch_rss('https://hnrss.org/frontpage', 'hackernews')


@post_handler('lenta', 'Лента.ру')
def posts_lenta():
    _fetch_rss('https://lenta.ru/rss/news', 'lenta')


@post_handler('3dnews', '3DNews')
def posts_3dnews():
    _fetch_rss('https://3dnews.ru/news/rss/', '3dnews')
