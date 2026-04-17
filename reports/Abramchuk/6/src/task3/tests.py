import pytest
from task import repeatStr

def test_repeat_basic():
    assert repeatStr("e", 0) == ""
    assert repeatStr("e", 3) == "eee"
    assert repeatStr(" ABC ", 2) == " ABC  ABC "

def test_repeat_value_error():
    with pytest.raises(ValueError):
        repeatStr("e", -2)

def test_repeat_type_error():
    with pytest.raises(TypeError):
        repeatStr(None, 1)
