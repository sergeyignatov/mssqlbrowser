from distutils import sysconfig
from distutils.core import setup
import os

LIB_PATH = sysconfig.get_python_lib()

plugin_name = 'twisted/plugins/twisted_mssqlbrowser'
data_files = [
  (os.path.join(LIB_PATH, 'twisted', 'plugins'),
   [''.join((plugin_name, extension)) for extension in ('.py', '.pyc')])
]

setup(
    name='pymssqlbrowser',
    version='1.0',
    description='Provide MSSQL database browser fuctionality',
    author = 'Sergey Ignatov',
    author_email='cm2k05@gmail.com',
    data_files=data_files
)

