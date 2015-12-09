`int tp_iget(TP,tp_obj *r, tp_obj self, tp_obj k) `


Failsafe attribute lookup.


This is like [tp\_get](tp_get.md), except it will return false if the attribute lookup
failed. Otherwise, it will return true, and the object will be returned
over the reference parameter r.


[Back to the Operations module.](Operations.md)