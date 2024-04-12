from loguru import logger

# Логгеры для дебага и эррора, файлы отправляются по команде /loggs
DEBUG = logger.add("LOGGING/DEBUG.txt", format="--------\n{time:DD-MM-YYYY HH:mm}\n{level}\n{message}\n--------", level='DEBUG', rotation='1 week')
ERROR = logger.add("LOGGING/ERROR.txt", format="--------\n{time:DD-MM-YYYY HH:mm}\n{level}\n{message}\n--------", level='ERROR', rotation='1 week')

