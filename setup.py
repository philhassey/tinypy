import os
import sys

VARS = {}
TOPDIR = os.path.abspath(os.path.dirname(__file__))

def main():
    if len(sys.argv) < 2:
        print HELP
        return
    
    cmd = sys.argv[1]
    if cmd == 'linux':
        vars_linux()
        build_gcc()
    elif cmd == 'mingw':
        vars_windows()
        build_gcc()
    elif cmd == 'vs':
        build_vs()
    elif cmd == '64k':
        build_64k()
    elif cmd == 'tinypy':
        build_tinypy()
    else:
        print 'invalid command'

HELP = """
python setup.py command [options]

Commands:
    linux - build tinypy for linux
    mingw - build tinypy for mingw under windows
    vs - build tinypy using Visual Studio 2005 / 2008
    
    64k - build a 64k version of the tinypy source 
    tinypy - build tinypy.c and tinypy.h
    
    build - build CPython module *
    install - install CPython module *
    
Options:
    n/a
    
* vaporware
"""

def vars_linux():
    VARS['$RM'] = 'rm -f'
    VARS['$VM'] = './vm'
    VARS['$TINYPY'] = './tinypy'
    VARS['$FLAGS'] = ''
    VARS['$SDL'] = '`sdl-config --cflags --libs`'
    VARS['$SYS'] = '-linux'

def vars_windows():
    VARS['$RM'] = 'del'
    VARS['$VM'] = 'vm'
    VARS['$TINYPY'] = 'tinypy'
    VARS['$FLAGS'] = '-mwindows -lmingw32'
    VARS['$SDL'] = '-lSDLmain -lSDL'
    VARS['$SYS'] = '-mingw32'


def do_cmd(cmd):
    for k,v in VARS.items():
        cmd = cmd.replace(k,v)
    if '$' in cmd:
        print 'vars_error',cmd
        sys.exit(-1)
    
    print cmd
    r = os.system(cmd)
    if r:
        print 'exit_status',r
        sys.exit(r)

def chksize():
    import mk64k
    t1,t2 = 0,0
    for fname in [
        'tokenize.py','parse.py','encode.py','py2bc.py',
        'tp.h','list.c','dict.c','misc.c','string.c','builtins.c',
        'gc.c','ops.c','vm.c','tp.c','tpmain.c',
        ]:
        fname = os.path.join(os.path.dirname(__file__),'tinypy',fname)
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
    
def open_tinypy(fname,*args):
    return open(os.path.join(TOPDIR,'tinypy',fname),*args)
    
def build_tp():
    out = []
    out.append("/*")
    out.extend([v.rstrip() for v in open(os.path.join(TOPDIR,'LICENSE.txt'),'r')])
    out.append("*/")
    out.append("")
    
    out.append("#ifndef TINYPY_H")
    out.append("#define TINYPY_H")
    out.extend([v.rstrip() for v in open_tinypy('tp.h','r')])
    for fname in ['list.c','dict.c','misc.c','string.c','builtins.c',
        'gc.c','ops.c','vm.c','tp.c']:
        for line in open_tinypy(fname,'r'):
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
    f = open_tinypy('tinypy.h','w')
    f.write('\n'.join(out))
    f.close()
    
    # we leave all the tinypy.h stuff at the top so that
    # if someone wants to include tinypy.c they don't have to have
    # tinypy.h cluttering up their folder
    
    for mod in MODS:
        out.append("""extern unsigned char tp_%s[];"""%mod)

                
    for fname in ['list.c','dict.c','misc.c','string.c','builtins.c',
        'gc.c','ops.c','vm.c','tp.c','bc.c']:
        for line in open_tinypy(fname,'r'):
            line = line.rstrip()
            if line.find('#include "') != -1: continue
            out.append(line)
    out.append('')
    f = open_tinypy('tinypy.c','w')
    f.write('\n'.join(out))
    f.close()
    
    

    #compat = '-compat' in sys.argv
    #if compat: do_cmd("gcc -std=c89 -Wall -g vmmain.c $FLAGS -lm -o vm-c89")
    #if compat: do_cmd("g++ -Wall -g vmmain.c $FLAGS -lm -o vm-cpp")
    #if compat: do_cmd("gcc -std=c89 -Wall -g tpmain.c $FLAGS -lm -o tinypy-c89")
    #if compat: do_cmd("g++ -Wall -g tpmain.c $FLAGS -lm -o tinypy-cpp")

def build_gcc():
    mods = MODS[:]; mods.append('tests')
    os.chdir(os.path.join(TOPDIR,'tinypy'))
    do_cmd("gcc -Wall -g vmmain.c $FLAGS -lm -o vm")
    do_cmd('python tests.py $SYS')
    for mod in mods: do_cmd('python py2bc.py %s.py %s.tpc'%(mod,mod))
    do_cmd('$VM tests.tpc $SYS')
    for mod in mods: do_cmd('$VM py2bc.tpc %s.py %s.tpc'%(mod,mod))
    build_bc()
    do_cmd("gcc -Wall -g tpmain.c $FLAGS -lm -o tinypy")
    #second pass - builts optimized binaries and stuff
    do_cmd('$TINYPY tests.py $SYS')
    for mod in mods: do_cmd('$TINYPY py2bc.py %s.py %s.tpc -nopos'%(mod,mod))
    build_bc(True)
    do_cmd("gcc -Wall -O2 tpmain.c $FLAGS -lm -o tinypy")
    do_cmd('$TINYPY tests.py $SYS')
    print("# OK - we'll try -O3 for extra speed ...")
    do_cmd("gcc -Wall -O3 tpmain.c $FLAGS -lm -o tinypy")
    do_cmd('$TINYPY tests.py $SYS')
    print("# OK")
    build_tp()
    #do_cmd("gcc -Wall -O3 tinypy-sdl.c tinypy.c $FLAGS $SDL -lm -o tinypy-sdl")

if __name__ == '__main__':
    main()
