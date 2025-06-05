import turtle as t
import math
from time import sleep
import cv2
import numpy as np
from PIL import Image # 导入 Pillow 库

# 添加模式选择
print("请选择绘画模式:")
print("1. 使用 OpenCV 提取轮廓并绘制")
print("2. 直接复制像素颜色 (从中心向外)")
print("3. 直接复制像素颜色 (斐波那契螺旋)")
print("请选择模式编号 (1, 2或3): ")
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

    elif mode == '3':
        print("选择模式 3: 直接复制像素颜色 (斐波那契螺旋)")

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

            # Create a dictionary for quick lookup by block image coordinates
            block_dict = {}
            # Also map image indices back to Turtle coordinates for drawing
            img_to_turtle_map = {}
            for block in blocks_to_draw:
                 # Calculate block's top-left image coordinates
                 # Convert Turtle pos (relative to center) back to image top-left (relative to image top-left)
                 img_x_tl = block['pos_x'] / auto_mul + img_width / 2.0
                 img_y_tl = -block['pos_y'] / auto_mul + img_height / 2.0
                 # Use integer indices for the dictionary key
                 block_ix = int(round(img_x_tl / block_size)) # Use round for better mapping to grid indices
                 block_iy = int(round(img_y_tl / block_size))
                 
                 block_dict[(block_ix, block_iy)] = block
                 # Store the block indices mapped to Turtle coordinates for drawing
                 img_to_turtle_map[(block_ix, block_iy)] = (block['pos_x'], block['pos_y'], block['color'])

            print(f"已创建 {len(block_dict)} 个块的查找字典和映射。")

            # Keep track of drawn blocks by their image indices
            drawn_blocks = set()

            # Determine the starting block (center of the image)
            start_ix = int(round(img_width / 2.0 / block_size))
            start_iy = int(round(img_height / 2.0 / block_size))

            # Use a list to maintain the sequence of blocks to visit
            # Start with the center block if it exists
            blocks_to_visit_queue = []
            if (start_ix, start_iy) in block_dict:
                 blocks_to_visit_queue.append((start_ix, start_iy))
                 drawn_blocks.add((start_ix, start_iy))
                 print(f"起始块索引: ({start_ix}, {start_iy})")
            else:
                 print("警告: 图片中心块不存在，尝试寻找最接近的块作为起点。")
                 # Fallback: find the closest existing block to the center
                 min_dist = float('inf')
                 closest_block_key = None
                 for key in block_dict.keys():
                      dist = math.sqrt((key[0] - start_ix)**2 + (key[1] - start_iy)**2)
                      if dist < min_dist:
                           min_dist = dist
                           closest_block_key = key
                 if closest_block_key:
                      blocks_to_visit_queue.append(closest_block_key)
                      drawn_blocks.add(closest_block_key)
                      start_ix, start_iy = closest_block_key
                      print(f"找到并使用最接近中心的块作为起点: ({start_ix}, {start_iy})")
                 else:
                      print("错误: 未找到任何块可供绘制。")
                      # Skip drawing logic if no blocks found
                      max_steps = 0 # Set steps to 0 to skip the loop

            # Define possible moves (8 directions: N, NE, E, SE, S, SW, W, NW)
            moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

            # Parameters for approximating spiral direction
            # Need to map grid coordinates back to a conceptual 'angle'
            # For a spiral, the angle depends on the distance from the center
            # Let's use the angle of the vector from the start point to the current point
            
            print("开始按斐波那契螺旋近似路径绘制块...")
            block_count = 0

            # Turtle starts at center (0,0) already from test dot
            # We will move the turtle directly to the block position before drawing

            while blocks_to_visit_queue:
                # Take the next block from the queue (simple FIFO for now, could be refined)
                # Using a list as a queue (pop(0) is O(n), better to use deque for performance with large images)
                # For simplicity with current tools, stick to list for now.
                current_ix, current_iy = blocks_to_visit_queue.pop(0)

                # Get block info and draw
                if (current_ix, current_iy) in img_to_turtle_map:
                    turtle_pos_x, turtle_pos_y, block_color = img_to_turtle_map[(current_ix, current_iy)]
                    block = block_dict[(current_ix, current_iy)] # Need block_dict to get width and height

                    t.penup()
                    t.goto(turtle_pos_x, turtle_pos_y)

                    t.fillcolor(block_color)
                    t.pencolor(block_color)

                    t.pendown()
                    t.begin_fill()
                    
                    # Draw rectangle
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

                    block_count += 1

                    # Find potential next blocks (neighbors)
                    next_blocks_candidates = []
                    for move_dx, move_dy in moves:
                        neighbor_ix = current_ix + move_dx
                        neighbor_iy = current_iy + move_dy

                        # Check if neighbor is within bounds and exists in our block dictionary
                        # Need to determine image bounds in terms of block indices
                        # Max indices would be ceil(img_width/block_size) - 1 and ceil(img_height/block_size) - 1
                        max_ix = int(math.ceil(img_width / block_size)) - 1
                        max_iy = int(math.ceil(img_height / block_size)) - 1

                        if 0 <= neighbor_ix <= max_ix and 0 <= neighbor_iy <= max_iy and \
                           (neighbor_ix, neighbor_iy) in block_dict and \
                           (neighbor_ix, neighbor_iy) not in drawn_blocks:
                           
                           next_blocks_candidates.append((neighbor_ix, neighbor_iy))

                    # --- Selection Logic for the next block ---
                    # Choose the neighbor that best follows the spiral path.
                    # This is a simplification; a true spiral follows a specific angle pattern.
                    # For a simple approximation, we can try to favor moving 'outward'
                    # or based on a theoretical spiral angle at the current block's position.

                    # Calculate the angle from the start point to the current neighbor candidate
                    # in a grid coordinate system. This is a simplification of the spiral angle.
                    def calculate_grid_angle(p1_ix, p1_iy, p2_ix, p2_iy):
                        dx = p2_ix - p1_ix
                        dy = p2_iy - p1_iy # Grid Y increases downwards
                        # Invert dy for angle calculation if you want angle based on Turtle/math coords (Y up)
                        # angle = math.atan2(-dy, dx) # Use -dy if mapping to math coords
                        
                        # Let's calculate angle based on grid coordinates (Y down) relative to the image center block
                        center_block_ix = int(round(img_width / 2.0 / block_size))
                        center_block_iy = int(round(img_height / 2.0 / block_size))
                        
                        vec_x = p2_ix - center_block_ix
                        vec_y = p2_iy - center_block_iy # Grid Y increases downwards
                        # Angle in grid system, may not directly match math.atan2 conventions easily
                        # A simpler approach might be to calculate the ideal spiral angle at the current grid position
                        # based on the distance from the center.

                        # Let's use a simplified heuristic: prioritize neighbors further from the center
                        # and maybe try to follow a general counter-clockwise outward movement.
                        return (p2_ix - center_block_ix)**2 + (p2_iy - center_block_iy)**2 # Distance squared heuristic

                    # Sort candidates based on distance from the center (simple outward movement)
                    # This doesn't guarantee spiral shape, just outward expansion.
                    # To approximate spiral, we need angle.
                    # Let's calculate the angle of the vector from the current block to the candidate neighbor
                    # and compare it to the expected spiral angle at the current block's position.

                    # Calculate the position of the current block's center in image coordinates
                    current_img_x_center = (current_ix + 0.5) * block_size
                    current_img_y_center = (current_iy + 0.5) * block_size

                    # Calculate the ideal spiral angle (theta) at the current image center position
                    # Based on r = a * sqrt(theta), theta = (r/a)^2
                    # r is the distance from the image center in image pixels
                    dist_from_img_center = math.sqrt((current_img_x_center - img_width/2.0)**2 + (current_img_y_center - img_height/2.0)**2)
                    
                    # Avoid division by zero if exactly at the center
                    if dist_from_img_center > 1e-6:
                        # Approximating theta - this is tricky as theta defines r, and r defines theta
                        # A simple way might be to track the 'unwrapped' angle as we move.
                        # Let's simplify and use the angle from the image center to the current block center.
                        angle_to_current_block = math.atan2(-(current_img_y_center - img_height/2.0), current_img_x_center - img_width/2.0) # Use -dy for standard math angle

                        # The spiral direction should be roughly perpendicular to the vector from the center,
                        # plus a small outward component.
                        # For a counter-clockwise spiral, this is roughly angle_to_current_block + PI/2
                        # Need to normalize angle to [0, 2*PI) or similar
                        ideal_spiral_angle = angle_to_current_block + math.pi / 2.0
                        # Normalize angle
                        ideal_spiral_angle = ideal_spiral_angle % (2 * math.pi)
                        if ideal_spiral_angle < 0:
                            ideal_spiral_angle += 2 * math.pi

                    else: # At the center, any outward direction is valid initially
                         ideal_spiral_angle = 0 # Start moving right (angle 0) or adjust based on desired start direction

                    def angle_difference(angle1, angle2):
                         diff = abs(angle1 - angle2)
                         return min(diff, 2 * math.pi - diff)

                    # Sort candidates based on how well their direction vector from the current block aligns with the ideal spiral angle
                    def calculate_alignment_score(current_ix, current_iy, candidate_ix, candidate_iy, ideal_angle):
                         # Vector from current block center to candidate block center
                         vec_dx = (candidate_ix - current_ix) # * block_size # In block indices
                         vec_dy = (candidate_iy - current_iy) # * block_size # In block indices (Y is down)
                         
                         # Calculate the angle of this vector. Use -dy because math.atan2 assumes Y is up.
                         candidate_angle = math.atan2(-vec_dy, vec_dx)
                         # Normalize angle
                         candidate_angle = candidate_angle % (2 * math.pi)
                         if candidate_angle < 0:
                             candidate_angle += 2 * math.pi

                         # Score is inverse of angle difference (smaller difference is better)
                         return -angle_difference(ideal_angle, candidate_angle)

                    # Sort candidates. A more sophisticated sort might consider distance from center as a secondary factor.
                    next_blocks_candidates.sort(key=lambda candidate: calculate_alignment_score(current_ix, current_iy, candidate[0], candidate[1], ideal_spiral_angle), reverse=True)

                    # Add sorted, unvisited neighbors to the front of the queue to prioritize exploring along the spiral
                    # This makes it more of a priority queue/greedy approach than strict FIFO
                    for next_block_key in next_blocks_candidates:
                         if next_block_key not in drawn_blocks:
                            blocks_to_visit_queue.insert(0, next_block_key) # Add to the front
                            drawn_blocks.add(next_block_key)


            print(f"总共绘制了 {block_count} 个块 (按近似斐波那契螺旋路径)。")
            print("模式 3 近似斐波那契螺旋填充绘制完成。")

        except FileNotFoundError:
            print("错误：无法读取图片，请确保your.png文件存在。")
        except Exception as e:
            print(f"模式 3 绘制过程中发生错误: {e}")
            import traceback
            traceback.print_exc()

else:
    print("错误：无法读取图片，请确保your.png文件存在。")
    exit()

t.done()
