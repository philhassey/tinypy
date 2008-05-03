#include "tp.c"
/* INCLUDE */

int main(int argc, char *argv[]) {
    tp_vm *tp = tp_init(argc,argv);
    /* INIT */
    tp_call(tp,"py2bc","tinypy",None);
    tp_deinit(tp);
    return(0);
}

/**/
