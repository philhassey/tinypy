`tp_obj tp_params_v(TP,int n,...) `


Pass parameters for a tinypy function call.


When you want to call a tinypy method, then you use this to pass parameters
to it.

### Parameters ###


|`n`| The number of variable arguments following.|
|:--|:-------------------------------------------|
|`...`| Pass n tinypy objects, which a subsequently called tinypy method will       receive as parameters.|


### Returns ###



A tinypy list object representing the current call parameters. You can modify
the list before doing the function call.


[Back to the Miscellaneous module.](Miscellaneous.md)