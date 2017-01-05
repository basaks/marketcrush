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
        self.strategy = s['strategy']
        self.point_value = self.strategy['point_value']
        self.short_tp = self.strategy['time_periods']['short_tp']
        self.long_tp = self.strategy['time_periods']['long_tp']
        self.filter_fp = self.strategy['time_periods']['filter_fp']
        self.filter_sp = self.strategy['time_periods']['filter_sp']
        self.risk_factor = self.strategy['risk_factor']
        self.initial_cap = self.strategy['initial_cap']
        self.atr_exit_fraction = self.strategy['atr_exit_fraction']
        self.atr_stops_period = self.strategy['atr_stops_period']
        self.commission = self.strategy['commission']
        self.point_value = self.strategy['point_value']
        self.output_file = s['output']['file']
