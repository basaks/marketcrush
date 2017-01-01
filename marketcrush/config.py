import yaml


class Config:
    """Class representing the global configuration of the marketcrush scripts

    Parameters
    ----------
    yaml_file : string
        The path to the yaml config file. For details on the yaml schema
        see the marketcrush documentation
    """
    def __init__(self, yaml_file):
        with open(yaml_file, 'r') as f:
            s = yaml.load(f)
        self.data_path = s['data'][0]['path']




