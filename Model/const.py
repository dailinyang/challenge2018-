from pygame.math import Vector2 as Vec
import View.const as viewconst
from math import sqrt, ceil
PlayerNum = 4
MaxManualPlayerNum = 4

#dir const
dirConst = [
    [0,0],              # can't movw
    [0,-1],             # Up
    [0.707,-0.707],     # Right up
    [1,0],              # Right
    [0.707,0.707],      # Right down
    [0,1],              # Down
    [-0.707,0.707],     # Left down
    [-1,0],             # Left
    [-0.707,-0.707]     # Left up
]
dirBounce = [
    [0, 1, 8, 7, 6, 5, 4, 3, 2], # x bouce
    [0, 5, 4, 3, 2, 1, 8, 7, 6], # y bouce
]

eps=1e-7


#####################  Vec direction #####################
Vec_dir = [
    Vec( 0,1 ), ##left
    Vec( 1,0 ), ##up
    Vec( 0,-1 ),  ##right
    Vec( -1,0 )   ##down
]

#####################  white ball const  #####################
wb_init_num = 15
wb_max_num  = 50
wb_born_period = 1 #second
wb_radius   = 10
#####################  white ball const  #####################


def init_grav_list(g_list):
    # --------------------------- Grav 0 --------------------------- 
    grav_st=85
    grav_r = 75
    grav_dr=(800-grav_st*2)/4
    for i in range(5):
        if i % 2 == 0:
            for j in range(3):
                g_list[0].append([Vec(grav_st+grav_dr*2*j,grav_st+grav_dr*i), grav_r])
        else:
            for j in range(2):
                g_list[0].append([Vec(grav_st + grav_dr + grav_dr * 2 * j, 0.5+grav_st+grav_dr*i), grav_r])
    # --------------------------- Grav 1 --------------------------- 
    grav_r=55
    grav_circle_num=int(viewconst.GameSize[0] / sqrt(2) / grav_r - sqrt(2) + 1)
    shift_size=int((viewconst.GameSize[0]-2*grav_r)/(grav_circle_num-1))
    for i in range(grav_circle_num):
        g_list[1].append([Vec(viewconst.GameSize[0] - grav_r - (shift_size*i), grav_r + (shift_size*i)),grav_r-6])
    # --------------------------- Grav 2 --------------------------- 
    g_list[2].append([Vec(400,400),200])
    g_list[2].append([Vec(100,100),80])
    g_list[2].append([Vec(100,700),80])
    g_list[2].append([Vec(700,100),80])
    g_list[2].append([Vec(700,700),80])
    g_list[2].append([Vec(208,208),55])
    g_list[2].append([Vec(208,592),55])
    g_list[2].append([Vec(592,208),55])
    g_list[2].append([Vec(592,592),55])
    # --------------------------- Grav 3 --------------------------- 
    grav_st=80
    grav_r = 50
    grav_dr=(800-grav_st*2)/5
    g_list[3].append([Vec(135,135),grav_r*2+20])
    g_list[3].append([Vec(800-135,800-135),grav_r*2+20])
    for i in range(4):
        g_list[3].append([Vec(grav_st+grav_dr*(i+2),grav_st),grav_r])
        g_list[3].append([Vec(grav_st+grav_dr*i,800-grav_st),grav_r])
    for i in range(1,4):
        g_list[3].append([Vec(grav_st,grav_st+grav_dr*(i+1)),grav_r])
        g_list[3].append([Vec(800-grav_st,grav_st+grav_dr*i),grav_r])
    # --------------------------- Grav 4 --------------------------- 
    g_list[4].append([Vec(630,300),150])
    g_list[4].append([Vec(250,570),100])
    g_list[4].append([Vec(80,400),70])
    g_list[4].append([Vec(430,100),50])
    g_list[4].append([Vec(80,700),50])
    g_list[4].append([Vec(370,300),60])
    g_list[4].append([Vec(200,90),80])
    g_list[4].append([Vec(120,250),40])
    g_list[4].append([Vec(700,700),90])




def next_grav():
    '''change the gravity map cyclicly'''
    global grav
    next_grav.counter += 1
    grav = grav_list[next_grav.counter%len(grav_list)]
next_grav.counter = 0



#####################     head const     #####################


max_dash_time = 50

normal_speed = 2
#dash_speed = normal_speed * 3
dash_speed_multiplier = 3
dash_speed = normal_speed * dash_speed_multiplier
pos_log_max = 25 / normal_speed + 1
init_r = 40
init_no_wb_r = 80
head_radius = 11
#the grav now is for debug
grav_list = [ [] for _ in range(5) ]

grav = grav_list[0]
init_grav_list(grav_list)


init_r=40
#####################     head const     #####################

#####################    body const    ######################
body_radius = 10
body_gap = 6
dash_radius = head_radius + body_radius
dash_cool=30
#####################    body const    ######################

#####################  bullet const  #####################
bullet_radius = 8
bullet_a = 0.1
bullet_speed0 = normal_speed * 7

suddendeath_ticks = viewconst.FramePerSec * 40
suddendeath_speed = normal_speed
freq = 7
#####################  bullet const  #####################

#####################  item const #####################

PROP_TYPE_EXPLOSIVE = 0
PROP_TYPE_MULTIBULLET = 1
PROP_TYPE_BIGBULLET = 2
item_max = 7
item_born_period = 3#second
item_init_num = 1
item_radius = 12

explosive_radius = 150.0

bigbullet_r = bullet_radius * 4


#####################  item const #####################

wb_speed = normal_speed * 1.5
wb_fast_speed = dash_speed * 1.5

bombtime = 60
bomb_speed = bullet_speed0
bomb_a = bullet_a 
bomb_amount = 20

