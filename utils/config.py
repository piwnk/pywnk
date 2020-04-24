import json
import os
from collections import namedtuple

CONFIG_FILE = 'config.json'

if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE) as fh:
        config = json.load(fh, object_hook=lambda d: namedtuple(
            'config', d.keys())(*d.values()))
