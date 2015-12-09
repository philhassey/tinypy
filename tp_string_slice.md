`tp_obj tp_string_slice(TP,tp_obj s, int a, int b) `


Create a new string sliced from an existing string.


Unlike [tp\_string](tp_string.md) and [tp\_string\_n](tp_string_n.md), a copy of the actual string is made,
and storage for the new string will always be managed by tinypy, no matter
what kind of string you pass.

### Example ###

tp_obj foo(void)
{
    char test[4] = "foo";
    return tp_string_slice(tp_string(test), 0, 3);
}}}}


This will work correctly, even though the variable "test" will go out of
scope when the function returns, because tp_string_splice makes its own
copy of the string.

===Parameters===


||`s`|| The string to create a substring of.||
||`a`|| Index of the first character to include in the slice.||
||`b`|| Index of the first character not to include.||


===Returns===



A new string object corresponding to s[a:b] in actual tinypy code.


[String Back to the String module.]```