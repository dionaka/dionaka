import cv2
import numpy as np
#直接比较像素值：适用于完全相同的图像。
def compare_pixel(img1_path,img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    if img1 is None or img2 is None:
        print("Error: Image not found.")
        return False
    if img1.shape != img2.shape:
        print("Error: Image sizes are not equal.")
        return False
    difference = img1 == img2
    same_pixel = np.sum(difference)
    total_pixels= img1.size
    accuracy = same_pixel/ total_pixels
    return accuracy
    #return (img1 == img2).all()


#计算哈希值：适用于完全相同的图像，速度快。
def compare_hash(img1_path,img2_path):
    pass
#结构相似性指数（SSIM）：适用于判断图像是否相似但不完全相同的情况。
#感知哈希（pHash）：适用于判断图像是否有轻微变化但仍相似的情况。