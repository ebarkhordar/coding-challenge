import pytest

from tests.interface import StackDataStructure


def test_size(my_stack, mocker):
    mocker.patch.object(StackDataStructure, 'stack', ['A', 'B', 'C', 'D'])
    assert type(my_stack.size()) is int
    assert my_stack.size() == 4
    mocker.patch.object(StackDataStructure, 'stack', ['A', 'B'])
    assert type(my_stack.size()) is int
    assert my_stack.size() == 2
    mocker.patch.object(StackDataStructure, 'stack', [])
    assert type(my_stack.size()) is int
    assert my_stack.size() == 0


def test_push(my_stack, mocker):
    with pytest.raises(Exception) as exc_info:
        my_stack.push(None)
    assert str(exc_info.value) == 'NullElementException'

    mocker.patch.object(StackDataStructure, 'stack', ['A', 'B', 'C'])
    my_stack.push('D')
    assert my_stack.stack[-1] == 'D'
    my_stack.push('F')
    my_stack.push('G')
    assert my_stack.stack[-1] == 'G'


def test_pop(my_stack, mocker):
    with pytest.raises(Exception) as exc_info:
        my_stack.pop()
    assert str(exc_info.value) == 'EmptyStackException'

    mocker.patch.object(StackDataStructure, 'stack', ['A', 'B', 'C'])
    assert my_stack.pop() == 'C'
    assert my_stack.pop() == 'B'
    assert my_stack.pop() == 'A'

    with pytest.raises(Exception) as exc_info:
        my_stack.pop()
    assert str(exc_info.value) == 'EmptyStackException'


def test_peek(my_stack, mocker):
    with pytest.raises(Exception) as exc_info:
        assert my_stack.peek()
    assert str(exc_info.value) == 'EmptyStackException'

    mocker.patch.object(StackDataStructure, 'stack', ['A', 'B', 'C'])
    assert my_stack.peek() == 'C'
    assert my_stack.peek() == 'C'

    mocker.patch.object(StackDataStructure, 'stack', ['A', 'B'])
    assert my_stack.peek() == 'B'


def test_empty(my_stack, mocker):
    assert my_stack.empty() is True
    mocker.patch.object(StackDataStructure, 'stack', ['A', 'B', 'C'])
    assert my_stack.empty() is False
