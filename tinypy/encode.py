import tokenize

if not (str(1.0) == "1"):
    from boot import *

EOF,ADD,SUB,MUL,DIV,POW,AND,OR,CMP,GET,SET,NUMBER,STRING,GGET,GSET,MOVE,DEF,PASS,JUMP,CALL,RETURN,IF,DEBUG,EQ,LE,LT,DICT,LIST,NONE,LEN,POS,PARAMS,IGET,FILE,NAME,NE,HAS,RAISE,SETJMP,MOD,LSH,RSH,ITER,DEL,REGS = 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44

class DState:
    def __init__(self,code,fname):
        self.code, self.fname = code,fname
        self.lines = self.code.split('\n')

        self.stack,self.out,self._scopei,self.tstack,self._tagi,self.data = [],[('tag','EOF')],0,[],0,{}
        self.error = False
    def begin(self,gbl=False):
        if len(self.stack): self.stack.append((self.vars,self.r2n,self.n2r,self._tmpi,self.mreg,self.snum,self._globals,self.lineno,self.globals,self.cregs))
        else: self.stack.append(None)
        self.vars,self.r2n,self.n2r,self._tmpi,self.mreg,self.snum,self._globals,self.lineno,self.globals,self.cregs = [],{},{},0,0,str(self._scopei),gbl,-1,[],['regs']
        self._scopei += 1
        insert(self.cregs)
    def end(self):
        self.cregs.append(self.mreg)
        code(EOF)
        if len(self.stack) > 1:
            self.vars,self.r2n,self.n2r,self._tmpi,self.mreg,self.snum,self._globals,self.lineno,self.globals,self.cregs = self.stack.pop()
        else: self.stack.pop()


def insert(v): D.out.append(v)
def write(v):
    if istype(v,'list'):
        insert(v)
        return
    for n in range(0,len(v),4):
        insert(('data',v[n:n+4]))
def setpos(v):
    if '-nopos' in ARGV: return
    line,x = v
    if line == D.lineno: return
    text = D.lines[line-1]
    D.lineno = line
    val = text + "\0"*(4-len(text)%4)
    code_16(POS,len(val)/4,line)
    write(val)
def code(i,a=0,b=0,c=0):
    if not istype(i,'number'): raise
    if not istype(a,'number'): raise
    if not istype(b,'number'): raise
    if not istype(c,'number'): raise
    write(('code',i,a,b,c))
def code_16(i,a,b):
    if b < 0: b += 0x8000
    code(i,a,(b&0xff00)>>8,(b&0xff)>>0)
def get_code16(i,a,b):
    return ('code',i,a,(b&0xff00)>>8,(b&0xff)>>0)
def do_string(t,r=None):
    r = get_tmp(r)
    val = t['val'] + "\0"*(4-len(t['val'])%4)
    code_16(STRING,r,len(t['val']))
    write(val)
    return r
def do_number(t,r=None):
    r = get_tmp(r)
    code(NUMBER,r,0,0)
    write(fpack(number(t['val'])))
    return r

def get_tag():
    k = str(D._tagi)
    D._tagi += 1
    return k
def stack_tag():
    k = get_tag()
    D.tstack.append(k)
    return k
def pop_tag():
    D.tstack.pop()

def tag(*t):
    t = D.snum+':'+':'.join([str(v) for v in t])
    insert(('tag',t))
def jump(*t):
    t = D.snum+':'+':'.join([str(v) for v in t])
    insert(('jump',t))
def setjmp(*t):
    t = D.snum+':'+':'.join([str(v) for v in t])
    insert(('setjmp',t))
def fnc(*t):
    t = D.snum+':'+':'.join([str(v) for v in t])
    r = get_reg(t)
    insert(('fnc',r,t))
    return r

