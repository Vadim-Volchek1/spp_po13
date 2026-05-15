"""Tests for Levenshtein distance."""
import pytest
from levenshtein import levenshteinDistance

def test_levenshtein_spec():
    """Test Levenshtein distance based on specification."""
    with pytest.raises(TypeError):
        levenshteinDistance(None, None)

    assert levenshteinDistance(None, "test") == -1
    assert levenshteinDistance("test", None) == -1
    assert levenshteinDistance("", "") == 0
    assert levenshteinDistance("", "a") == 1
    assert levenshteinDistance(" aaapppp ", "") == 9
    assert levenshteinDistance("fly", "ant") == 3
    assert levenshteinDistance("hello", "hallo") == 1
