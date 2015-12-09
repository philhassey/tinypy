`tp_vm`


Representation of a tinypy virtual machine instance.


A new tp\_vm struct is created with [tp\_init](tp_init.md), and will be passed to most
tinypy functions as first parameter. It contains all the data associated
with an instance of a tinypy virtual machine - so it is easy to have
multiple instances running at the same time. When you want to free up all
memory used by an instance, call [tp\_deinit](tp_deinit.md).

### Fields ###



These fields are currently documented:

|`builtins`| A dictionary containing all builtin objects.|
|:---------|:--------------------------------------------|
|`modules` | A dictionary with all loaded modules.       |
|`params`  | A list of parameters for the current function call.|
|`frames`  | A list of all call frames.                  |
|`cur`     | The index of the currently executing call frame.|
|`frames[n].globals`| A dictionary of global symbols in call frame n.|



[Back to the General module.](General.md)