import logging

from fileapi.app.config import config
from wsgi import app


logger = logging.getLogger(config.APP_NAME)


def autoretry_task(name, max_retries=config.TASK_MAX_RETRIES, countdown=config.TASK_DELAY,
                   exceptions=(Exception,)):
    """
    :param name: Имя задачи
    :param max_retries: Максимальное количество повторений
    :param countdown: Израсходованное количество попыток
    :param exceptions: Список чувствительности по исключениям для retry
    :return: decorator Декоратор для задачи
    """
    if not exceptions:
        raise ValueError("You must define a list of retriable exceptions.")

    def decorator(func):
        @app.task(name=name, max_retries=max_retries, bind=True, countdown=countdown)
        def wrapper(self, *args, **kwargs):
            try:
                logger.debug(f'RUN task({name}) with params {args or kwargs}')
                return func(*args, **kwargs)
            except Exception as exc:
                for exception_type in exceptions:
                    if isinstance(exc, exception_type):
                        if self.request.retries + 1 < max_retries:
                            logger.warning(
                                f'RETRY #{self.request.retries + 1} to run task({name}) with params {args or kwargs} '
                                f'because of exception {exc}'
                            )
                            return self.retry(countdown=countdown * (self.request.retries + 1), exc=exc)

                logger.error(f'Failed to complete the task({name}) with params {args or kwargs}. \n'
                             f'Error: {exception_type}({exc})')
                raise exc

        return wrapper

    return decorator
