from core.logger import log

HANDLERS = {}


def register(category):
    def decorator(fn):
        HANDLERS[category] = fn
        return fn
    return decorator


def run_all():
    for category, fn in HANDLERS.items():
        try:
            fn()
            log.info(f"Handler OK: {category}")
        except Exception as e:
            log.error(f"Handler error [{category}]: {e}")


def _fetch_rss(url, category, limit=10):
    import requests
    import xml.etree.ElementTree as ET
    from core.core import post_add
    from core.models import Post

    resp = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    root = ET.fromstring(resp.content)
    channel = root.find('channel')
    if channel is None:
        return

    for item in channel.findall('item')[:limit]:
        title = item.findtext('title', '').strip()
        link = item.findtext('link', '').strip()
        desc = item.findtext('description', '').strip()

        if not title:
            continue
        if Post.query.filter(Post.category == category,
                             Post.data.like(f'## {title}\n%')).first():
            continue

        post_add(category, f'## {title}\n\n{desc}\n\n[Читать далее]({link})')


@register('bbc')
def handler_bbc():
    _fetch_rss('https://feeds.bbci.co.uk/news/rss.xml', 'bbc')


@register('tass')
def handler_tass():
    _fetch_rss('https://tass.ru/rss/v2.xml', 'tass')


@register('lenta')
def handler_lenta():
    _fetch_rss('https://lenta.ru/rss/news', 'lenta')


@register('rbc')
def handler_rbc():
    _fetch_rss('https://rssexport.rbc.ru/rbcnews/news/30/full.rss', 'rbc')


@register('kommersant')
def handler_kommersant():
    _fetch_rss('https://www.kommersant.ru/RSS/main.xml', 'kommersant')
