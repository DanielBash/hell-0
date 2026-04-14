"""Все фильтры"""

# - импорт модулей
import markdown
from markupsafe import Markup


# -- фильтры
# - фильтер markdown
def filter_markdown(text):
    html = markdown.markdown(
        text,
        extensions=[
            "fenced_code",
            "codehilite",
            "tables",
            "nl2br",
            "sane_lists"
        ]
    )

    return Markup(html)


# - сбор всех фильтров
jinja_filters = {}

for name in list(globals().keys()):
    if name.startswith("filter_") and callable(globals()[name]):
        jinja_filters[name[7:]] = globals()[name]
