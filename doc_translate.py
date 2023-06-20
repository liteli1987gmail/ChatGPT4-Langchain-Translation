import zipfile
import os
import json
import shutil
from lxml import etree
from collections import OrderedDict
from getreqopenai import getOpenAIapi
from lxml.etree import SubElement
from utils import split_data,safe_json_loads


def translate_word_xml(xml_file_path):
    # 解析XML文件
    tree = etree.parse(xml_file_path)
    root = tree.getroot()

    # 提取所有<w:t>标签的内容，并记录它们在XML中的位置
    translate_predata = {}
    OrderedDict_elements = OrderedDict()
    for i, element in enumerate(root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')):
        # 记录元素的位置和内容
        OrderedDict_elements[i] = element.text
        translate_predata[i] = [element.text]
        # # 创建一个新的<w:t>元素
        parent = element.getparent()
        new_element = etree.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
        # # 设置新元素的文本为翻译后的文本
        new_element.text = OrderedDict_elements[i]
        # Insert the new element right after the current one
        index = parent.index(element)
        parent.insert(index+1, new_element)

    print(f"{OrderedDict_elements}")

    # data_dict = dict(OrderedDict_elements)

    # 把字典转化为JSON对象
    # data_dict_json = json.dumps(data_dict, ensure_ascii=False)
    
    split_json = split_data(translate_predata, 8000)  # 这是数组
    print(f"====split_data====")
    print(f"{split_json}")

    for slicedata in split_json:
        print(f"====slicedata====")
        print(f"{slicedata}")
        data_dict_json = json.dumps(slicedata, ensure_ascii=False)

        translated_res = getOpenAIapi(data_dict_json)
        print(f"====translated_res====")
        print(f"{translated_res}")

        if len(translated_res) > 4:
            translated_dict = safe_json_loads(translated_res)
            print(f"{translated_dict}")

            if translated_dict != {}:

                for key, value in translated_dict.items():
                    OrderedDict_elements[int(key)] = "".join(value)


    # 将翻译后的文本插入回XML
    for i, element in enumerate(root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')):
        if i in OrderedDict_elements:
            element.text = OrderedDict_elements[i]

    # 保存修改后的XML文件
    tree.write(xml_file_path, encoding='utf-8')

def translate_word_doc(input_file_path, output_file_path):
    # 创建一个临时文件夹来存放解压缩的Word文档
    temp_folder_path = 'temp'
    if not os.path.exists(temp_folder_path):
        os.makedirs(temp_folder_path)

    # 解压缩Word文档到临时文件夹
    with zipfile.ZipFile(input_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_folder_path)

    # 翻译XML文件
    translate_word_xml(os.path.join(temp_folder_path, 'word/document.xml'))

    # 将临时文件夹重新压缩为一个Word文档
    shutil.make_archive(output_file_path, 'zip', temp_folder_path)
    # 如果输出文件已经存在，就先删除它
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
    shutil.move(output_file_path+'.zip', output_file_path)

    # 删除临时文件夹
    shutil.rmtree(temp_folder_path)



# 指定输入文件路径和输出文件路径
input_file_path = './en_docs/input.docx'
output_file_path = './cn_docs/output.docx'

# 翻译Word文档
translate_word_doc(input_file_path, output_file_path)
