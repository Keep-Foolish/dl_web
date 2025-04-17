from flask import Blueprint, request,jsonify
from untils import uploadPng

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return 'Hello, World!'

@bp.route('/about')
def about():
    return 'about'

@bp.route('/json', methods=['POST'])
def json_example():
    data = request.get_json()  # 解析 JSON 请求体
    name = data.get('name')
    email = data.get('email')
    return f'Name: {name}, Email: {email}'

# 待检测png上传
@bp.route('/upload', methods=['POST'])
def handle_upload():
    # 判断图片上传是否成功
    uploadStatus = uploadPng.upload_image()

    if uploadStatus == False:
        return jsonify({"message": False}), 400
    else:
        return jsonify({"message": True}), 200