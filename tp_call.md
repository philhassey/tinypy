`tp_obj tp_call(TP,tp_obj self, tp_obj params) `


Calls a tinypy function.


Use this to call a tinypy function.

### Parameters ###


|`tp`| The VM instance.|
|:---|:----------------|
|`self`| The object to call.|
|`params`| Parameters to pass.|


### Example ###


```
 tp_call(tp,
     tp_get(tp, tp->builtins, tp_string("foo")),
     tp_params_v(tp, tp_string("hello")))
```

This will look for a global function named "foo", then call it with a single
positional parameter containing the string "hello".


[Back to the VM module.](VM.md)