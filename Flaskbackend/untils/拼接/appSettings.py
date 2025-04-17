import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QHBoxLayout, \
    QScrollArea, QFrame, QGridLayout, QGraphicsView, QSizePolicy,QGraphicsScene,QGraphicsPixmapItem
from PySide6.QtGui import QPixmap, QFont, QPainter,QImageReader
from PySide6.QtCore import Qt
from PIL import Image
import subprocess



class ImageViewerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件夹图片浏览")
        self.setGeometry(100, 100, 900, 700)  # 设置窗口大小
        self.setStyleSheet("background-color: #f5f5f5;")  # 设置背景色

        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建顶部按钮布局
        top_button_layout = QHBoxLayout()

        # 创建选择文件夹的按钮
        self.folder_button = QPushButton("选择图片文件夹", self)
        self.folder_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 12px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1e6e99;
            }
        """)
        self.folder_button.clicked.connect(self.choose_folder)

        # 创建输出文件夹选择按钮
        self.output_button = QPushButton("选择输出文件夹", self)
        self.output_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border-radius: 5px;
                padding: 12px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.output_button.clicked.connect(self.choose_output_folder)

        # 创建拼接图片的按钮
        self.stitch_button = QPushButton("拼接图片", self)
        self.stitch_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 12px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.stitch_button.clicked.connect(self.stitch_images)

        # 将按钮添加到顶部按钮布局
        top_button_layout.addWidget(self.folder_button)
        top_button_layout.addWidget(self.output_button)
        top_button_layout.addWidget(self.stitch_button)
        top_button_layout.setSpacing(15)  # 设置按钮间的间距

        # 创建显示文件夹路径的标签
        self.path_label = QLabel("尚未选择文件夹", self)
        self.path_label.setAlignment(Qt.AlignCenter)
        self.path_label.setFont(QFont("Arial", 12))

        # 创建显示输出文件夹路径的标签
        self.output_path_label = QLabel("尚未选择输出文件夹", self)
        self.output_path_label.setAlignment(Qt.AlignCenter)
        self.output_path_label.setFont(QFont("Arial", 12))

        # 创建显示图片缩略图的区域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.image_container = QFrame(self)
        self.scroll_area.setWidget(self.image_container)

        # 图片布局
        self.image_layout = QGridLayout(self.image_container)
        self.image_layout.setSpacing(10)  # 图片之间的间距

        # 添加组件到布局
        main_layout.addLayout(top_button_layout)  # 添加顶部按钮布局
        main_layout.addWidget(self.path_label)
        main_layout.addWidget(self.scroll_area)
        main_layout.addWidget(self.output_path_label)
        main_layout.addSpacing(20)  # 添加额外的间距

        # 创建显示拼接结果的区域（使用 QGraphicsView）
        self.graphics_view = QGraphicsView(self)
        self.graphics_scene = QGraphicsScene(self)
        self.graphics_view.setScene(self.graphics_scene)
        self.graphics_view.setStyleSheet("border: 1px solid #ddd; background-color: #ffffff;")
        self.graphics_view.setAlignment(Qt.AlignCenter)
        self.graphics_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # 设置大小策略为横向和纵向扩展
        main_layout.addWidget(self.graphics_view)

    def choose_folder(self):
        """选择文件夹并显示其中的图片缩略图"""
        folder_path = QFileDialog.getExistingDirectory(self, "选择图片文件夹")
        if folder_path:
            self.path_label.setText(f"选择的文件夹: {folder_path}")
            self.display_images(folder_path)

    def choose_output_folder(self):
        """选择输出文件夹"""
        output_folder = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if output_folder:
            self.output_path_label.setText(f"选择的输出文件夹: {output_folder}")
            self.output_folder = output_folder  # 保存输出文件夹路径

    def display_images(self, folder_path):
        """展示文件夹中的图片缩略图"""
        # 清空之前的缩略图
        for i in reversed(range(self.image_layout.count())):
            widget = self.image_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # 获取文件夹中的所有图片文件
        image_files = [f for f in os.listdir(folder_path) if
                       f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # 设置每行显示的图片数量
        columns = 5
        row = 0
        column = 0

        # 为每个图片创建一个缩略图
        for img_file in image_files:
            img_path = os.path.join(folder_path, img_file)

            # 使用 QPixmap 加载图片
            pixmap = QPixmap(img_path)
            pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # 创建一个标签来显示图片
            img_label = QLabel(self)
            img_label.setPixmap(pixmap)
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setFixedSize(100, 100)
            img_label.setStyleSheet("border: 1px solid #ddd; border-radius: 10px; background-color: #fff;")

            # 将图片标签添加到布局中
            self.image_layout.addWidget(img_label, row, column)

            # 更新行列，确保每行最多显示 5 张图片
            column += 1
            if column >= columns:
                column = 0
                row += 1
    def stitch_images(self):
        """执行图片拼接功能"""
        input_folder = self.path_label.text().replace("选择的文件夹: ", "")
        output_folder = self.output_path_label.text().replace("选择的输出文件夹: ", "")
        if not input_folder or not output_folder:
            print("请选择输入和输出文件夹")
            return

        print(f"开始拼接文件夹 {input_folder} 中的图片并保存到 {output_folder}")

        # Metashape 路径和脚本路径
        metashape_path = r"C:\Program Files\metashape\metashape.exe"  # 替换为你的 Metashape 安装路径
        script_path = r"C:\code\py\test\2.py"  # 替换为你的 Metashape 脚本文件路径

        # 确保路径存在
        os.makedirs(output_folder, exist_ok=True)

        # 调用 Metashape 命令行工具运行脚本
        command = [metashape_path, "-r", script_path, "--input_path", input_folder, "--output_path", output_folder]
        print(f"运行命令: {' '.join(command)}")
        subprocess.run(command)

        print("处理完成！")

        # 加载输出文件夹中的 .tiff 文件并显示
        self.display_stitched_image()

    def display_stitched_image(self):
        """将 TIFF 图像转换为 PNG 格式并显示"""
        QImageReader.setAllocationLimit(512 * 1024 * 1024)  # 512MB

        output_folder = self.output_path_label.text().replace("选择的输出文件夹: ", "")
        if not output_folder:
            return

        try:
            # 假设拼接图像存储在输出文件夹
            stitched_image_path = os.path.join(output_folder, "output.tif")
            # 使用 Pillow 打开 TIFF 文件
            Image.MAX_IMAGE_PIXELS = None
            img = Image.open(stitched_image_path)

            # 将图片转换为 RGB 格式（如果需要）
            img = img.convert("RGB")

            # 将图片保存为 PNG 格式
            png_path = stitched_image_path.rsplit('.', 1)[0] + '.png'
            img.save(png_path, 'PNG')

            # 使用 QPixmap 加载 PNG 图片
            pixmap = QPixmap(png_path)

            # 如果图片过大，缩小显示
            scale_factor = 1
            max_width = self.graphics_view.width()  # 获取 QGraphicsView 当前宽度
            max_height = self.graphics_view.height()  # 获取 QGraphicsView 当前高度

            if pixmap.width() > max_width or pixmap.height() > max_height:
                scale_factor = min(max_width / pixmap.width(), max_height / pixmap.height())
                pixmap = pixmap.scaled(pixmap.width() * scale_factor, pixmap.height() * scale_factor,
                                       Qt.KeepAspectRatio,
                                       Qt.SmoothTransformation)

            # 使用 QGraphicsPixmapItem 显示图片
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.graphics_scene.clear()  # 清空之前的图片
            self.graphics_scene.addItem(pixmap_item)

            # 自动缩放以适应视图
            self.graphics_view.setRenderHint(QPainter.Antialiasing, True)
            self.graphics_view.setRenderHint(QPainter.SmoothPixmapTransform, True)

        except Exception as e:
            print(f"加载和显示图片时发生错误: {e}")


def main():
    app = QApplication(sys.argv)
    window = ImageViewerWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
