import turtle as t
import math
from time import sleep
import cv2
import numpy as np

# mul = float(input('输入图片输入倍数: ')) # 移除手动输入mul
turtle_speed = int(input('输入绘画速度 (0-10, 0最快): '))
t.speed(turtle_speed)
t.mode('standard')
t.color('blue')
# t.setup(1000*mul, 1500*mul, 0, 0) # 移除旧的setup调用
t.pensize(2)

# 定义全局变量并初始化
auto_mul = 1.0 
global_offset_x = 0
global_offset_y = 0

def tp(x, y):
    # Use calculated global scale and offset for setpos
    t.penup()
    t.setpos(x*auto_mul + global_offset_x, -(y*auto_mul) + global_offset_y)  
    # Note: tp function no longer includes pendown or penup

def draw_contours(contours):
    # Add print info to check number of contours and points in the first contour
    print(f"开始绘制 {len(contours)} 个轮廓。")
    if len(contours) > 0 and len(contours[0]) > 0:
        print(f"第一个轮廓有 {len(contours[0])} 个点。")

    for cnt in contours:
        if len(cnt) < 2:
            continue
        # Move to the first point (using tp, pen is up at this point)
        x0, y0 = cnt[0][0]
        tp(x0, y0)
        t.pendown() # After moving to the first point, put the pen down
        
        # Draw lines sequentially (use setpos for subsequent points, pen is down)
        for pt in cnt[1:]:
            x, y = pt[0]
            # Use the calculated global offset for setpos
            t.setpos(x*auto_mul + global_offset_x, -(y*auto_mul) + global_offset_y)
        t.penup() # After drawing a contour, lift the pen up

# Function to calculate and set global scale and offset
def calculate_scale_and_offset(original_width, original_height, screen_width, screen_height):
    global auto_mul, global_offset_x, global_offset_y

    if screen_width > 0 and screen_height > 0:
        scale_w = screen_width / original_width
        scale_h = screen_height / original_height
        auto_mul = min(scale_w, scale_h) * 0.95 # Leave a small margin
        
        # Calculate offset to map image top-left (0,0) to Turtle top-left (-screen_width/2, screen_height/2)
        global_offset_x = -screen_width / 2.0
        global_offset_y = screen_height / 2.0  # Y-axis is positive upwards in Turtle

        print(f"根据屏幕和图片尺寸自动计算的缩放倍数 auto_mul: {auto_mul}")
        print(f"计算的偏移量 global_offset_x: {global_offset_x}, global_offset_y: {global_offset_y}")
    else:
        # Fallback if screen dimensions are not available
        auto_mul = 0.5 # Default value
        global_offset_x = -original_width * auto_mul / 2 # Simple top-left estimation
        global_offset_y = original_height * auto_mul / 2 # Simple top-left estimation (Y-axis inverted)
        print("警告：无法获取屏幕尺寸，使用默认缩放倍数 0.5 和简单左上角估算。请确保图片不太大。")


# 1. Read image
img = cv2.imread('your.png', 0)  # 0 for grayscale

# Automatically set up turtle canvas to full screen and calculate appropriate scale and offset

if img is not None:
    print("图片your.png读取成功。")
    original_height, original_width = img.shape

    # Set turtle window to full screen (100% of screen width and height)
    t.setup(width=1.0, height=1.0, startx=None, starty=None)

    # Get the actual pixel dimensions of the turtle canvas
    screen_width = t.window_width() 
    screen_height = t.window_height() 
    print(f"Turtle窗口尺寸: {screen_width}x{screen_height}")

    # Calculate and set global scale and offset using the new function
    calculate_scale_and_offset(original_width, original_height, screen_width, screen_height)

else:
    print("错误：无法读取图片，请确保your.png文件存在。")
    exit()

# 2. Binarize
_, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

# 3. Edge detection
edges = cv2.Canny(binary, 50, 150)

# 4. Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Add print info for contour count
print(f"检测到 {len(contours)} 个轮廓。")

# 5. Draw all contours with turtle
draw_contours(contours)

t.done()
