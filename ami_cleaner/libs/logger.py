from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO


def get_logger(args):
    logger = getLogger('ami_cleaner')
    handler = StreamHandler()
    handler.setLevel(DEBUG if args.debug else INFO)
    handler_format = Formatter(
        '%(asctime)s \
        %(levelname)-8s \
        %(name)s:%(lineno)-4d \
        %(funcName)-16s \
        %(message)s'
    )
    handler.setFormatter(handler_format)
    logger.setLevel(DEBUG)
    logger.addHandler(handler)
    logger.propagate = False
    return logger
