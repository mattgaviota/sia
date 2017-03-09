#!/usr/bin/env python3

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/Sia")
sys.path.insert(0, "/var/www/Sia/Sia")

from Sia import create_app

application = create_app('default')
