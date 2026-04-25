"""Все фильтры"""


# - импорт модулей
import markdown
import datetime
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

def plural_ru(n, words):
    n = abs(n) % 100
    if 11 <= n <= 14:
        return words[2]
    n1 = n % 10
    if n1 == 1:
        return words[0]
    if 2 <= n1 <= 4:
        return words[1]
    return words[2]

def filter_relative_time(value, now=None):
    if not value:
        return ""

    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)

    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.timezone.utc)
    else:
        value = value.astimezone(datetime.timezone.utc)

    diff = now - value
    seconds = diff.total_seconds()

    if seconds < 0:
        return "в будущем"
    if seconds < 60:
        return "только что"

    minutes = int(seconds // 60)
    if minutes < 60:
        return f"{minutes} {plural_ru(minutes, ('минуту назад', 'минуты назад', 'минут назад'))}"

    hours = int(minutes // 60)
    if hours < 24:
        return f"{hours} {plural_ru(hours, ('час назад', 'часа назад', 'часов назад'))}"

    days = int(hours // 24)
    if days < 7:
        return f"{days} {plural_ru(days, ('день назад', 'дня назад', 'дней назад'))}"

    weeks = int(days // 7)
    if weeks < 4:
        return f"{weeks} {plural_ru(weeks, ('неделю назад', 'недели назад', 'недель назад'))}"

    months = int(days // 30)
    if months < 12:
        return f"{months} {plural_ru(months, ('месяц назад', 'месяца назад', 'месяцев назад'))}"

    years = int(days // 365)
    return f"{years} {plural_ru(years, ('год назад', 'года назад', 'лет назад'))}"

# - сбор всех фильтров
jinja_filters = {}

for name in list(globals().keys()):
    if name.startswith("filter_") and callable(globals()[name]):
        jinja_filters[name[7:]] = globals()[name]
