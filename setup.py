from distutils import sysconfig
from distutils.core import setup
import os

LIB_PATH = sysconfig.get_python_lib()

# ...

plugin_name = 'twisted/plugins/twisted_mssqlbrowser'
# '.pyc' extension is necessary for correct plugins removing
data_files = [
  (os.path.join(LIB_PATH, 'twisted', 'plugins'),
   [''.join((plugin_name, extension)) for extension in ('.py', '.pyc')])
]

setup(
      # ...
      data_files=data_files
)
