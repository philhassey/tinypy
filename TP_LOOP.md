`#define TP_LOOP(e) `


Macro to iterate over all remaining arguments.


If you have a function which takes a variable number of arguments, you can
iterate through all remaining arguments for example like this:

```
tp_obj *my_func(tp_vm *tp)
{
    // We retrieve the first argument like normal.
    tp_obj first = TP_OBJ();
    // Then we iterate over the remaining arguments.
    tp_obj arg;
    TP_LOOP(arg)
        // do something with arg
    TP_END
}
```


[Back to the General module.](General.md)