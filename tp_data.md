`tp_obj tp_data(TP,int magic,void *v) `

Creates a new data object.

### Parameters ###
|`magic`| An integer number associated with the data type. This can be used         to check the type of data objects.|
|:------|:------------------------------------------------------------------------------------------------------------|
|`v`    | A pointer to user data. Only the pointer is stored in the object,         you keep all responsibility for the data it points to.|

### Returns ###
The new data object.

### Public fields ###
The following fields can be access in a data object:

|`magic`| An integer number stored in the object.|
|:------|:---------------------------------------|
|`val`  | The data pointer of the object.        |
|`info->free`| If not NULL, a callback function called when the object gets              destroyed.|

### Example ###
```
void *__free__(TP, tp_obj self)
{
    free(self.data.val);
}

tp_obj my_obj = tp_data(TP, 0, my_ptr);
my_obj.data.info->free = __free__;
```

[Back to the Miscellaneous module.](Miscellaneous.md)