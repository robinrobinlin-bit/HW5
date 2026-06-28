import sys
import pytinytex

try:
    print('Installing TinyTeX...')
    pytinytex.install()
    print('TinyTeX installed successfully')
except Exception as e:
    print('Error installing TinyTeX:', e)
    sys.exit(1)
