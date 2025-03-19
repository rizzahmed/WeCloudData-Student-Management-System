import sys, os, json

def get_base_path():
    """ Get the base path of the executable or the script. """
    try:
        # When running as a bundled executable
        base_path = sys._MEIPASS
    except AttributeError:
        # When running from source
        base_path = os.path.dirname(os.path.realpath(__file__))
    return base_path


def ReadConfig():
    base_path = get_base_path()
    config_path = os.path.join(base_path, "config.json")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    else:
        with open(config_path, 'r') as file:
            config = json.load(file)
        
        return config


def getDirectoryPath(path):
    base_path = get_base_path()
    return os.path.join(base_path, path)