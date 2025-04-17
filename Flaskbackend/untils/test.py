import numpy as np
import rasterio
from PIL import Image
import warnings

# 关闭 PIL 图片解压警告
warnings.simplefilter('ignore', Image.DecompressionBombWarning)


# 计算分批处理的面积
def calculate_area_batch(red_area_mask, batch_size=1000):
    height, width = red_area_mask.shape
    total_red_area = 0

    # 分批处理：按列和行分批
    for row_start in range(0, height, batch_size):
        for col_start in range(0, width, batch_size):
            row_end = min(row_start + batch_size, height)
            col_end = min(col_start + batch_size, width)
            batch = red_area_mask[row_start:row_end, col_start:col_end]
            batch_red_area = np.sum(batch)
            total_red_area += batch_red_area

    return total_red_area


def calculate_area_with_geolocation(tif_image_path, png_image_path):
    # 加载 TIFF 图像，获取地理参考信息
    with rasterio.open(tif_image_path) as src:
        tif_data = src.read(1)  # 读取第一个波段（假设是单波段图像）

        # 获取每个像素的经纬度大小（空间分辨率）
        pixel_width, pixel_height = src.res[0], src.res[1]

        # 获取图像的地理范围（经纬度）
        bounds = src.bounds
        print(f"图像的地理范围: {bounds}")

        # 计算每个像素的实际面积（单位：平方米）
        pixel_area = abs(pixel_width * pixel_height)  # 每个像素的面积

    # 加载 PNG 图像并转换为 NumPy 数组
    png_image = Image.open(png_image_path)
    png_data = np.array(png_image)

    # 假设红色区域标记为 R 通道值大于 200，绿色区域标记为 G 通道值大于 200
    red_area_mask = (png_data[:, :, 0] > 200) & (png_data[:, :, 1] < 100) & (png_data[:, :, 2] < 100)
    green_area_mask = (png_data[:, :, 0] < 100) & (png_data[:, :, 1] > 200) & (png_data[:, :, 2] < 100)

    # 计算红色区域和绿色区域的面积（乘以每个像素的实际面积）
    red_area = calculate_area_batch(red_area_mask) * pixel_area
    green_area = calculate_area_batch(green_area_mask) * pixel_area

    return red_area, green_area


# 主函数
if __name__ == "__main__":
    tif_image_path = r"C:\Users\zhangwei\Desktop\小麦倒伏数据\tif\0521厂房旁-4D.tif"
    png_image_path = r"C:\Users\zhangwei\Desktop\小麦倒伏数据\标注png\0521厂房旁-annoted标注.png"

    try:
        red_area, green_area = calculate_area_with_geolocation(tif_image_path, png_image_path)
        print(f"红色区域面积: {red_area} 平方米")
        print(f"绿色区域面积: {green_area} 平方米")
    except Exception as e:
        print(f"计算出现错误: {e}")