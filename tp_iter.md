`tp_obj tp_iter(TP,tp_obj self, tp_obj k) `


Iterate through a list or dict.


If self is a list/string/dictionary, this will iterate over the
elements/characters/keys respectively, if k is an increasing index
starting with 0 up to the length of the object-1.


In the case of a list of string, the returned items will correspond to the
item at index k. For a dictionary, no guarantees are made about the order.
You also cannot call the function with a specific k to get a specific
item -- it is only meant for iterating through all items, calling this
function len(self) times. Use [tp\_get](tp_get.md) to retrieve a specific item, and
[tp\_len](tp_len.md) to get the length.

### Parameters ###


|`self`| The object over which to iterate.|
|:-----|:---------------------------------|
|`k`   | You must pass 0 on the first call, then increase it by 1 after each call,     and don't call the function with k >= len(self).|


### Returns ###



The first (k = 0) or next (k = 1 .. len(self)-1) item in the iteration.


[Back to the Operations module.](Operations.md)