import pytest
from task import is_equal, return_indexes_sum

def test_is_equal_basic():
    assert is_equal([1, 1, 1])
    assert is_equal([5])
    assert not is_equal([1, 2, 1])
    assert not is_equal([1, 2, 3])
    assert is_equal([])

def test_is_equal_type_error():
    with pytest.raises(TypeError):
        is_equal([1, 2, "3"])
    with pytest.raises(TypeError):
        is_equal(["a", "b"])

def test_return_indexes_sum_basic():
    assert return_indexes_sum([1, 2, 3, 4], 5) == [0, 3]
    assert return_indexes_sum([2, 7, 11, 15], 9) == [0, 1]
    assert return_indexes_sum([1, 1, 1, 1], 2) == [0, 1]
    assert return_indexes_sum([1, 2, 3], 10) is None
    assert return_indexes_sum([], 0) is None

def test_return_indexes_sum_type_error():
    with pytest.raises(TypeError):
        return_indexes_sum([1, "2", 3], 5)
    with pytest.raises(TypeError):
        return_indexes_sum([1, 2, 3], "5")
