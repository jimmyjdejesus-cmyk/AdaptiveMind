
import sys
sys.path.insert(0, '.')
try:
    from adaptivemind_core.app import AdaptiveMindApplication
    print('Import successful')
except Exception as e:
    print(f'Import failed: {e}')

