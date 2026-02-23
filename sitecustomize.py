"""
Sitecustomize module - automatically loaded when Python starts.
This module replaces the real NLTK package with stubs to avoid wordnet dependency.
"""
import sys
import types


def create_nltk_stubs():
    """Create stub NLTK modules to avoid wordnet dependency."""
    # Create stub nltk module
    nltk_stub = types.ModuleType('nltk')
    nltk_stub.__path__ = []

    # Create stub nltk.translate (which requires wordnet)
    translate_stub = types.ModuleType('nltk.translate')
    translate_stub.__path__ = []

    # Create stub nltk.stem
    stem_stub = types.ModuleType('nltk.stem')
    stem_stub.__path__ = []

    # Create stub nltk.corpus
    corpus_stub = types.ModuleType('nltk.corpus')
    corpus_stub.__path__ = []

    # Create stub nltk.corpus.reader with AlignedCorpusReader
    class AlignedCorpusReader:
        """Minimal stub AlignedCorpusReader."""
        pass

    reader_stub = types.ModuleType('nltk.corpus.reader')
    reader_stub.__path__ = []
    reader_stub.AlignedCorpusReader = AlignedCorpusReader
    reader_stub.__all__ = ['AlignedCorpusReader']
    corpus_stub.reader = reader_stub

    # Add stubs to sys.modules BEFORE any imports happen
    sys.modules['nltk'] = nltk_stub
    sys.modules['nltk.translate'] = translate_stub
    sys.modules['nltk.stem'] = stem_stub
    sys.modules['nltk.corpus'] = corpus_stub
    sys.modules['nltk.corpus.reader'] = reader_stub

    print('NLTK stubs installed via sitecustomize.py')


# Install stubs on module load
create_nltk_stubs()
