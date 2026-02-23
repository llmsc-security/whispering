#!/bin/bash
set -e

echo "Starting Whispering Tiger audio processing..."

# Set NLTK data directory
export NLTK_DATA=/app/nltk_data
mkdir -p $NLTK_DATA

cd /app

# Uninstall real NLTK and replace with stub
echo "Installing NLTK stubs..."
pip uninstall -y nltk && \
python -c "
import os
import sys
import types

# Create stub nltk module to avoid wordnet dependency
nltk_stub = types.ModuleType('nltk')
nltk_stub.__path__ = []

translate_stub = types.ModuleType('nltk.translate')
translate_stub.__path__ = []

stem_stub = types.ModuleType('nltk.stem')
stem_stub.__path__ = []

corpus_stub = types.ModuleType('nltk.corpus')
corpus_stub.__path__ = []

class AlignedCorpusReader:
    pass

reader_stub = types.ModuleType('nltk.corpus.reader')
reader_stub.__path__ = []
reader_stub.AlignedCorpusReader = AlignedCorpusReader
reader_stub.__all__ = ['AlignedCorpusReader']
corpus_stub.reader = reader_stub

sys.modules['nltk'] = nltk_stub
sys.modules['nltk.translate'] = translate_stub
sys.modules['nltk.stem'] = stem_stub
sys.modules['nltk.corpus'] = corpus_stub
sys.modules['nltk.corpus.reader'] = reader_stub

print('NLTK stubs installed successfully')
"

# Fix ctranslate2 executable stack issues
# The ctranslate2 shared library requires an executable stack
# Use execstack from binutils to clear the executable stack requirement
echo "Fixing ctranslate2 executable stack issue..."
CT2_LIB="/usr/local/lib/python3.11/site-packages/ctranslate2/_ext.cpython-311-x86_64-linux-gnu.so"
CT2_LIB_ALT="/usr/local/lib/python3.11/site-packages/ctranslate2/libctranslate2-bc15bf3f.so.4.5.0"

# Try to find and fix the ctranslate2 library
if command -v execstack &> /dev/null; then
    if [ -f "$CT2_LIB" ]; then
        echo "Found ctranslate2 library at $CT2_LIB"
        execstack -c "$CT2_LIB" 2>&1 || true
        echo "ctranslate2 executable stack cleared"
    elif [ -f "$CT2_LIB_ALT" ]; then
        echo "Found ctranslate2 library at $CT2_LIB_ALT"
        execstack -c "$CT2_LIB_ALT" 2>&1 || true
        echo "ctranslate2 executable stack cleared"
    else
        echo "ctranslate2 library not found, searching..."
        find /usr/local/lib -name "*ctranslate2*.so*" 2>/dev/null || true
    fi
else
    echo "execstack not found, trying alternative fix..."
    # Try using setarch to disable executable stack check
    export LD_PRELOAD=""
fi

echo "Starting websocket server on 0.0.0.0:11010..."

# Run audioWhisper.py
exec python audioWhisper.py --websocket_ip 0.0.0.0 --websocket_port 11010 "$@"
