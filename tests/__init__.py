# -*- coding: utf-8 -*-
"""package init"""

import os
import sys

# (for now) run tests relative to package root
# from: https://stackoverflow.com/a/55795157/4054683
# also, over time modularize source, add __main__ and remove this
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pymwp')))