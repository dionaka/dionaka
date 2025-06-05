import turtle as t
import math
from time import sleep
import cv2
import numpy as np
from PIL import Image # 导入 Pillow 库

# 添加模式选择
print("请选择绘画模式:")
print("1. 使用 OpenCV 提取轮廓并绘制")
print("2. 直接复制像素颜色 (实验性，效果可能不佳)")
print("请选择模式编号 (1或2): ")
mode = input()

# mul = float(input('输入图片输入倍数: ')) # 移除手动输入mul
turtle_speed = int(input('输入绘画速度 (0-10, 0最快): ')) # 恢复用户输入速度
# turtle_speed = 0 # 移除直接设置为最快速度
t.speed(turtle_speed)

# 添加背景颜色选择
print("请选择背景颜色 (black 或 white): ")
bg_color = input().lower() # 读取用户输入并转换为小写

if bg_color == 'white':
    t.Screen().bgcolor("white")
    print("Turtle 窗口背景已设置为白色。")
elif bg_color == 'black':
    t.Screen().bgcolor("black")
    print("Turtle 窗口背景已设置为黑色。")
else:
    t.Screen().bgcolor("black") # 默认设置为黑色
    print("无效的背景颜色输入，默认为黑色。")

t.mode('standard')
t.color('blue')
# t.setup(1000*mul, 1500*mul, 0, 0) # 移除旧的setup调用
t.pensize(2)
t.colormode(255) # Set color mode to 255 to accept integer RGB values 0-255

# 定义全局变量并初始化
auto_mul = 1.0 
global_offset_x = 0
global_offset_y = 0

def tp(x, y):
    # Use calculated global scale and offset for setpos
    t.penup()
    t.setpos(x*auto_mul + global_offset_x, -(y*auto_mul) + global_offset_y)  
    # Note: tp function no longer includes pendown or penup

def draw_contours(contours, original_color_img):
    # Add print info to check number of contours and points in the first contour - REMOVED
    # print(f"开始绘制 {len(contours)} 个轮廓。") # REMOVED
    # if len(contours) > 0 and len(cnt[0]) > 0: # REMOVED
    #     print(f"第一个轮廓有 {len(cnt[0])} 个点。") # REMOVED

    for cnt in contours:
        if len(cnt) < 2:
            continue
            
        # Get color from the original color image at the first point of the contour
        x0, y0 = cnt[0][0]
        # Ensure coordinates are within image bounds (especially after potential scaling issues, though unlikely with first point) - REMOVED check for simplicity, assume first point is valid
        # OpenCV uses [y, x] indexing, BGR order
        color_bgr = original_color_img[y0, x0]
        color_rgb = (int(color_bgr[2]), int(color_bgr[1]), int(color_bgr[0])) # Convert BGR to RGB tuple
        
        # Set turtle color to the sampled color
        t.fillcolor(color_rgb)
        t.pencolor(color_rgb) # Set stroke color as well

        # Move to the first point (using tp, pen is up at this point)
        x0, y0 = cnt[0][0]
        tp(x0, y0)
        t.pendown() # After moving to the first point, put the pen down
        t.begin_fill() # 开始填充

        # Draw lines sequentially (use setpos for subsequent points, pen is down)
        for pt in cnt[1:]:
            x, y = pt[0]
            # Use the calculated global offset for setpos
            t.setpos(x*auto_mul + global_offset_x, -(y*auto_mul) + global_offset_y)
        t.end_fill() # 结束填充
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

        # print(f"根据屏幕和图片尺寸自动计算的缩放倍数 auto_mul: {auto_mul}") # REMOVED
        # print(f"计算的偏移量 global_offset_x: {global_offset_x}, global_offset_y: {global_offset_y}") # REMOVED
    else:
        # Fallback if screen dimensions are not available
        auto_mul = 0.5 # Default value
        global_offset_x = -original_width * auto_mul / 2 # Simple top-left estimation
        global_offset_y = original_height * auto_mul / 2 # Simple top-left estimation (Y-axis inverted)
        # print("警告：无法获取屏幕尺寸，使用默认缩放倍数 0.5 和简单左上角估算。请确保图片不太大。") # REMOVED


