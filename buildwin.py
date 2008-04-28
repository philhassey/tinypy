import os, sys, struct

# How to compile on windows with Visual Studio:
# Call the batch script that sets environement variables for Visual Studio and
# then run this script.
# For VS 2005 the script is:
# "C:\Program Files\Microsoft Visual Studio 8\Common7\Tools\vsvars32.bat"
# For VS 2008: "C:\Program Files\Microsoft Visual Studio 9.0\Common7\Tools\vsvars32.bat"
# Doesn't compile with vc6 (no variadic macros)

ARGV = sys.argv

def number(v):
    if type(v) is str and v[0:2] == '0x':
        v = int(v[2:],16)
    return float(v)

def istype(v,t):
    if t == 'string': return isinstance(v,str)
    elif t == 'list': return (isinstance(v,list) or isinstance(v,tuple))
    elif t == 'dict': return isinstance(v,dict)
    elif t == 'number': return (isinstance(v,float) or isinstance(v,int))
    raise '?'

def boot_init():
    global FTYPE 
    f = open('tp.h','r').read()
    FTYPE = 'f'
    if 'double tp_num' in f: FTYPE = 'd'

boot_init()

def fpack(v):
    return struct.pack(FTYPE,v)

def system(cmd):
    return os.system(cmd)

def load(fname):
    f = open(fname,'rb')
    r = f.read()
    f.close()
    return r

def save(fname,v):
    f = open(fname,'wb')
    f.write(v)
    f.close()

def do_cmd(cmd):
    print cmd
    r = os.system(cmd)
    if r:
        print 'exit',r
        sys.exit(r)

def chksize():
    import mk64k
    t1,t2 = 0,0
    for fname in [
        'tokenize.py','parse.py','encode.py','py2bc.py',
        'tp.h','list.c','dict.c','misc.c','string.c','builtins.c',
        'gc.c','ops.c','vm.c','tp.c','tpmain.c',
        ]:
        f = open(fname,'r'); t1 += len(f.read()); f.close()
        txt = mk64k.shrink(fname)
        t2 += len(txt)
    print "#",t1,t2,t2-65536
    return t2

MODS = ['tokenize','parse','encode','py2bc']

def build_bc(opt=False):
    out = []
    for mod in MODS:
        out.append("""unsigned char tp_%s[] = {"""%mod)
        fname = mod+".tpc"
        data = open(fname,'rb').read()
        cols = 16
        for n in xrange(0,len(data),cols):
            out.append(",".join([str(ord(v)) for v in data[n:n+cols]])+',')
        out.append("""};""")
    out.append("")
    f = open('bc.c','wb')
    f.write('\n'.join(out))
    f.close()

def build_tp():
    out = []
    out.append("/*")
    out.extend([v.rstrip() for v in open('LICENSE.txt','r')])
    out.append("*/")
    out.append("")
    
    out.append("#ifndef TINYPY_H")
    out.append("#define TINYPY_H")
    out.extend([v.rstrip() for v in open('tp.h','r')])
    for fname in ['list.c','dict.c','misc.c','string.c','builtins.c',
        'gc.c','ops.c','vm.c','tp.c']:
        for line in open(fname,'r'):
            line = line.rstrip()
            if not len(line): continue
            if line[0] == ' ': continue
            if line[0] == '\t': continue
            if line[-1] != '{': continue
            if 'enum' in line: continue
            if '=' in line: continue
            if '#' in line: continue
            line = line.replace('{',';') 
            out.append(line)
    out.append("#endif")
    out.append('')
    f = open('tinypy.h','w')
    f.write('\n'.join(out))
    f.close()
    
    # we leave all the tinypy.h stuff at the top so that
    # if someone wants to include tinypy.c they don't have to have
    # tinypy.h cluttering up their folder
    
    for mod in MODS:
        out.append("""extern unsigned char tp_%s[];"""%mod)

                
    for fname in ['list.c','dict.c','misc.c','string.c','builtins.c',
        'gc.c','ops.c','vm.c','tp.c','bc.c']:
        for line in open(fname,'r'):
            line = line.rstrip()
            if line.find('#include "') != -1: continue
            out.append(line)
    out.append('')
    f = open('tinypy.c','w')
    f.write('\n'.join(out))
    f.close()

def bootstrap():
    mods = MODS[:]; mods.append('tests')
    do_cmd('cl vmmain.c /D "inline=" /Od /Zi /Fdvm.pdb /Fmvm.map /Fevm.exe')
    do_cmd('python tests.py -win')
    for mod in mods: do_cmd('python py2bc.py %s.py %s.tpc'%(mod,mod))
    do_cmd('vm.exe tests.tpc -win')
    for mod in mods: do_cmd('vm.exe py2bc.tpc %s.py %s.tpc'%(mod,mod))
    build_bc()
    do_cmd('cl /Od tpmain.c /D "inline=" /Zi /Fdtinypy.pdb /Fmtinypy.map /Fetinypy.exe')
    #second pass - builts optimized binaries and stuff
    do_cmd('tinypy.exe tests.py -win')
    for mod in mods: do_cmd('tinypy.exe py2bc.py %s.py %s.tpc -nopos'%(mod,mod))
    build_bc(True)
    do_cmd('cl /Os vmmain.c /D "inline=__inline" /D "NDEBUG" /Gy /GL /Zi /Fdvm.pdb /Fmvm.map /Fevm.exe /link /opt:ref /opt:icf')
    do_cmd('cl /Os tpmain.c   /D "inline=__inline" /D "NDEBUG" /Gy /GL /Zi /Fdtinypy.pdb /Fmtinypy.map /Fetinypy.exe /link /opt:ref /opt:icf')
    do_cmd("tinypy.exe tests.py -win")
    do_cmd("dir *.exe")

if __name__ == '__main__':
    bootstrap()
