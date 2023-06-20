import requests
import json
import time

openaikey_env = "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"
print("Bearer "+ openaikey_env)
fileAndContent = {}

MAX_RETRY_COUNT = 3 # 最大重试次数
RETRY_INTERVAL_SECONDS = 60 # 重试间隔时间，单位为秒

retry_count = 0

# 接口请求地址
api_url = "https://service-k31jp0z6-1317488882.usw.apigw.tencentcs.com/v1/chat/completions"

# 这个模板为getOpenAIapi函数
def getOpenAIapi(encontent):
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer "+ openaikey_env
    }
    p = """
You are a seasoned technical writer with a mastery of bilingual document writing and translation in both English and Chinese. Many readers have highly praised your translation work in the manuals you've written. 
I need to translate the following English technical document into Chinese. During the translation process, please note the following points:
    1. Please retain all punctuation marks, and do not change their positions or forms.
    2. When translating content that is in the format of Markdown document titles, please use the annotation translation strategy. For example  {'1':'["## Backward\\n"]'}. , translate them to {'1':'["## 回退（Backward）\\n"]'}.
    3. Content that begins with coding keywords and coding equations do not need to be translated. For example, code starting with 'from', 'const', 'with', as well as variable names, should not be translated.
       For instance, {'1':['$code_chatbot_streaming\n']} should not be translated.
       {'1':'[column_names = ["Reference (y)", "Style Code(w)", "Real Face Image(x)"]\n]'} should not be translated.
    4. If it's like this: {'1':['[Adding example inputs](#example-inputs)\n']}, please translate it to: {'1':['[添加输入示例 （Adding example inputs）](#example-inputs)\n']}.
    5. If it's like this: {'1':["- `Dependents <./dependents.html>`_: List of repositories that use LangChain.\n"]}, please translate it to: {'1':['- Dependents <./dependents.html>`_: 所有使用LangChain的代码仓库.\n']}.
    6. All machine learning, NLP, and Python professional terms do not need to be translated.
    7. [{'5': '    - [Dependents](#Dependents)\n'}] should be translated as: [{'5': '    - [依赖项（Dependents）](#Dependents)\n'}].
    8. When English words or numbers appear in the translated text, they should be typed in half-width characters, and a half-width space should be left on both sides.
The content that needs to be translated is as follows: {""" +  encontent   + """}. The result of your translation must maintain the original string JSON object format."""
    payload = {
     "model": "gpt-3.5-turbo-16k",
     "messages": [{"role": "user", "content": p}],
     "temperature": 0.7
   }
    

    if(encontent != None and encontent != '{}'):
        print('进入请求')
        print(payload)
        try:
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            # print(response)

            response_data = response.json()
            if response.status_code == 200 and 'choices' in response_data:
                messages = response_data['choices'][0]['message']['content']
                return messages
            # elif response.status_code == 429:
            #     print('进入429循环请求'+str(response.status_code ))
            #     for i in range(MAX_RETRY_COUNT):
            #         print('进入429循环请求retry_count'+str(retry_count))
            #         response = requests.post(url, data=json.dumps(payload), headers=headers)
            #         response_data = response.json()
            #         if response.status_code == 429: # 如果返回码为 429，进行等待后重试
            #             time.sleep(RETRY_INTERVAL_SECONDS) 
            #             retry_count += 1
            #             print("加一次" +str(retry_count))
            #         elif response.status_code == 200 and 'choices' in response_data: # 请求成功，获取返回结果并跳出循环
            #             messages = response_data['choices'][0]['message']['content'] # 获取返回结果
            #             return messages
                # raise Exception('尝试三次后，请求失败，请查阅失败的文件有哪些? 在error_file_paths：{}'.format(response.status_code))    
            else:
                print(f"接口请求出错: {str(response.status_code)}")
                return str(response.status_code)
        except requests.exceptions.RequestException as e:
            print(f"接口请求出错: {e}")
            return '999'
            
    # else:
    #     return json.dumps({"result": ""})
    # return response.json()['choices'][0]['message']['content']