def map_tags():
    tags = {}
    out = []
    n = 0
    for item in D.out:
        if item[0] == 'tag':
            tags[item[1]] = n
            continue
        if item[0] == 'regs':
            out.append(get_code16(REGS,item[1],0))
            n += 1
            continue
        out.append(item)
        n += 1
    for n in range(0,len(out)):
        item = out[n]
        if item[0] == 'jump':
            out[n] = get_code16(JUMP,0,tags[item[1]]-n)
        elif item[0] == 'setjmp':
            out[n] = get_code16(SETJMP,0,tags[item[1]]-n)
        elif item[0] == 'fnc':
            out[n] = get_code16(DEF,item[1],tags[item[2]]-n)
    for n in range(0,len(out)):
        item = out[n]
        if item[0] == 'data':
            out[n] = item[1]
        elif item[0] == 'code':
            i,a,b,c = item[1:]
            out[n] = chr(i)+chr(a)+chr(b)+chr(c)
        else:
            raise str(('huh?',item))
        if len(out[n]) != 4:
            raise ('code '+str(n)+' is wrong length '+str(len(out[n])))
    D.out = out

def get_tmp(r=None):
    if r != None: return r
    return get_tmps(1)[0]
def get_tmps(t):
    rs = alloc(t)
    regs = range(rs,rs+t)
    for r in regs:
        set_reg(r,"$"+str(D._tmpi))
        D._tmpi += 1
    return regs
def alloc(t):
    s = ''.join(["01"[r in D.r2n] for r in range(0,min(256,D.mreg+t))])
    return s.index('0'*t)
def is_tmp(r):
    if r is None: return False
    return (D.r2n[r][0] == '$')
def un_tmp(r):
    n = D.r2n[r]
    free_reg(r)
    set_reg(r,'*'+n)
def free_tmp(r):
    if is_tmp(r): free_reg(r)
    return r
def free_tmps(r):
    for k in r: free_tmp(k)
def get_reg(n):
    if n not in D.n2r:
        set_reg(alloc(1),n)
    return D.n2r[n]
def get_clean_reg(n):
    if n in D.n2r: raise
    set_reg(D.mreg,n)
    return D.n2r[n]
def set_reg(r,n):
    D.n2r[n] = r; D.r2n[r] = n
    D.mreg = max(D.mreg,r+1)
def free_reg(r):
    n = D.r2n[r]; del D.r2n[r]; del D.n2r[n]

def imanage(orig,fnc):
    items = orig['items']
    orig['val'] = orig['val'][:-1]
    t = {'from':orig['from'],'type':'symbol','val':'=','items':[items[0],orig]}
    return fnc(t)

def infix(i,tb,tc,r=None):
    r = get_tmp(r)
    b,c = do(tb,r),do(tc)
    code(i,r,b,c)
    if r != b: free_tmp(b)
    free_tmp(c)
    return r
def ss_infix(ss,i,tb,tc,r=None):
    r = get_tmp(r)
    r2 = get_tmp()
    ss = do_number({'val':ss})
    t = get_tag()
    r = do(tb,r)
    code(EQ,r2,r,ss)
    code(IF,r2)
    jump(t,'else')
    jump(t,'end')
    tag(t,'else')
    r = do(tc,r)
    tag(t,'end')
    return r

def do_symbol(t,r=None):
    sets = ['=']
    isets = ['+=','-=','*=','/=']
    cmps = ['<','>','<=','>=','==','!=']
    metas = {
        '+':ADD,'*':MUL,'/':DIV,'**':POW,
        '-':SUB,'and':AND,'or':OR,
        '%':MOD,'>>':RSH,'<<':LSH,
        '&':AND,'|':OR,
    }
    if t['val'] == 'None':
        r = get_tmp(r)
        code(NONE,r)
        return r
    if t['val'] == 'True':
        return do_number({'from':t['from'],'val':1},r)
    if t['val'] == 'False':
        return do_number({'from':t['from'],'val':0},r)
    items = t['items']

    if t['val'] in ['and','or']:
        ss = int(t['val'] == 'or')
        return ss_infix(ss,metas[t['val']],items[0],items[1],r)
    if t['val'] in isets:
        return imanage(t,do_symbol)
    if t['val'] == 'is':
        return infix(EQ,items[0],items[1],r)
    if t['val'] == 'isnot':
        return infix(CMP,items[0],items[1],r)
    if t['val'] == 'not':
        return infix(EQ,{'from':t['from'],'type':'number','val':0},items[0],r)
    if t['val'] == 'in':
        return infix(HAS,items[1],items[0],r)
    if t['val'] == 'notin':
        r = infix(HAS,items[1],items[0],r)
        zero = do_number({'from':t['from'],'type':'number','val':0})
        code(EQ,r,r,free_tmp(zero))
        return r
    if t['val'] in sets:
        return do_set_ctx(items[0],items[1]);
    elif t['val'] in cmps:
        b,c = items[0],items[1]
        v = t['val']
        if v[0] in ('>','>='):
            b,c,v = c,b,'<'+v[1:]
        cd = EQ
        if v == '<': cd = LT
        if v == '<=': cd = LE
        if v == '!=': cd = NE
        return infix(cd,b,c,r)
    else:
        return infix(metas[t['val']],items[0],items[1],r)

