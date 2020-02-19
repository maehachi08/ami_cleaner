from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO


def get_logger(args):
    logger = getLogger('ami_cleaner')
    handler = StreamHandler()
    handler.setLevel(DEBUG if args.debug else INFO)
    handler_format = Formatter(
        '%(asctime)s \
        %(levelname)s \
        %(name)s:%(lineno)d \
        %(funcName)-8s \
        %(message)s'
    )
    handler.setFormatter(handler_format)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
