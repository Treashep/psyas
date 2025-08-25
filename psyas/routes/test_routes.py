from Tools.scripts.fixnotice import process
from flask import Blueprint, jsonify, request  # 核心工具
from psyas.extensions import db
from psyas.user.models import User

test_bp = Blueprint('test', __name__, url_prefix='/api/test')

# 测试接口 1：基础连接测试
@test_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({"code": 200,
                    "message":"前后端连接成功！",
                    "data": None
    })

@test_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'code': 400,
                        'message':'请传输JSON数据'}),400
    if 'name' not in data or 'age' not in data:
        return jsonify({'code': 400,
                        'message':'请缺少name或age'}),400
    process_age=int(data['age'])+1
    return jsonify({'code': 200,
                    'message':'数据处理成功',
                    'data':{"原始数据":data,"age":process_age}})
@test_bp.route('/greet', methods=['GET'])
def greet():
    username=request.args.get('name',default='访客',type=str)
    greeting=f"你好{username}！后端已收到你传递的参数"
    return jsonify({'code': 200,
                    'message':'参数接收成功',
                    'data':{"greeting":greeting,
                            'received_username':username}
                    })

