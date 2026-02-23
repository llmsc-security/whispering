#!/usr/bin/env python3
"""
Create stub NLTK modules to avoid wordnet dependency issues.
This file creates minimal stubs that prevent the import errors.
"""
import os
import sys
import types

# Create a stub nltk module that won't trigger wordnet imports
def create_stub_nltk():
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

    # Create stub nltk.corpus.reader
    reader_stub = types.ModuleType('nltk.corpus.reader')
    reader_stub.__path__ = []

    # Add minimal AlignedCorpusReader to reader_stub
    class AlignedCorpusReader:
        """Minimal stub AlignedCorpusReader."""
        def __init__(self, *args, **kwargs):
            pass
        def alignments(self, *args, **kwargs):
            return []
        def __iter__(self):
            return iter([])

    reader_stub.AlignedCorpusReader = AlignedCorpusReader

    # Add reader_stub to corpus_stub
    corpus_stub.reader = reader_stub

    # Set up the module hierarchy
    sys.modules['nltk'] = nltk_stub
    sys.modules['nltk.translate'] = translate_stub
    sys.modules['nltk.stem'] = stem_stub
    sys.modules['nltk.corpus'] = corpus_stub
    sys.modules['nltk.corpus.reader'] = reader_stub

    print("Created stub NLTK modules")

if __name__ == "__main__":
    create_stub_nltk()
    print("NLTK stubs created successfully")
