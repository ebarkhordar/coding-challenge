### Interface Struct
#### Methods:
* `size() -> integer`
Returns an integer representing the total number of items in the stack.


* `push(element)`
Pushes the element onto the top of the stack.
Throws a custom NullElementException if the supplied element is null.


* `pop() -> element`
Removes the top element from the stack and returns its value.
Throws a custom EmptyStackException if the stack is empty when this method is called.


* `peek() -> element`
Retrieves the top element from the stack without removing it, and returns its value.
Throws a custom EmptyStackException if the stack is empty when this method is called.


* `empty() -> boolean`
Tests whether the stack is empty.
