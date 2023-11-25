import cv2
import numpy as np

def find_slider_gap(image_path):
    # 读取图片
    original_image = cv2.imread(image_path)

    # 将图像转换为HSV颜色空间
    hsv_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    # 提取阴影的掩码
    lower_shadow = np.array([0, 0, 0], dtype=np.uint8)
    upper_shadow = np.array([180, 255, 50], dtype=np.uint8)
    shadow_mask = cv2.inRange(hsv_image, lower_shadow, upper_shadow)

    # 使用形态学操作扩大阴影区域
    kernel = np.ones((5, 5), np.uint8)
    shadow_mask = cv2.morphologyEx(shadow_mask, cv2.MORPH_CLOSE, kernel)

    # 找到轮廓
    contours, _ = cv2.findContours(shadow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 找到最大的轮廓
    max_contour = max(contours, key=cv2.contourArea)

    # 在原图上绘制红线轮廓
    cv2.drawContours(original_image, [max_contour], -1, (0, 0, 255), 2)

    # 保存带有红线轮廓的图片
    cv2.imwrite('output_image_with_contour.jpg', original_image)

    # 获取包围盒
    x, y, w, h = cv2.boundingRect(max_contour)

    # 返回缺口的左边边的 X 坐标
    return x

# 替换为你的验证码图片路径
image_path = 'input.png'
gap_x_coordinate = find_slider_gap(image_path)
print("缺口左边边的 X 坐标:", gap_x_coordinate)
