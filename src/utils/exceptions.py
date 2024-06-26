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