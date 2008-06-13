tp_obj tp_print(TP) {
    int n = 0;
    tp_obj e;
    TP_LOOP(e)
        if (n) { printf(" "); }
        printf("%s",TP_CSTR(e));
        n += 1;
    TP_END;
    printf("\n");
    return tp_None;
}

tp_obj tp_bind(TP) {
    tp_obj r = TP_TYPE(TP_FNC);
    tp_obj self = TP_OBJ();
    return tp_fnc_new(tp,r.fnc.ftype|2,r.fnc.val,self,r.fnc.info->globals);
}

tp_obj tp_min(TP) {
    tp_obj r = TP_OBJ();
    tp_obj e;
    TP_LOOP(e)
        if (tp_cmp(tp,r,e) > 0) { r = e; }
    TP_END;
    return r;
}

tp_obj tp_max(TP) {
    tp_obj r = TP_OBJ();
    tp_obj e;
    TP_LOOP(e)
        if (tp_cmp(tp,r,e) < 0) { r = e; }
    TP_END;
    return r;
}

tp_obj tp_copy(TP) {
    tp_obj r = TP_OBJ();
    int type = r.type;
    if (type == TP_LIST) {
        return _tp_list_copy(tp,r);
    } else if (type == TP_DICT) {
        return _tp_dict_copy(tp,r);
    }
    tp_raise(tp_None,"tp_copy(%s)",TP_CSTR(r));
}


tp_obj tp_len_(TP) {
    tp_obj e = TP_OBJ();
    return tp_len(tp,e);
}


tp_obj tp_assert(TP) {
    int a = TP_NUM();
    if (a) { return tp_None; }
    tp_raise(tp_None,"%s","assert failed");
}

tp_obj tp_range(TP) {
    int a,b,c,i;
    tp_obj r = tp_list(tp);
    switch (tp->params.list.val->len) {
        case 1: a = 0; b = TP_NUM(); c = 1; break;
        case 2:
        case 3: a = TP_NUM(); b = TP_NUM(); c = TP_DEFAULT(tp_number(1)).number.val; break;
        default: return r;
    }
    if (c != 0) {
        for (i=a; (c>0) ? i<b : i>b; i+=c) {
            _tp_list_append(tp,r.list.val,tp_number(i));
        }
    }
    return r;
}


tp_obj tp_system(TP) {
    char const *s = TP_STR();
    int r = system(s);
    return tp_number(r);
}

tp_obj tp_istype(TP) {
    tp_obj v = TP_OBJ();
    char const *t = TP_STR();
    if (strcmp("string",t) == 0) { return tp_number(v.type == TP_STRING); }
    if (strcmp("list",t) == 0) { return tp_number(v.type == TP_LIST); }
    if (strcmp("dict",t) == 0) { return tp_number(v.type == TP_DICT); }
    if (strcmp("number",t) == 0) { return tp_number(v.type == TP_NUMBER); }
    if (strcmp("fnc",t) == 0) { return tp_number(v.type == TP_FNC && (v.fnc.ftype&2) == 0); }
    if (strcmp("method",t) == 0) { return tp_number(v.type == TP_FNC && (v.fnc.ftype&2) != 0); }
    tp_raise(tp_None,"is_type(%s,%s)",TP_CSTR(v),t);
}


tp_obj tp_float(TP) {
    tp_obj v = TP_OBJ();
    int ord = TP_DEFAULT(tp_number(0)).number.val;
    int type = v.type;
    if (type == TP_NUMBER) { return v; }
    if (type == TP_STRING) {
        if (strchr(TP_CSTR(v),'.')) { return tp_number(atof(TP_CSTR(v))); }
        return(tp_number(strtol(TP_CSTR(v),0,ord)));
    }
    tp_raise(tp_None,"tp_float(%s)",TP_CSTR(v));
}


tp_obj tp_save(TP) {
    char const *fname = TP_STR();
    tp_obj v = TP_OBJ();
    FILE *f;
    f = fopen(fname,"wb");
    if (!f) { tp_raise(tp_None,"tp_save(%s,...)",fname); }
    fwrite(v.string.val,v.string.len,1,f);
    fclose(f);
    return tp_None;
}

