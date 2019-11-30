#!C:\All\LuxoftBot\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'yaql==1.1.3','console_scripts','yaql'
__requires__ = 'yaql==1.1.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('yaql==1.1.3', 'console_scripts', 'yaql')()
    )
