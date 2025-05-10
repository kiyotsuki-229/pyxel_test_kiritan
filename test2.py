import pyxel

SPEED=5
SIZE=48
DEBUG=False
DEBUG_VALUE=[]

class player:
    player1=(0,0,SIZE,SIZE)
    player_map=[0,0,1,0]
    u_s=1
    uita=False
    init1=True
    falling=True
    on_g=False

class block:
    def __init__(self,x1,y1):
        self.block1=(x1,y1)

class coin:
    working=True
    POINT=1
    def __init__(self,x,y):
        self.item1=(0,0,SIZE,SIZE)
        self.item1_map=[x,y,0,0]
    def move(self,x,y):
        self.X+=x
        self.Y+=y
    def gotten(self,pl):
        x,y,u,v=pl.player_map
        if not (x+SIZE<self.item1_map[0] or x>self.item1_map[0]+SIZE or y+SIZE<self.item1_map[1] or y>self.item1_map[1]+SIZE):
            self.working=False
            return self.POINT
        return 0


def upper(x,y,obj):
    if (not y+SIZE<=obj.block1[1]) and (y+SIZE-obj.block1[1]<24):
        y=obj.block1[1]-SIZE
    elif (not y>=obj.block1[1]+SIZE) and (obj.block1[1]+SIZE-y<24):
        y=obj.block1[1]+SIZE
    if (not x+SIZE<=obj.block1[0]) and (x+SIZE-obj.block1[0]<24):
        x=obj.block1[0]-SIZE
    elif (not x>=obj.block1[0]+SIZE) and (obj.block1[0]+SIZE-x<24):
        x=obj.block1[0]+SIZE
    return x,y


def is_c(x,y,uita,objs,pl):
    global SIZE,DEBUG
    for obj in objs:
        if not (x+SIZE<=obj.block1[0] or x>=obj.block1[0]+SIZE or y+SIZE<=obj.block1[1] or y>=obj.block1[1]+SIZE):
            return True
        else:
            continue
    return False

def fall(x,y,objs,uita,dy):
    global DEBUG_VALUE
    for obj in objs:
        if (x+SIZE<=obj.block1[0] or x>=obj.block1[0]+SIZE):
            continue
        elif (not (x+SIZE<=obj.block1[0] or x>=obj.block1[0]+SIZE)) and abs(obj.block1[1]-(y+SIZE))<5:
            if ((not y+SIZE<=obj.block1[1]) and (y+SIZE-obj.block1[1]<24)) or dy>=0:
                y=obj.block1[1]-SIZE
                return False,True,y
            elif dy<0:
                return True,False,y
            return True,True,y
    return True,False,y


def push_back(x,y,dx,dy,bl,uita,pl):
    global SPEED
    for _ in range(pyxel.ceil(abs(dy))):
        step=max(-1*SPEED,min(SPEED,dy))
        j=is_c(x,y+step,uita,bl,pl)
        if j:
            break
        y+=step
        dy-=step
    for _ in range(pyxel.ceil(abs(dx))):
        step=max(-1*SPEED,min(SPEED,dx))
        j=is_c(x+step,y,uita,bl,pl)
        if j:
            break
        x+=step
        dx-=step
    return x,y,uita