def do_set_ctx(k,v):
    if k['type'] == 'name':
        if (D._globals and k['val'] not in D.vars) or (k['val'] in D.globals):
            c = do_string(k)
            b = do(v)
            code(GSET,c,b)
            free_tmp(c)
            free_tmp(b)
            return
        a = do_local(k)
        b = do(v)
        code(MOVE,a,b)
        free_tmp(b)
        return a
    elif k['type'] in ('tuple','list'):
        if v['type'] in ('tuple','list'):
            n,tmps = 0,[]
            for kk in k['items']:
                vv = v['items'][n]
                tmp = get_tmp(); tmps.append(tmp)
                code(MOVE,tmp,do(vv))
                n+=1
            n = 0
            for kk in k['items']:
                vv = v['items'][n]
                tmp = tmps[n]
                do_set_ctx(kk,{'from':vv['from'],'type':'reg','val':tmp})
                n += 1
            return

        r = do(v); un_tmp(r)
        n, tmp = 0, {'from':v['from'],'type':'reg','val':r}
        for tt in k['items']:
            do_set_ctx(tt,{'from':tmp['from'],'type':'get','items':[tmp,{'from':tmp['from'],'type':'number','val':str(n)}]})
            n += 1
        free_reg(r)
        return
    r = do(k['items'][0])
    rr = do(v)
    code(SET,r,do(k['items'][1]),rr)
    return rr

def manage_seq(i,a,items,sav=0):
    l = max(sav,len(items))
    n,tmps = 0,get_tmps(l)
    for tt in items:
        r = tmps[n]
        b = do(tt,r)
        if r != b:
            code(MOVE,r,b)
            free_tmp(b)
        n +=1
    if not len(tmps):
        code(i,a,0,0)
        return 0
    code(i,a,tmps[0],len(items))
    free_tmps(tmps[sav:])
    return tmps[0]

def p_filter(items):
    a,b,c,d = [],[],None,None
    for t in items:
        if t['type'] == 'symbol' and t['val'] == '=': b.append(t)
        elif t['type'] == 'args': c = t
        elif t['type'] == 'nargs': d = t
        else: a.append(t)
    return a,b,c,d

def do_import(t):
    for mod in t['items']:
        mod['type'] = 'string'
        v = do_call({'from':t['from'],'items':[
            {'from':t['from'],'type':'name','val':'import'},
            mod]})
        mod['type'] = 'name'
        do_set_ctx(mod,{'type':'reg','val':v})
def do_globals(t):
    for t in t['items']:
        if t['val'] not in D.globals:
            D.globals.append(t['val'])
def do_del(tt):
    for t in tt['items']:
        r = do(t['items'][0])
        code(DEL,r,do(t['items'][1]))

def do_call(t,r=None):
    r = get_tmp(r)
    items = t['items']
    fnc = do(items[0])
    a,b,c,d = p_filter(t['items'][1:])
    e = None
    if len(b) != 0 or d != None:
        e = do_dict({'items':[]}); un_tmp(e);
        for p in b: code(SET,e,do(p['items'][0]),do(p['items'][1]))
        if d: do_call({'items':[{'type':'name','val':'merge'},{'type':'reg','val':e},d['items'][0]]})
    manage_seq(PARAMS,r,a)
    if c != None: code(SET,r,do_string({'val':'*'}),do(c['items'][0]))
    if e != None: code(SET,r,do_symbol({'val':'None'}),e)
    code(CALL,r,fnc,r)
    return r

