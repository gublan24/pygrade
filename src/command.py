__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

class Command(object):

    def __init__(self):
        raise NotImplementedError("The method should be implemented in the concrete class!")

    def execute(self) -> bool:
        raise NotImplementedError("The method should be implemented in the concrete class!")

    def set_args(self, args: list):
        raise NotImplementedError("The method should be implemented in the concrete class!")

    def set_kwargs(self, kwargs: dict):
        raise NotImplementedError("The method should be implemented in the concrete class!")

    def get_result(self) -> (bool, str):
        raise NotImplementedError("The method should be implemented in the concrete class!")


class PythonCommand(Command):

    def __init__(self, task_to_perform, args=[], kwargs={}):
        self.task = task_to_perform
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def set_args(self, args: list):
        self.args = args

    def set_kwargs(self, kwargs: dict):
        self.kwargs = kwargs

    def execute(self):
        """
        The goal is to call a method by reference,
        see https://stackoverflow.com/a/706735/3504748
        """
        self.result = self.task(*self.args, **self.kwargs)

    def get_result(self) -> (bool, str):
        return self.result


class BashCommand(Command):

    def __init__(self, task_to_perform: str, pre_rq: str = None):
        super().__init__()
        self.task = task_to_perform
        self.pre_rq = pre_rq
        self.result = ""
        self.executed = False

    def execute(self) -> bool:
        pass

    def get_result(self) -> str:
        pass
