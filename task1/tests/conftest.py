import pytest

from task1.tests.interface import StackDataStructure


@pytest.fixture
def my_stack():
    return StackDataStructure()
