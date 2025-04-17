import numpy as np
from PIL import Image
import geopandas as gpd
from shapely.geometry import Polygon
import rasterio
from rasterio.features import shapes

def generate_shapefile_from_png(png_path, shapefile_path):
    # 打开PNG图像
    image = Image.open(png_path)
    image = image.convert("RGB")
    image_array = np.array(image)

    # 创建一个空的掩膜，初始化为背景（255表示背景，0表示其他区域）
    mask = np.ones(image_array.shape[:2], dtype=np.uint8) * 255

    # 红色代表小麦倒伏：R > 150, G < 100, B < 100
    red_areas = (image_array[:,:,0] > 150) & (image_array[:,:,1] < 100) & (image_array[:,:,2] < 100)
    mask[red_areas] = 1  # 小麦倒伏区域标记为1

    # 绿色代表正常小麦：G > 150, R < 100, B < 100
    green_areas = (image_array[:,:,1] > 150) & (image_array[:,:,0] < 100) & (image_array[:,:,2] < 100)
    mask[green_areas] = 2  # 正常小麦区域标记为2

    # 使用rasterio读取mask数据并转换为Shapefile
    mask_data = []
    with rasterio.open(png_path) as src:
        for shape, value in shapes(src.read(1), mask=mask != 255, transform=src.transform):
            if value == 1:  # 小麦倒伏区域
                mask_data.append({'geometry': Polygon(shape['coordinates'][0]), 'value': '倒伏'})
            elif value == 2:  # 正常小麦区域
                mask_data.append({'geometry': Polygon(shape['coordinates'][0]), 'value': '正常'})

    # 创建GeoDataFrame并保存为Shapefile
    gdf = gpd.GeoDataFrame(mask_data)
    gdf.set_crs('EPSG:4326', inplace=True)  # 根据需要设置合适的坐标系
    gdf.to_file(shapefile_path)

    return shapefile_path

# 测试
png_path = r"C:\Users\zhangwei\Desktop\2.jpg"  # 替换为实际的PNG文件路径
shapefile_path = "output_mask.shp"  # 输出的Shapefile路径
shapefile = generate_shapefile_from_png(png_path, shapefile_path)
print(f"生成的Shapefile文件保存路径为: {shapefile}")
