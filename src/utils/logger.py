import logging


class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[0m",
        "CRITICAL": "\033[0;31m",
        "RESET": "\033[0m",
    }

    def format(self, record):
        levelname = record.levelname
        reset = self.COLORS["RESET"]
        color = self.COLORS.get(levelname, reset)

        record.levelname = f"{color}{levelname}{reset}"
        record.msg = f"{color}{record.msg}{reset}"

        return super().format(record)


handler = logging.StreamHandler()
formatter = ColorFormatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.handlers = [handler]
