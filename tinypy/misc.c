tp_obj *tp_ptr(tp_obj o) {
    tp_obj *ptr = tp_malloc(sizeof(tp_obj)); *ptr = o;
    return ptr;
}

tp_obj _tp_dcall(TP,tp_obj fnc(TP)) { 
    return fnc(tp);
}
tp_obj _tp_tcall(TP,tp_obj fnc) {
    if (fnc.fnc.ftype&2) {
        _tp_list_insert(tp,tp->params.list.val,0,fnc.fnc.val->self);
    }
    return _tp_dcall(tp,fnc.fnc.fval);
}

tp_obj tp_fnc_new(TP,int t, void *v, tp_obj s, tp_obj g) {
    tp_obj r = {TP_FNC};
    _tp_fnc *self = tp_malloc(sizeof(_tp_fnc));
    self->self = s;
    self->globals = g;
    r.fnc.ftype = t;
    r.fnc.val = self;
    r.fnc.fval = v;
    return tp_track(tp,r);
}

tp_obj tp_def(TP,void *v, tp_obj g) {
    return tp_fnc_new(tp,1,v,None,g);
}

tp_obj tp_fnc(TP,tp_obj v(TP)) {
    return tp_fnc_new(tp,0,v,None,None);
}

tp_obj tp_method(TP,tp_obj self,tp_obj v(TP)) {
    return tp_fnc_new(tp,2,v,self,None);
}

tp_obj tp_data(TP,void *v) {
    tp_obj r = {TP_DATA};
    r.data.info = tp_malloc(sizeof(_tp_data));
    r.data.val = v;
    r.data.meta = 0;
    r.data.meta = &r.data.info->meta;
    return tp_track(tp,r);
}

tp_obj tp_params(TP) {
    tp_obj r;
    tp->params = tp->_params.list.val->items[tp->cur];
    r = tp->_params.list.val->items[tp->cur];
    r.list.val->len = 0;
    return r;
}
tp_obj tp_params_n(TP,int n, tp_obj argv[]) {
    tp_obj r = tp_params(tp);
    int i; for (i=0; i<n; i++) { _tp_list_append(tp,r.list.val,argv[i]); }
    return r;
}
tp_obj tp_params_v(TP,int n,...) {
    int i;
    tp_obj r = tp_params(tp);
    va_list a; va_start(a,n);
    for (i=0; i<n; i++) { 
        _tp_list_append(tp,r.list.val,va_arg(a,tp_obj)); 
    }
    va_end(a);
    return r;
}