def do_name(t,r=None):
    if t['val'] in D.vars:
        return do_local(t,r)
    return do_global(t,r)

def do_local(t,r=None):
    if t['val'] not in D.vars:
        D.vars.append(t['val'])
    return get_reg(t['val'])

def do_global(t,r=None):
    r = get_tmp(r)
    c = do_string(t)
    code(GGET,r,c)
    free_tmp(c)
    return r



def do_def(tok,kls=None):
    items = tok['items']

    t = get_tag()
    rf = fnc(t,'end')

    D.begin()
    if 'from' in tok: setpos(tok['from'])
    r = do_local({'val':'__params'})
    do_info(items[0]['val'])
    a,b,c,d = p_filter(items[1]['items'])
    for p in a:
        v = do_local(p)
        code(GET,v,r,do_symbol({'val':'None'}))
    for p in b:
        v = do_local(p['items'][0])
        do(p['items'][1],v)
        code(IGET,v,r,do_symbol({'val':'None'}))
    if c != None:
        v = do_local(c['items'][0])
        code(GET,v,r,do_string({'val':'*'}))
    if d != None:
        e = do_local(d['items'][0])
        code(GET,e,r,do_symbol({'val':'None'}))
    do(items[2])
    D.end()

    tag(t,'end')

    if kls == None:
        if D._globals: do_globals({'items':[items[0]]})
        r = do_set_ctx(items[0],{'type':'reg','val':rf})
    else:
        rn = do_string(items[0])
        code(SET,kls,rn,rf)
        free_tmp(rn)

    free_tmp(rf)

def do_class(t):
    tok = t
    items = t['items']
    parent = None
    if items[0]['type'] == 'name':
        name = items[0]['val']
    else:
        name = items[0]['items'][0]['val']
        parent = items[0]['items'][1]['val']

    kls = do_dict({'items':[]})
    code(GSET,do_string({'val':name}),kls)

    init,_new = False,[]
    if parent:
        _new.append({'type':'call','items':[
            {'type':'get','items':[
                {'type':'name','val':parent},
                {'type':'string','val':'__new__'}
                ]
            },
            {'type':'name','val':'self'},
            ]})

    for fc in items[1]['items']:
        if fc['type'] != 'def': continue
        fn = fc['items'][0]['val']
        if fn == '__init__': init = True
        do_def(fc,kls)
        _new.append({'type':'symbol','val':'=','items':[
            {'type':'get','items':[
                {'type':'name','val':'self'},
                {'type':'string','val':fn}]},
            {'type':'call','items':[
                {'type':'name','val':'bind'},
                {'type':'get','items':[
                    {'type':'name','val':name},
                    {'type':'string','val':fn}]},
                {'type':'name','val':'self'}]}
            ]})

    do_def({'items':[
        {'val':'__new__'},
        {'items':[{'type':'name','val':'self'}]},
        {'type':'statements','items':_new},
        ]},kls)

    t = get_tag()
    rf = fnc(t,'end')
    D.begin()
    params = do_local({'val':'__params'})

    slf = do_local({'val':'self'})
    code(DICT,slf,0,0)

    do_call({'items':[
        {'type':'get','items':[
            {'type':'name','val':name},
            {'type':'string','val':'__new__'}
            ]
        },
        {'type':'name','val':'self'},
        ]})

    if init:
        tmp = get_tmp()
        code(GET,tmp,slf,do_string({'val':'__init__'}))
        code(CALL,get_tmp(),tmp,params)
    code(RETURN,slf)

    D.end()
    tag(t,'end')
    code(SET,kls,do_string({'val':'__call__'}),rf)




def do_while(t):
    items = t['items']
    t = stack_tag()
    tag(t,'begin')
    tag(t,'continue')
    r = do(items[0])
    code(IF,r)
    jump(t,'end')
    do(items[1])
    jump(t,'begin')
    tag(t,'break')
    tag(t,'end')
    pop_tag()

