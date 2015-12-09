`tp_obj tp_setmeta(TP) `


Set a "dict's meta".


This is a builtin function, so you need to use [tp\_params](tp_params.md) to provide the
parameters.


In tinypy, each dictionary can have a so-called "meta" dictionary attached
to it. When dictionary attributes are accessed, but not present in the
dictionary, they instead are looked up in the meta dictionary. To get the
raw dictionary, you can use [tp\_getraw](tp_getraw.md).


This function is particulary useful for objects and classes, which are just
special dictionaries created with [tp\_object](tp_object.md) and [tp\_class](tp_class.md). There you can
use tp\_setmeta to change the class of the object or parent class of a class.

### Parameters ###


|`self`| The dictionary for which to set a meta.|
|:-----|:---------------------------------------|
|`meta`| The meta dictionary.                   |


### Returns ###



None


[Back to the Builtins module.](Builtins.md)