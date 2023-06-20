
import json


import re

def safe_json_loads(s):
    pattern = r'"(\d+)": \s*(\[[^\]]*\]|"[^"]*"|\'[^\']*\')?'
    matches = re.findall(pattern, s)

    result = {}
    for key, value in matches:
        if not value:  # 如果值为空，跳过这个键值对
            continue
        # 移除开始和结束的引号或方括号，然后去除首尾的空白
        # value = value.strip('[]\'" ').split(",")
        # 添加引号并用方括号包围，确保格式正确
        # value = [v.strip('\'" ') for v in value]
        result[key] = json.loads(value)
    return result


def read_ipynb_file(file_path):
    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 保存 markdown cell 的信息
    markdown_cells = {}
    
    # 遍历所有单元格
    for cell in data['cells']:
        if cell['cell_type'] == 'markdown':
            # 保存 markdown 单元格
            markdown_cells[cell['id']] = cell['source']
    
    return markdown_cells

def split_data(data: dict, max_length: int) -> list:
    divided_data = []
    temp = {}

    # 对字典进行遍历，一个一个的将键值对添加到临时字典中
    for key, value in data.items():
        print(key, value)
        print(len(json.dumps(temp)) + len(json.dumps({key: value})))
        if len(json.dumps({key: value})) > max_length:
            # 如果键值对单独组成字典已经超过 max_length，就算这个字典为空也不能添加这个字典，否则这个字典会一直空等到永远
            raise ValueError(f"键值对 {key}:{value} 超过了最大长度限制")

        # 如果临时字典加上新的键值对即没超过 max_length 的长度限制，那就将新键值对加到临时字典里
        if len(json.dumps(temp)) + len(json.dumps({key: value})) <= max_length:
            temp.update({key: value})
        else:
            # 否则，把当前的临时字典中的所有键值对构成一个子字典加入到列表中，并清空临时字典，将新键值对加入到已清空的字典中
            divided_data.append(temp)
            temp = {key: value}
    
    if temp:
        # 如果仍然有没处理的剩余键值对，那么将它们添加为最后一个字典项
        divided_data.append(temp)
    
    return divided_data

def read_rst_file(path):
    """
    读取rst格式文件的每一行，将标题或段落作为key，其内容作为value，以json格式返回
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    result = {}
    for i, line in enumerate(lines,start=1):
        result[str(i)] = line
    return result



def extract_rst_file(path):
    """
    读取rst格式文件的每一行，将标题或段落作为key，其内容作为value，以json格式返回
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    result = {}

    for i, line in enumerate(lines,start=1):
        if line.startswith('|') and ('>`_' not in line) or (',' in line and '.' in line):    
        # if (line.startswith("|")  and not ((">`_.") in line)) or ((",") in line and ("." in line)):
            result[str(i)] = [line]
    return result


# def extract_md_file(filepath):
#     lines = {}
#     with open(filepath, 'r', encoding='utf-8') as f:
#         content = f.readlines()
#     for i, line in enumerate(content, start=1):
#         if (not line.strip().startswith('```python')) and \
#            (not line.strip().startswith('```')) and \
#            ('```' not in line):
#             lines[str(i)] = [line]
#     return lines

def extract_md_file(json_obj):
    non_code_obj = {}
    code_block_stack = []  # 用堆栈跟踪代码块的嵌套
    code_block_lines = []  # 存储所有代码块行的行号
    for key, value in json_obj.items():
        if '```' in value:
            code_block_marker = value[value.index('```'):value.index('```')+3]  # 提取 '```' 及其前面的空格
            if code_block_stack and code_block_stack[-1] == code_block_marker:
                code_block_stack.pop()  # 如果堆栈顶部的元素与当前元素匹配，那么我们正在结束一个代码块
                code_block_lines.append(key)  # 添加代码块结束行
            else:
                code_block_stack.append(code_block_marker)  # 否则，我们正在开始一个新的代码块
                code_block_lines.append(key)  # 添加代码块开始行
        if not code_block_stack and key not in code_block_lines and value.strip():  # 如果堆栈为空并且这一行不在代码块中，那么我们将这一行添加到非代码块对象中
            non_code_obj[key] = [value]
    return non_code_obj



    

def read_md_file(file_path):
    """
    读取md格式文件的每一行，将标题或段落作为key，其内容作为value，以json格式返回
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    result = {}
    for i, line in enumerate(lines,start=1):
        
        result[str(i)] = line

    return result
