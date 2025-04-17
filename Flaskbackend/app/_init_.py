from flask import Flask
from flask_cors import CORS  # 导入 flask_cors
from config import Config  # 确保从 config.py 里导入 Config 类

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # 这里使用 Config 类

    # 启用 CORS，允许所有域名访问
    CORS(app, resources={r"/upload": {"origins": "*"}})

    # 导入并注册 Blueprint
    from .routes import bp  # 确保 routes.py 在 app 目录下
    app.register_blueprint(bp)

    return app
