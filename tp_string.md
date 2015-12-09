`tp_inline static tp_obj tp_string(char const *v) `


Creates a new string object from a C string.


Given a pointer to a C string, creates a tinypy object representing the
same string.


**Note** Only a reference to the string will be kept by tinypy, so make sure
it does not go out of scope, and don't de-allocate it. Also be aware that
tinypy will not delete the string for you. In many cases, it is best to
use [tp\_string\_t](tp_string_t.md) or [tp\_string\_slice](tp_string_slice.md) to create a string where tinypy
manages storage for you.


[Back to the General module.](General.md)