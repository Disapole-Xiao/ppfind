__version__ = "1.1.0"
__author__ = "disapole"
__email__ = "disapolexiao@gmail.com"

from .core import PaperInfoFetcher
from .cli import main
from .config import config_manager

__all__ = ['PaperInfoFetcher', 'main', 'config_manager']
