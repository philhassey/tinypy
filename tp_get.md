`tp_obj tp_get(TP,tp_obj self, tp_obj k) `


Attribute lookup.


This returns the result of using `self[k]` in actual code. It works for
dictionaries (including classes and instantiated objects), lists and strings.


As a special case, if self is a list, `self[None]` will return the first
element in the list and subsequently remove it from the list.


[Back to the Operations module.](Operations.md)