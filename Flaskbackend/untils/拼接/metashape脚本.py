# 载入所需库函数
import Metashape
import os
import argparse


# 创建 ArgumentParser 对象
parser = argparse.ArgumentParser(description="Process some images with Metashape.")
parser.add_argument('--input_path', type=str, required=True, help='Path to the input folder')
parser.add_argument('--output_path', type=str, required=True, help='Path to the output folder')

# 解析命令行参数
args = parser.parse_args()

# 使用解析后的参数
input_path = args.input_path
output_path = args.output_path
# 输入输出文件夹

# 寻找图片函数
def find_files(folder, types):
    return [entry.path for entry in os.scandir(folder) if
            (entry.is_file() and os.path.splitext(entry.name)[1].lower() in types)]


# 创建一个新项目
doc = Metashape.app.document
if not doc:
    doc = Metashape.Document()
doc.read_only = False  # 确保文档不是只读模式

# 检查是否已经存在Chunk，如果不存在则创建一个
if not doc.chunk:
    chunk = doc.addChunk()
else:
    chunk = doc.chunk  # 或者选择当前的chunk

# 导入图片
photos = find_files(input_path, [".jpg", ".jpeg", ".tif", ".tiff"])
chunk.addPhotos(photos)

# 图片对齐
chunk.matchPhotos(generic_preselection=True,
                  reference_preselection=False)
chunk.alignCameras()

# 建立深度图
chunk.buildDepthMaps()
# 生成密集点云
chunk.buildDenseCloud()
# 保存
doc.save(input_path + "/project.psx")

# 构建DEM
chunk = doc.chunk
chunk.buildDem(source_data=Metashape.DataSource.DenseCloudData,
               interpolation=Metashape.Interpolation.EnabledInterpolation)

#doc.save()

# 构建正射影像
chunk.buildOrthomosaic(surface_data=Metashape.DataSource.ElevationData,
                       blending_mode=Metashape.BlendingMode.MosaicBlending)
#doc.save()

# 导出正射影像
chunk.exportRaster(output_path + "/output.tif")

Metashape.app.quit()