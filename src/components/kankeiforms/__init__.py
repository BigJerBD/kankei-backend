from components.kankeiforms.kankeiform import KankeiForm


def init(config):
    KankeiForm.timeout = config.DB_TIMEOUT_SEC
    from . import exploration
    from . import comparison
    from . import autocorrelation


def get_kankeiforms(config):
    init(config)
    return KankeiForm.registry


def get_kankeiforms_dict(config):
    """
    note:: currently simply forward query config, however it is not ideal
    since we want to present information about `querying` and not the config
    :return:
    """
    init(config)
    return {
        grp: {name: content.asdict() for name, content in content.items()}
        for grp, content in KankeiForm.registry.items()
    }
