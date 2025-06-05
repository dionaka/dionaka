import turtle as t
import math
from time import sleep

#mul=float(input('输入图片输入倍数'))
mul=2.5
t.speed(0)
t.mode('standard')
t.color('blue')
t.setup(1000*mul,1500*mul,0,0)
t.pensize(0)

def tp(x,y):
    t.penup()
    t.setpos(x*mul,y*mul)
    t.pendown()

def c(r,op,ed):
    t.setheading((op+90))
    if ed>=op:
        t.circle(r*mul,ed-op)
    else:
        t.circle(r*mul,ed+360-op)

#精准画圆
def tpc(x,y,r,op,ed):
    rad=math.radians(op)
    x+=r*math.cos(rad)
    y+=r*math.sin(rad)
    tp(x,y)
    c(r,op,ed)

def l(x1,y1,x2,y2):
    width=211
    height=122
    x1-=width
    x2-=width
    y1-=height
    y2-=height
    tp(x1,y1)
    t.setpos(x2*mul,y2*mul)

def ed():
    t.penup()
    t.setpos(1000*mul,1500*mul)
    sleep(100)
l(0,244.475,0,0)
l(0,244.475,423.333,244.475)
l(423.333,244.475,423.333,0)
l(0,0,423.333,0)
l(75.9311,139.5413,75.9311,56.6839)
l(75.9311,56.6839,84.7137,59.0011)
l(84.7137,59.0011,84.7137,134.478)
l(84.7137,134.478,75.9311,139.5413)
l(78.4563,155.3244,78.4563,138.0855)
l(80.6227,153.5193,80.6227,136.8365)
l(78.4664,21.7647,78.4664,57.3528)
l(80.2928,22.069,80.2928,57.8347)
l(72.1348,20.7299,82.5455,20.7299)
l(70.7955,0,72.1348,20.7299)
l(82.5455,20.7299,82.5455,0)
l(86.4886,22.5844,82.5455,20.7299)
l(72.1348,20.7299,75.8096,22.5844)
l(75.8096,22.5844,86.4886,22.5844)
l(88.9,0,86.4886,22.58)
l(278.9472,79.3724,423.3333,79.3724)
