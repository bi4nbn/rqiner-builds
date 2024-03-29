import requests

def translate_json(content, translated_content):
    translated_data = {}
    for key, value in content.items():
        if isinstance(value, list):
            translated_data[translated_content.get(key, key)] = [translate_json(item, translated_content) for item in value]
        elif isinstance(value, dict):
            translated_data[translated_content.get(key, key)] = translate_json(value, translated_content)
        else:
            translated_data[translated_content.get(key, key)] = value
    return translated_data

def print_info(info):
    print(f"\n纪元: {info['纪元']}")
    print(f"全体战斗力: {info['全体战斗力']: .0f}")  # 更改为‘全体战斗力’
    print(f"战士数量: {info['战士数量']}")
    print(f"战绩: {info['战绩']}")

    for item in info['战士列表']:
        print(f"\n战士信息: 战士姓名: {item['战士姓名']}, 战斗力: {item['战斗力']: .0f}, 战绩: {item['战绩']}")

def get_wallet_info(wallet_id):
    # 构建URL
    url = f"https://pooltemp.qubic.solutions/info?miner={wallet_id}&list=true"

    # 发送GET请求获取数据并添加异常处理
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误: {http_err}")
        return
    except Exception as err:
        print(f"出现错误: {err}")
        return
        
    content = response.json()
    # 定义字段名称翻译
    translated_content = {
        "epoch": "纪元",
        "iterrate": "全体战斗力",  # 更改为‘全体战斗力’
        "devices": "战士数量",
        "solutions": "战绩",
        "device_list": "战士列表",
        "label": "战士姓名",
        "last_iterrate": "战斗力"
    }

    # 提取并翻译数据
    translated_data = translate_json(content, translated_content)

    # 打印所有数据
    print_info(translated_data)

# 测试函数
wallet_id = "KFYHWZGKJDMBGHXLKWLQFPAGXLVCFRMTRDOWZRZBRDMHVBSTRZRIMVWARYSM"
get_wallet_info(wallet_id)