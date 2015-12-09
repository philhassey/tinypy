`tp_inline static tp_obj tp_string_n(char const *v,int n) `


Creates a new string object from a partial C string.


Like [tp\_string](tp_string.md), but you specify how many bytes of the given C string to
use for the string object. The **note** also applies for this function, as the
string reference and length are kept, but no actual substring is stored.


[Back to the General module.](General.md)