class App:
    size=SIZE
    mode1=0
    sk=True
    n1,n2=SPEED,SPEED
    it=[]
    point=0

    umplus10=pyxel.Font("umplus_j10r.bdf")
    umplus12=pyxel.Font("umplus_j12r.bdf")
    
    def __init__(self):
        pyxel.init(640,480,title='test1')

        pyxel.load('data1.pyxres')
        self.pl=player()
        self.bl=[]
        for i in range(3,9):
            self.bl.append(block(self.size*i,400))
            if i>6:
                self.bl.append(block(self.size*i,352))


        for i in range(4):
            self.it.append(coin(i*self.size,300))
        self.it.append(coin(9999,9999))
        pyxel.screen_mode(1)

        pyxel.run(self.update,self.draw)

    def update(self):
        global DEBUG,DEBUG_VALUE
        if not self.pl.falling:
            self.pl.u_s=0

        
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        x,y,u,v=self.pl.player_map
        dx,dy=0,0
        if pyxel.btn(pyxel.KEY_SPACE) and self.sk:
            self.mode1=(self.mode1+1)%2
            self.sk=False
        elif not (self.sk or pyxel.btn(pyxel.KEY_SPACE)):
            self.sk=True

        
        if self.pl.falling:
            dy+=self.pl.u_s
            self.pl.u_s+=1
            
        if pyxel.btn(pyxel.KEY_UP):
            self.pl.uita=True
            self.pl.falling=True
            self.pl.on_g=False
            
        if pyxel.btn(pyxel.KEY_LEFT) and (self.pl.player_map[0]>0):
            dx=-1*SPEED
            u,v=0,1
        if pyxel.btn(pyxel.KEY_RIGHT) and (self.pl.player_map[0]+self.size<pyxel.width):
            dx=SPEED
            u,v=0,2
            
        if u==0 and ((self.pl.u_s<3*SPEED and not self.pl.uita) or (self.pl.u_s>=3*SPEED and self.pl.uita)):
            u+=[1,0,1,2][pyxel.frame_count//5%4]
        if self.pl.uita:
            dy-=3*SPEED
            
        x,y,self.pl.uita=push_back(x,y,dx,dy,self.bl,self.pl.uita,self.pl)
        self.pl.falling,self.pl.on_g,y=fall(x,y,self.bl,self.pl.uita,dy)

        
        
        x=min(max(x,0),pyxel.width-self.size)
        y=min(max(y,0),pyxel.height-self.size)
        if y>=pyxel.height-self.size or self.pl.on_g:
            self.pl.u_s=0
            self.pl.uita=False
            self.pl.init1=False
            self.pl.falling=False
            self.pl.on_g=True
        
        self.pl.player_map=[x,y,u,v]
        DEBUG_VALUE=f'judge:{y>=pyxel.height-self.size or self.pl.on_g},{y}>={pyxel.height}-{self.size} or {self.pl.on_g}'

        #debug plyaer1(x1,y1,x2,y2) player_map(x,y,~~)
        if pyxel.btn(pyxel.KEY_D) and not DEBUG:
            DEBUG=False
        elif not(pyxel.btn(pyxel.KEY_D) or DEBUG):
            DEBUG=True

        if DEBUG:
            pass
            #print(self.pl.u_s)

        self.it[0].item1_map[0]+=self.n1
        self.it[0].item1_map[1]+=self.n2
        if self.it[0].item1_map[0]>pyxel.width-self.size or self.it[0].item1_map[0]<0:
            self.n1*=-1
        if self.it[0].item1_map[1]>pyxel.height-self.size or self.it[0].item1_map[1]<0:
            self.n2*=-1
        numlis=[]
        c=0
        for i in self.it:
            jud=i.gotten(self.pl)
            if jud:
                numlis.append(c)
            c+=1
            self.point+=jud
        for i in numlis:
            del self.it[i]
    def draw(self):
        pyxel.cls(8)

        x,y,u,v=self.pl.player_map
        pyxel.blt(x,y-1,self.mode1,self.pl.player1[0]+u*self.size,self.pl.player1[1]+v*self.size,self.pl.player1[2],self.pl.player1[3],11)

        
        for i in self.it:
            x,y,u,v=i.item1_map
            pyxel.blt(x,y-1,2,i.item1[0]+u*self.size,i.item1[1]+v*self.size,i.item1[2],i.item1[3],11)
        for i in self.bl:
            pyxel.blt(i.block1[0],i.block1[1],2,0,self.size,self.size,self.size,5)

        pyxel.text(21, 8, str(DEBUG_VALUE), 1, self.umplus10)
        pyxel.text(21,56,str(self.point),5,self.umplus12)

App()
