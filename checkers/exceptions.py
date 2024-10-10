class InvalidCheckException(Exception):
    """
    Raised when a check function is invalid.
    """


class ConfigException(Exception):
    pass


class ConfigFileNotFoundException(ConfigException):
    """
    Raised when trying to load a configuration file that does not exist
    """


class ConfigFileInvalid(ConfigException):
    """
    Raised when the config file does not conform to the required spec
    """


class SkipException(Exception):
    """
    Raised when a model should be skipped from being checked
    """


class WarnException(Exception):
    """
    Raised when a model should be warned rather than failed
    """
