import requests
import os
import tempfile
import sys # 为了处理退出
from openai import OpenAI
import time # 用于生成唯一文件名

# 创建保存语音的目录
audio_save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice")
os.makedirs(audio_save_dir, exist_ok=True)
print(f"语音将保存到: {audio_save_dir}")

# 获取用户输入的API信息
llm_base_url = input("请输入LLM API的Base URL (例如 https://api.deepseek.com): ")
llm_api_key = input("请输入LLM API Key: ")

tts_api_choice = input("请选择TTS API (gpt_sovits 或 vits_simple_api): ").lower()
tts_api_url = input(f"请输入 {tts_api_choice} API 的地址: ")
tts_api_url = tts_api_url.rstrip('/') # 移除末尾的斜杠以避免双斜杠问题

# 如果选择VITS Simple API，获取发言人ID
vits_speaker_id = None
if tts_api_choice == 'vits_simple_api':
    vits_speaker_id = input("请输入VITS Simple API 的发言人ID (例如 0, 1, 2...): ")

# 初始化LLM客户端
try:
    client = OpenAI(api_key=llm_api_key, base_url=llm_base_url)
    print("LLM客户端初始化成功。")
except Exception as e:
    print(f"LLM客户端初始化失败: {e}")
    sys.exit()

print("开始聊天。输入 '退出' 结束对话。")

while True:
    user_input = input("你: ")

    if user_input.lower() == '退出':
        print("聊天结束。")
        break

    try:
        # 1. 调用LLM API获取回复
        print("正在调用LLM...")
        # 使用openai库进行调用，根据用户提供的片段修改
        response = client.chat.completions.create(
            model='deepseek-reasoner', # 假设使用 deepseek-reasoner 模型，您可以根据需要更改
            messages=[
                {"role": "system", "content": "你是一个人工智能助手，输出格式为文本文档模式，请不要输出markdown格式"},
                {"role": "user", "content": user_input},
            ],
            stream=False
        )

        llm_text = response.choices[0].message.content
        print(f"AI: {llm_text}")

        # 2. 调用TTS API获取语音数据
        # 这里需要根据您选择的TTS API接口来构建请求
        print("正在调用TTS...")
        if tts_api_choice == 'gpt_sovits':
            # GPT-SoVITS可能需要更多参数，例如语音角色等
            # 请根据实际API文档调整，假设合成端点是 /synthesize，使用POST，JSON格式
            tts_payload = {"text": llm_text}
            tts_response = requests.post(f"{tts_api_url}/synthesize", json=tts_payload)
        elif tts_api_choice == 'vits_simple_api':
            # VITS Simple API 根据用户提供的日志，使用GET方法，端点是 /voice/vits
            # 文本和ID作为查询参数
            if vits_speaker_id is None:
                 print("错误：未提供VITS Simple API 发言人ID。")
                 continue
            tts_url = f"{tts_api_url}/voice/vits?text={requests.utils.quote(llm_text)}&id={vits_speaker_id}"
            tts_response = requests.get(tts_url)
        else:
            print(f"不支持的TTS API选择: {tts_api_choice}")
            continue # 跳过本次循环

        tts_response.raise_for_status()

        # 3. 保存语音数据到指定文件并播放
        # 假设TTS API返回的是wav格式的音频数据
        # 使用时间戳生成文件名
        timestamp = int(time.time())
        audio_filename = f"tts_{timestamp}.wav"
        audio_filepath = os.path.join(audio_save_dir, audio_filename)

        with open(audio_filepath, 'wb') as audio_file:
            audio_file.write(tts_response.content)

        print(f"正在播放语音: {audio_filepath}")
        # 根据操作系统选择播放命令
        if sys.platform == "win32":
            # Windows下使用powershell Start-Process
            # 注意：Start-Process 是非阻塞的
            os.system(f'powershell Start-Process "{audio_filepath}"')
        elif sys.platform == "darwin":
            # macOS下使用afplay
            os.system(f"afplay {audio_filepath}")
        else:
            # Linux下使用aplay或者paplay
            os.system(f"aplay {audio_filepath}")

        # 播放完成后删除临时文件 (对于非阻塞播放，可能需要更复杂的清理机制)
        # 暂时不自动删除，以免播放失败，用户可以手动清理

    except requests.exceptions.RequestException as e:
        print(f"API请求错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

# 退出前可以添加清理临时文件的逻辑，如果之前没有删除
