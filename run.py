# %%
import sys
import os

from package_1 import helpers as h1
from package_1 import constants as c



h1.generate_key()

h1.analyze_regulator()

sys.modules[__name__].__dict__.clear()

# %%
