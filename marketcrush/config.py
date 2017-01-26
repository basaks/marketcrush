import yaml
import logging
from marketcrush.compat import HasMatplotlib

log = logging.getLogger(__name__)
log = log.setLevel(logging.INFO)

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
        self.data_path = s['data']
        self.strategy = s['strategy']
        self.strategy_parameters = s['parameters']
        self.output_file = s['output']['file']
        self.show = s['show_plot']
        if self.show and (not HasMatplotlib):
            self.show = False
            log.warning('Matplotlib could not be imported. Plotting will be'
                        'disabled!')

