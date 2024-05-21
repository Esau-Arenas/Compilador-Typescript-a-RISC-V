from enum import Enum

class ExpressionType(Enum):
    INTEGER = 0
    FLOAT = 1
    STRING = 2
    BOOLEAN = 3
    ARRAY = 4
    STRUCT = 5
    NULL = 6
    CHAR = 7
    BREAK = 8
    CONTINUE = 9
    RETURN = 10