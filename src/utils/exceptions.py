class UserAlreadyExistsException(Exception):
    pass

class LoginException(Exception):
    pass

class UserNotFound(Exception):
    pass

class BiometricsNotFound(Exception):
    pass

class BiometricsNotValid(Exception):
    pass

class CryptoException(Exception):
    pass

class ExpensesException(Exception):
    pass

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UserNotFoundException(Exception):
    pass

class InvalidCredentialsException(Exception):
    pass
