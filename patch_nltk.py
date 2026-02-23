#!/usr/bin/env python3
"""Patch NLTK to work without wordnet data."""

import os
import re

# Path to NLTK site-packages
nltk_base = '/usr/local/lib/python3.11/site-packages/nltk'

# 1. Patch nltk/__init__.py to skip wordnet-related imports
nltk_init = os.path.join(nltk_base, '__init__.py')
with open(nltk_init, 'r') as f:
    content = f.read()

# Comment out the line that imports from translate (which requires wordnet)
content = content.replace(
    'from nltk.translate import *',
    '# from nltk.translate import *  # Patched to skip wordnet'
)

with open(nltk_init, 'w') as f:
    f.write(content)
print('Patched nltk/__init__.py')

# 2. Patch nltk/corpus/reader/__init__.py - add mock for AlignedCorpusReader
reader_init = os.path.join(nltk_base, 'corpus', 'reader', '__init__.py')
with open(reader_init, 'r') as f:
    content = f.read()

# Find the __all__ list and add AlignedCorpusReader to it
# First, find the current __all__ list
all_pattern = r'(__all__\s*=\s*\[)(\s*"[^"]*"(?:\s*,\s*"[^"]*")*\s*)(\])'
match = re.search(all_pattern, content)
if match:
    # Add AlignedCorpusReader to the __all__ list
    all_items = match.group(2)
    if '"AlignedCorpusReader"' not in all_items:
        content = content[:match.start(2)] + '    "AlignedCorpusReader",\n' + all_items + content[match.end(2):]
        print('Added AlignedCorpusReader to __all__')

# Insert the mock class before the _readers dictionary definition
mock_code = '''

# Mock for AlignedCorpusReader to avoid wordnet dependency
class AlignedCorpusReader:
    """Mock AlignedCorpusReader that does not require wordnet."""
    def __init__(self, *args, **kwargs):
        pass
    def alignments(self, *args, **kwargs):
        return []
    def __iter__(self):
        return iter([])
'''

# Insert before the _readers dictionary
content = content.replace(
    '_readers = {',
    mock_code + '\n_readers = {'
)

# Now comment out the aligned import to avoid its dependencies
content = content.replace(
    'from nltk.corpus.reader.aligned import *',
    '# from nltk.corpus.reader.aligned import *  # Patched - requires translate/wordnet'
)

with open(reader_init, 'w') as f:
    f.write(content)
print('Patched nltk/corpus/reader/__init__.py')

# 3. Patch nltk/stem/wordnet.py to skip morphy initialization
wordnet_py = os.path.join(nltk_base, 'stem', 'wordnet.py')
with open(wordnet_py, 'r') as f:
    content = f.read()

# Replace the morphy initialization with a safe version
content = content.replace(
    'morphy = wn.morphy',
    'try:\n    morphy = wn.morphy\nexcept:\n    morphy = None  # Patched for missing wordnet'
)

with open(wordnet_py, 'w') as f:
    f.write(content)
print('Patched nltk/stem/wordnet.py')

# 4. Patch nltk/translate/meteor_score.py to handle missing wordnet
meteor_py = os.path.join(nltk_base, 'translate', 'meteor_score.py')
with open(meteor_py, 'r') as f:
    content = f.read()

# Replace the wordnet import with a safe version
old_import = "from nltk.corpus import WordNetCorpusReader, wordnet"
new_import = """try:
    from nltk.corpus import WordNetCorpusReader, wordnet
except ImportError:
    WordNetCorpusReader = None
    wordnet = None
    # Create a minimal mock for when wordnet is not available
    class _MockWordnet:
        def morphy(self, *args, **kwargs): return None
    wordnet = _MockWordnet()"""

content = content.replace(old_import, new_import)

with open(meteor_py, 'w') as f:
    f.write(content)
print('Patched nltk/translate/meteor_score.py')

print('NLTK patching complete!')
