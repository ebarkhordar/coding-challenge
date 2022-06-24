import pytest

from tests.interface import StackDataStructure


@pytest.fixture
def my_stack():
    return StackDataStructure()