tp_obj tp_load(TP) {
    FILE *f;
    long l;
    tp_obj r;
    char *s;
    char const *fname = TP_STR();
    struct stat stbuf;
    stat(fname, &stbuf);
    l = stbuf.st_size;
    f = fopen(fname,"rb");
    if (!f) {
        tp_raise(tp_None,"tp_load(%s)",fname);
    }
    r = tp_string_t(tp,l);
    s = r.string.info->s;
    fread(s,1,l,f);
    fclose(f);
    return tp_track(tp,r);
}


tp_obj tp_fpack(TP) {
    tp_num v = TP_NUM();
    tp_obj r = tp_string_t(tp,sizeof(tp_num));
    *(tp_num*)r.string.val = v;
    return tp_track(tp,r);
}

tp_obj tp_abs(TP) {
    return tp_number(fabs(tp_float(tp).number.val));
}
tp_obj tp_int(TP) {
    return tp_number((long)tp_float(tp).number.val);
}
tp_num _roundf(tp_num v) {
    tp_num av = fabs(v); tp_num iv = (long)av;
    av = (av-iv < 0.5?iv:iv+1);
    return (v<0?-av:av);
}
tp_obj tp_round(TP) {
    return tp_number(_roundf(tp_float(tp).number.val));
}

tp_obj tp_exists(TP) {
    char const *s = TP_STR();
    struct stat stbuf;
    return tp_number(!stat(s,&stbuf));
}
tp_obj tp_mtime(TP) {
    char const *s = TP_STR();
    struct stat stbuf;
    if (!stat(s,&stbuf)) { return tp_number(stbuf.st_mtime); }
    tp_raise(tp_None,"tp_mtime(%s)",s);
}

int _tp_lookup(TP,tp_obj self, tp_obj k, tp_obj *meta) {
    int n = _tp_dict_find(tp,self.dict.val,k);
    if (n != -1) {
        *meta = self.dict.val->items[n].val;
        return 1;
    }
    if (self.dict.dtype && self.dict.val->meta.type == TP_DICT && _tp_lookup(tp,self.dict.val->meta,k,meta)) {
        if (self.dict.dtype == 2 && meta->type == TP_FNC) {
            *meta = tp_fnc_new(tp,meta->fnc.ftype|2,meta->fnc.val,self,meta->fnc.info->globals);
        }
        return 1;
    }
    return 0;
}

#define TP_META_BEGIN(self,name) \
    if (self.dict.dtype == 2) { \
        tp_obj meta; if (_tp_lookup(tp,self,tp_string(name),&meta)) {

#define TP_META_END \
        } \
    }
    
tp_obj tp_setmeta(TP) {
    tp_obj self = TP_TYPE(TP_DICT);
    tp_obj meta = TP_TYPE(TP_DICT);
    self.dict.val->meta = meta;
    return tp_None;
}

tp_obj tp_getmeta(TP) {
    tp_obj self = TP_TYPE(TP_DICT);
    return self.dict.val->meta;
}

tp_obj tp_object(TP) {
    tp_obj self = tp_dict(tp);
    self.dict.dtype = 2;
    return self;
}

tp_obj tp_object_new(TP) {
    tp_obj klass = TP_TYPE(TP_DICT);
    tp_obj self = tp_object(tp);
    self.dict.val->meta = klass;
    TP_META_BEGIN(self,"__init__");
        tp_call(tp,meta,tp->params);
    TP_META_END;
    return self;
}

tp_obj tp_object_call(TP) {
    tp_obj self;
    if (tp->params.list.val->len) {
        self = TP_TYPE(TP_DICT);
        self.dict.dtype = 2;
    } else {
        self = tp_object(tp);
    }
    return self;
}

tp_obj tp_getraw(TP) {
    tp_obj self = TP_TYPE(TP_DICT);
    self.dict.dtype = 0;
    return self;
}

tp_obj tp_class(TP) {
    tp_obj klass = tp_dict(tp);
    klass.dict.val->meta = tp_get(tp,tp->builtins,tp_string("object")); 
    return klass;
}

