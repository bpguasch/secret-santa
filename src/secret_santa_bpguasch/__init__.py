# Copyright (C) 2022 Borja Pérez Guasch
# Author: Borja Pérez Guasch
# Contact: borjaperez@icloud.com
# License: MIT

"""A package that implements the Secret Santa algorithm and notifies participants by email of whom they have to gift."""


from .config import Game, EmailServer, InvalidConfigurationException
from .algorithm import SecretSanta
