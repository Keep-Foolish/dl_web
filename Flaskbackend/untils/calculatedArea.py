import rasterio
import math
from PIL import Image
import numpy as np

# 计算空间分辨率（每像素面积）函数
def calculate_sr(tif_path):
    with rasterio.open(tif_path) as src:
        transform = src.transform
        width = src.width
        height = src.height
        crs = src.crs
        print(f"图像坐标参考系统（CRS）：{crs}")

        # 假设中心纬度为 30°
        latitude = 30.0
        latitude_rad = math.radians(latitude)

        pixel_width = transform[0]
        pixel_height = transform[4]  # 注意是 transform[4] 而不是 transform[1]，因为是负值

        pixel_width_in_meters = abs(pixel_width) * 111320 * math.cos(latitude_rad)
        pixel_height_in_meters = abs(pixel_height) * 111320

        # 每个像素面积（平方米）
        sr = pixel_width_in_meters * pixel_height_in_meters
        print(f"空间分辨率（每像素面积）：{sr:.4f} 平方米")

        return sr

# 统计每种颜色像素数量并计算面积
def calculate_area_from_segmentation(seg_image_path, pixel_area):
    image = Image.open(seg_image_path).convert("RGB")
    data = np.array(image)

    # 定义颜色标签
    red_label = (250, 4, 27)     # 倒伏
    green_label = (4, 250, 27)   # 未倒伏
    black_label = (0, 0, 0)      # 背景

    red_mask = np.all(data == red_label, axis=-1)
    green_mask = np.all(data == green_label, axis=-1)
    black_mask = np.all(data == black_label, axis=-1)

    red_count = np.sum(red_mask)
    green_count = np.sum(green_mask)
    black_count = np.sum(black_mask)

    red_area = red_count * pixel_area
    green_area = green_count * pixel_area
    black_area = black_count * pixel_area

    print(f"倒伏区域（红）面积：{red_area:.2f} 平方米")
    print(f"未倒伏区域（绿）面积：{green_area:.2f} 平方米")
    print(f"背景区域（黑）面积：{black_area:.2f} 平方米")
    print(f"图像总面积：{(red_area + green_area + black_area):.2f} 平方米")

    return red_area, green_area, black_area

# 主程序
if __name__ == "__main__":
    tif_path = r"C:\Users\zhangwei\Desktop\小麦倒伏数据\tif\20210531-field2.tif"
    seg_image_path = r"C:\Users\zhangwei\Desktop\result\20210531-field2-annoted\20210531-field2-annoted.png"  # 你的语义分割图像路径

    try:
        pixel_area = calculate_sr(tif_path)
        calculate_area_from_segmentation(seg_image_path, pixel_area)
    except Exception as e:
        print(f"发生错误：{e}")
