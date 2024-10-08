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
