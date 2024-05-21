from abc import ABC, abstractmethod

class Expression(ABC):

    @abstractmethod
    def ejecutar(self, ast, env):
        pass