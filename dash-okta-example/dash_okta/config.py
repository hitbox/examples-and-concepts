from configparser import ConfigParser

def _resolve_for_cp(cp_or_path):
    """
    Pass through for an instance of ConfigParser, otherwise assume path and
    read and return instance of ConfigParser.
    """
    if isinstance(cp_or_path, ConfigParser):
        cp = cp_or_path
    else:
        path = cp_or_path
        cp = ConfigParser()
        cp.read(path)
    return cp

def _cp_dict_for(cp, key):
    cp = _resolve_for_cp(cp)
    return dict(cp[key])

def okta_from_ini(cp, key='okta'):
    """
    Dict from INI file for okta client settings.
    """
    return _cp_dict_for(cp, key)

def flask_from_ini(cp, key='flask', uppercase_keys=True):
    """
    Dict from INI file for Flask configuration. Intended to be used with
    `app.config.from_mapping`.
    """
    config = _cp_dict_for(cp, key)
    if uppercase_keys:
        config = {key.upper(): val for key, val in config.items()}
    return config

def load_from_ini(app, path, prefix_okta='OKTA_'):
    """
    Load Flask and Okta config from INI into flask app's config.
    """
    okta_config = okta_from_ini(path)
    if prefix_okta

    flask_config = okta_from_ini(path)
