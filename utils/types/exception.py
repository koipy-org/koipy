class KoiError(Exception):
    pass


class ConfigError(KoiError):
    pass


class ConfigTypeError(ConfigError, TypeError):
    pass
