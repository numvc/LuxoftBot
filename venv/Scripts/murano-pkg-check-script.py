#!C:\All\LuxoftBot\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'murano-pkg-check==0.3.0','console_scripts','murano-pkg-check'
__requires__ = 'murano-pkg-check==0.3.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('murano-pkg-check==0.3.0', 'console_scripts', 'murano-pkg-check')()
    )
