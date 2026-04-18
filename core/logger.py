"""Настройки логирования"""

# -- импортирование модулей
import datetime
import logging
import shutil
from rich.console import Console
from rich.traceback import install
import friendly_traceback

# -- настройки для более понятных отчетах
friendly_traceback.install(lang="ru")

# -- настройки вывода
console = Console(force_terminal=True, color_system="truecolor", legacy_windows=False,
                  width=shutil.get_terminal_size().columns * 2)


# - базовый класс для логов
class RichMetaHandler(logging.Handler):
    def emit(self, record):
        time = datetime.datetime.fromtimestamp(record.created).strftime("%H:%M:%S")
        level = record.levelname
        msg = record.getMessage()
        file = record.filename
        line = record.lineno

        console.print(
            f"[dim]{time}[/] "
            f"[bold cyan]{level:<7}[/] "
            f"[magenta]{file}:{line}[/] "
            f"{msg}",
            markup=True
        )


# - функция красивого вывода
def rich(msg):
    console.print(msg, markup=True)

handler = RichMetaHandler()
log = logging.getLogger("news")
log.setLevel(logging.DEBUG)
log.addHandler(handler)
log.propagate = False
log.rich = rich
