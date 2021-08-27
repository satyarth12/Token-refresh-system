import pytest


@pytest.mark.xfail
def test_example():
    assert 1 == 1


@pytest.mark.slow
def test_example2():
    assert 1 == 2