# 1. Read image
img_color = cv2.imread('your.png', 1)  # Read in color (flag 1 or omit flag)

# Automatically set up turtle canvas to full screen and calculate appropriate scale and offset

if img_color is not None:
    # Declare global variables here at the very beginning of the block before they are assigned
    # global auto_mul, global_offset_x, global_offset_y # REMOVED, declared in function

    # print("图片your.png读取成功。") # REMOVED
    original_height, original_width = img_color.shape[:2] # Get dimensions from color image

    # Convert color image to grayscale for contour detection
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # Set turtle window to full screen (100% of screen width and height)
    t.setup(width=1.0, height=1.0, startx=None, starty=None)

    # Get the actual pixel dimensions of the turtle canvas
    screen_width = t.window_width() 
    screen_height = t.window_height() 
    # print(f"Turtle窗口尺寸: {screen_width}x{screen_height}") # REMOVED

    # Calculate and set global scale and offset using the new function
    calculate_scale_and_offset(original_width, original_height, screen_width, screen_height)

    # --- 根据选择的模式执行不同逻辑 ---
    if mode == '1':
        print("选择模式 1: 使用 OpenCV 提取轮廓并绘制")
        # 2. Binarize
        binary = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # 3. Edge detection
        edges = cv2.Canny(binary, 50, 150)

        # 4. Find contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # Add print info for contour count - Retained for general info
        print(f"检测到 {len(contours)} 个轮廓。")

        # 5. Draw all contours with turtle
        draw_contours(contours, img_color) # Pass the original color image to the drawing function
        
    elif mode == '2':
        print("选择模式 2: 尝试复制像素颜色块")

        # 使用 Pillow 读取图片
        try:
            img_pillow = Image.open('your.png')
            img_pillow = img_pillow.convert('RGB') # 确保图片是 RGB 格式
            img_width, img_height = img_pillow.size
            print(f"Pillow 读取图片成功，尺寸: {img_width}x{img_height}")

            # 定义块大小 (可以根据需要调整)
            block_size = 30 # 将块大小从 10 改为 30
            print(f"使用块大小: {block_size}")

            # 计算并设置缩放和偏移，确保绘制区域适配屏幕
            # 注意：这里重用了 calculate_scale_and_offset，它会设置全局 auto_mul, global_offset_x, global_offset_y
            # 在读取图片成功后已经调用过一次，这里可以省略或确保参数正确
            # calculate_scale_and_offset(img_width, img_height, t.window_width(), t.window_height())
            # 上面的行在读取图片后已经执行，不再重复
            print(f"使用的缩放倍数 auto_mul: {auto_mul}")
            print(f"使用的偏移量 global_offset_x: {global_offset_x}, global_offset_y: {global_offset_y}")

            # 遍历图片并绘制块
            t.penup()
            print("开始遍历图片块并绘制...") # 添加打印信息
            block_count = 0 # 添加计数器

            # --- 绘制测试标记 --- #
            # 移动画笔到窗口中心并绘制测试点 (B: 画笔从中心开始)
            t.goto(0, 0) 
            t.dot(20, "red") 
            print("已将画笔移动到屏幕中心并绘制红色测试点。") 
            # -------------------- #

            # 计算图片中心的 Turtle 坐标，作为绘制原点 (A: 图片内容居中)
            # 我们希望图片的中心 (img_width/2, img_height/2) 映射到 Turtle 的 (0,0)
            # 那么图片左上角 (0,0) 应该映射到 (-img_width/2 * auto_mul, img_height/2 * auto_mul)
            # 图片的 (x,y) 映射到 Turtle 的 ((x - img_width/2) * auto_mul, -(y - img_height/2) * auto_mul)

            # 存储块的信息以便按距离排序 (C: 绘制顺序从中心向外)
            blocks_to_draw = []

            for img_y in range(0, img_height, block_size):
                for img_x in range(0, img_width, block_size):
                    # 获取当前块的区域
                    x_end = min(img_x + block_size, img_width)
                    y_end = min(img_y + block_size, img_height)
                    if x_end <= img_x or y_end <= img_y:
                        continue

                    # 计算块的中心在图片像素坐标系中的位置
                    block_center_x_img = img_x + (x_end - img_x) / 2.0
                    block_center_y_img = img_y + (y_end - img_y) / 2.0

                    # 计算块中心到图片中心的距离（用于排序）
                    dist_to_center = math.sqrt((block_center_x_img - img_width/2.0)**2 + (block_center_y_img - img_height/2.0)**2)

                    # 获取块的平均颜色
                    try:
                        block_img = img_pillow.crop((img_x, img_y, x_end, y_end))
                        block_np = np.array(block_img)
                        if block_np.size == 0:
                           avg_color_rgb = (0, 0, 0) # Default to black if block is empty
                        elif len(block_np.shape) == 2:
                             avg_color_np = [np.mean(block_np)]*3
                             avg_color_rgb = (int(avg_color_np[0]), int(avg_color_np[1]), int(avg_color_np[2]))
                        elif block_np.shape[2] == 4:
                             avg_color_np = np.mean(block_np[:, :, :3], axis=(0, 1))
                             avg_color_rgb = (int(avg_color_np[0]), int(avg_color_np[1]), int(avg_color_np[2]))
                        else: # RGB
                             avg_color_np = np.mean(block_np, axis=(0, 1))
                             avg_color_rgb = (int(avg_color_np[0]), int(avg_color_np[1]), int(avg_color_np[2]))
                    except Exception as color_e:
                        print(f"获取块颜色时发生错误: {color_e}")
                        avg_color_rgb = (128, 128, 128) # Default to gray on error

                    # 计算块的左上角在 Turtle 坐标系中的位置 (相对于 Turtle 中心 0,0)
                    turtle_pos_x = (img_x - img_width/2.0) * auto_mul
                    turtle_pos_y = -(img_y - img_height/2.0) * auto_mul

                    # 计算绘制尺寸
                    draw_width = (x_end - img_x) * auto_mul
                    draw_height = (y_end - img_y) * auto_mul

                    # 存储块的信息 (包括距离用于排序)
                    blocks_to_draw.append({
                        'pos_x': turtle_pos_x,
                        'pos_y': turtle_pos_y,
                        'width': draw_width,
                        'height': draw_height,
                        'color': avg_color_rgb,
                        'distance': dist_to_center
                    })
            
            print(f"已收集 {len(blocks_to_draw)} 个块的信息。")

            # 按距离中心点的远近对块进行排序 (C: 绘制顺序)
            blocks_to_draw.sort(key=lambda block: block['distance'])
            print("已按距离中心点排序块信息。")

            # 绘制排序后的块
            print("开始按排序顺序绘制块...")
            for block in blocks_to_draw:
                # 移动到块的左上角位置
                t.penup()
                t.goto(block['pos_x'], block['pos_y'])

                # 设置颜色并绘制填充矩形
                t.fillcolor(block['color'])
                t.pencolor(block['color'])

                t.pendown()
                t.begin_fill()
                
                # 绘制矩形
                t.forward(block['width'])
                t.right(90)
                t.forward(block['height'])
                t.right(90)
                t.forward(block['width'])
                t.right(90)
                t.forward(block['height'])
                t.right(90)

                t.end_fill()
                t.penup()
                block_count += 1 # 重新计数绘制的块

            print(f"总共绘制了 {block_count} 个块 (按中心向外顺序)。")
            print("模式 2 块状填充绘制完成。")

        except FileNotFoundError:
            print("错误：无法读取图片，请确保your.png文件存在。")
        except Exception as e:
            print(f"模式 2 绘制过程中发生错误: {e}")
            import traceback
            traceback.print_exc()

else:
    print("错误：无法读取图片，请确保your.png文件存在。")
    exit()

t.done()
