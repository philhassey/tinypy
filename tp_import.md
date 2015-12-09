`tp_obj tp_import(TP, char const *fname, char const *name, void *codes) `


Imports a module.

### Parameters ###


|`fname`| The filename of a file containing the module's code.|
|:------|:----------------------------------------------------|
|`name` | The name of the module.                             |
|`codes`| The module's code. If this is given, fname is ignored.|


### Returns ###



The module object.


[Back to the VM module.](VM.md)