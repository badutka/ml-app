import sys
from mlengine.common.logger import logger


class ExceptionWithIDMixin(object):
    def __init__(self, id: int | str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id


class ExceptionWithMsgMixin(object):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message


class GenericException(ExceptionWithIDMixin, ExceptionWithMsgMixin, Exception):
    def __init__(self, id: int | str, message: str):
        super().__init__(id, message)


class DetailedGenericException(GenericException):
    def __init__(self, id: int | str, message: str, error_detail: sys, *args, **kwargs):
        # todo: if e hasattr id or message -> get them from e into new exception
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_info = f"Error occured in {file_name} on line number {exc_tb.tb_lineno}."
        if message:
            error_info += f"\nError message: {message}."

        super().__init__(id, error_info)

    def __str__(self):
        return self.message


class DetailedGenericExceptionLogged(DetailedGenericException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.exception(self.message)

    def __str__(self):
        return self.message
