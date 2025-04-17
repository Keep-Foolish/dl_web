from flask import request,jsonify
import os

def upload_image():
    # 检查请求是否包含文件
    if 'file' not in request.files:
        return False

    file = request.files['file']

    # 如果没有选择文件
    if file.filename == '':
        return False

    # 检查文件类型是否为PNG
    if file and file.filename.lower().endswith('.png'):
        # 定义文件保存的目录
        save_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'savePng')

        # 这里可以保存文件或者做其他处理
        # file.save('path_to_save_file.png')  # 如果需要保存
        print("接收到png图像")

        # 确保保存目录存在，如果不存在则创建
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        # 获取文件路径并保存文件
        file_path = os.path.join(save_directory, file.filename)
        file.save(file_path)
        return True
    else:
        return False