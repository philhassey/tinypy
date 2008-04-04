#import sdl

#SW,SH = 640,480
SW,SH = 320,240
pal = [((min(255,n)*65536)+(min(255,n*3/2)*256)+(min(255,n*2))) for n in range(0,256)]

def julia(mypal,ca,cb):
    for y in range(0,SH,2):
        for x in range(0,SW,2):
            i = 0
            a = ((x/SW*4)-2)
            b = ((y/SH*4)-2)
            while i < 15 and a*a+b*b<4:
                na=a*a-b*b+ca
                nb=2.0*a*b+cb
                a,b=na,nb
                i += 1
            c = mypal[i*16]
            set_pixel(x,y,c); set_pixel(x+1,y,c);
            set_pixel(x,y+1,c); set_pixel(x+1,y+1,c)
            

myjulia = bind(julia,pal)

print(SW,SH)
set_mode(SW,SH)
_quit = 0
while _quit == 0:
    t = get_ticks()
    m = get_mouse_pos()
    ca =m.x/SW * 2.0 - 1.0
    cb =m.y/SH * 2.0 - 1.0

    e = gfx_get_event()
    while e is not None:
        if e.type == 12 or e.type == 2:
            _quit = 1
        e = gfx_get_event()
    myjulia(ca,cb)
    update(0,0,SW,SH)
    print((get_ticks()-t))
