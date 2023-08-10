import logging
import logging.handlers


class Logger:

    _DEFAULT_FORMATTER = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    def __init__(self, name, path, **kwargs):
        self.my_logger = logging.getLogger(name)
        self.filename = "{path}/{name}.log".format(path=path, name=name)
        self._set_logger(**kwargs)

    def _set_logger(self, **kwargs):
        my_logger = self.my_logger
        my_logger.setLevel(kwargs.get("level", 'DEBUG'))
        formatter = kwargs.get("log_format", self._DEFAULT_FORMATTER)
        handler_ins = logging.handlers.RotatingFileHandler(self.filename)
        handler_ins.setFormatter(formatter)
        self.my_logger.addHandler(handler_ins)
        self.my_logger.propagate = False

    def get_logger(self):
        return self.my_logger
