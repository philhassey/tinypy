`tp_obj`


Tinypy's object representation.


Every object in tinypy is of this type in the C API.

### Fields ###


|`type`| This determines what kind of objects it is. It is either TP\_NONE, in        which case this is the none type and no other fields can be accessed.        Or it has one of the values listed below, and the corresponding        fields can be accessed.|
|:-----|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`number`| TP\_NUMBER                                                                                                                                                                                                                                              |
|`number.val`| A double value with the numeric value.                                                                                                                                                                                                                  |
|`string`| TP\_STRING                                                                                                                                                                                                                                              |
|`string.val`| A pointer to the string data.                                                                                                                                                                                                                           |
|`string.len`| Length in bytes of the string data.                                                                                                                                                                                                                     |
|`dict`| TP\_DICT                                                                                                                                                                                                                                                |
|`list`| TP\_LIST                                                                                                                                                                                                                                                |
|`fnc` | TP\_FNC                                                                                                                                                                                                                                                 |
|`data`| TP\_DATA                                                                                                                                                                                                                                                |
|`data.val`| The user-provided data pointer.                                                                                                                                                                                                                         |
|`data.magic`| The user-provided magic number for identifying the data type.                                                                                                                                                                                           |



[Back to the General module.](General.md)