def do_for(tok):
    items = tok['items']

    reg = do_local(items[0])
    itr = do(items[1])
    i = do_number({'val':'0'})

    t = stack_tag(); tag(t,'loop'); tag(t,'continue')
    code(ITER,reg,itr,i); jump(t,'end')
    do(items[2])
    jump(t,'loop')
    tag(t,'break'); tag(t,'end'); pop_tag()

    free_tmp(i)

def do_comp(t,r=None):
    name = 'comp:'+get_tag()
    r = do_local({'val':name})
    code(LIST,r,0,0)
    key = {'from':t['from'],'type':'get','items':[
            {'from':t['from'],'type':'reg','val':r},
            {'from':t['from'],'type':'symbol','val':'None'}
            ]}
    ap = {'from':t['from'],'type':'symbol','val':'=','items':[key,t['items'][0]]}
    do_for({'from':t['from'],'items':[t['items'][1],t['items'][2],ap]})
    return r

def do_if(t):
    items = t['items']
    t = get_tag()
    n = 0
    for tt in items:
        tag(t,n)
        if tt['type'] == 'elif':
            a = do(tt['items'][0]); code(IF,a); free_tmp(a);
            jump(t,n+1)
            do(tt['items'][1])
        elif tt['type'] == 'else':
            do(tt['items'][0])
        else:
            raise
        jump(t,'end')
        n += 1
    tag(t,n)
    tag(t,'end')

def do_try(t):
    items = t['items']
    t = get_tag()
    setjmp(t,'except')
    do(items[0])
    jump(t,'end')
    tag(t,'except')
    do(items[1]['items'][1])
    tag(t,'end')

def do_return(t):
    if 'items' in t: r = do(t['items'][0])
    else: r = do_symbol({'from':t['from'],'val':'None'})
    code(RETURN,r)
    free_tmp(r)
    return
def do_raise(t):
    if 'items' in t: r = do(t['items'][0])
    else: r = do_symbol({'from':t['from'],'val':'None'})
    code(RAISE,r)
    free_tmp(r)
    return

def do_statements(t):
    for tt in t['items']: free_tmp(do(tt))

def do_list(t,r=None):
    r = get_tmp(r)
    manage_seq(LIST,r,t['items'])
    return r

def do_dict(t,r=None):
    r = get_tmp(r)
    manage_seq(DICT,r,t['items'])
    return r

def do_get(t,r=None):
    items = t['items']
    return infix(GET,items[0],items[1],r)

def do_break(t): jump(D.tstack[-1],'break')
def do_continue(t): jump(D.tstack[-1],'continue')
def do_pass(t): code(PASS)

def do_info(name='?'):
    if '-nopos' in ARGV: return
    code(FILE,free_tmp(do_string({'val':D.fname})))
    code(NAME,free_tmp(do_string({'val':name})))
def do_module(t):
    do_info()
    do(t['items'][0])
def do_reg(t,r=None): return t['val']

fmap = {
    'module':do_module,'statements':do_statements,'def':do_def,
    'return':do_return,'while':do_while,'if':do_if,
    'break':do_break,'pass':do_pass,'continue':do_continue,'for':do_for,
    'class':do_class,'raise':do_raise,'try':do_try,'import':do_import,
    'globals':do_globals,'del':do_del,
}
rmap = {
    'list':do_list, 'tuple':do_list, 'dict':do_dict, 'slice':do_list,
    'comp':do_comp, 'name':do_name,'symbol':do_symbol,'number':do_number,
    'string':do_string,'get':do_get, 'call':do_call, 'reg':do_reg,
}

def do(t,r=None):
    if 'from' in t: setpos(t['from'])
    try:
        if t['type'] in rmap:
            return rmap[t['type']](t,r)
        return fmap[t['type']](t)
    except:
        if D.error: raise
        D.error = True
        if 'from' not in t: print("uh ohh",t['type'])
        tokenize.u_error('dump',D.code,t['from'])

def encode(fname,s,t):
    t = {'from':(1,1),'type':'module','val':'module','items':[t]}
    global D
    s = tokenize.clean(s)
    D = DState(s,fname)
    D.begin(True)
    do(t)
    D.end()
    map_tags()
    out = D.out; D = None
    return ''.join(out)

