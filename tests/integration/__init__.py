import os

from tests import root_dir

os.environ['PATH'] = "{}:{}".format(
    str(root_dir / 'chromedriver_bin'),
    os.environ['PATH']
)
