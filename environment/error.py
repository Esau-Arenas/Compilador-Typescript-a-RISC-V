class Error:
    def __init__(self, line, column, error_type, message):
        self.line = line
        self.column = column
        self.error_type = error_type
        self.message = message