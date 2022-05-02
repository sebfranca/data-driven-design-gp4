import logging

# TODO: Remove this.

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
debug_handler = logging.FileHandler(filename='log_debug.log', mode='w')
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(logging.Formatter(
    '%(asctime)s -%(levelname) 7s - %(module)s.%(funcName)s - %(message)s' ) )
info_handler  = logging.FileHandler(filename='log.log', mode='w')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname) 5s - %(message)s' ) )
logger.addHandler(debug_handler)
logger.addHandler(info_handler)


#TODO: why does one of the logs show in reentrant's __init__?




__author__      = 'The PyAuxetic Team'
__copyright__   = 'Copyright 2021, The PyAuxetic Team'
__credits__     = ['Mohammadreza Khoshbin', 'Javad Kadkhodapour']
__license__     = 'AGPLv3'
__version__     = "2.0.1"
__maintainer__  = 'Mohammadreza Khoshbin'
__email__       = 'm.khoshbin@live.com'
__status__      = 'Production'
__docs__        = 'https://pyauxetic.readthedocs.io'
__description__ = 'Python plugin and library for modeling, analyzing, and post-processing auxetic structures in Abaqus.'
