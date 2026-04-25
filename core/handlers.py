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


@register('bbc')
def handler_bbc():
    import requests
    import xml.etree.ElementTree as ET
    from core.core import post_add
    from core.models import Post

    resp = requests.get('https://feeds.bbci.co.uk/news/rss.xml', timeout=10)
    root = ET.fromstring(resp.content)
    channel = root.find('channel')

    for item in (channel.findall('item') or [])[:10]:
        title = item.findtext('title', '').strip()
        link = item.findtext('link', '').strip()
        desc = item.findtext('description', '').strip()

        if not title:
            continue

        existing = Post.query.filter(
            Post.category == 'bbc',
            Post.data.like(f'## {title}\n%')
        ).first()
        if existing:
            continue

        post_add('bbc', f'## {title}\n\n{desc}\n\n[Читать далее]({link})')
