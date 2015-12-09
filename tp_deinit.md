`void tp_deinit(TP) `


Destroys a VM instance.


When you no longer need an instance of tinypy, you can use this to free all
memory used by it. Even when you are using only a single tinypy instance, it
may be good practice to call this function on shutdown.


[Back to the VM module.](VM.md)