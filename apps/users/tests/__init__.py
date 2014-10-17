#Importing all files, no longer needed in Django ^1.6
import os
import glob
__all__ = [os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/test_*.py")]
