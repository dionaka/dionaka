import requests
import os
import tempfile
import sys # 为了处理退出
from openai import OpenAI
import time # 用于生成唯一文件名
import json # 导入 json 库
import playsound # 导入 playsound 库

# 创建保存语音的目录
audio_save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice")
os.makedirs(audio_save_dir, exist_ok=True)
print(f"语音将保存到: {audio_save_dir}")

# 定义配置文件路径
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# 函数：加载配置
def load_config(config_path):
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"加载配置失败或文件格式错误: {e}")
            return None
    return None

# 函数：保存配置
def save_config(config_data, config_path):
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=4)
        print(f"配置已保存到: {config_path}")
    except IOError as e:
        print(f"保存配置失败: {e}")

# 获取或加载用户输入的API信息
config = load_config(config_file_path)

# 存储当前配置的字典，用于在重新输入时提供默认值。
# 即使加载失败或用户选择重新输入，也尝试使用加载的数据作为默认值源。
current_config_values = config.copy() if config else {}

if config:
    print("\n检测到已保存的配置：")
    print(f"  LLM Base URL: {config.get('llm_base_url', '未设置')}")
    print(f"  LLM API Key: {'********' if config.get('llm_api_key') else '未设置'}") # 不显示完整的key
    print(f"  TTS API Choice: {config.get('tts_api_choice', '未设置')}")
    print(f"  TTS API URL: {config.get('tts_api_url', '未设置')}")
    if config.get('tts_api_choice', '').lower() == 'vits_simple_api':
         print(f"  VITS Speaker ID: {config.get('vits_speaker_id', '未设置')}")
    print(f"  System Prompt: {config.get('system_prompt', '未设置')}") # 添加显示系统提示词

    confirm = input("是否使用以上配置？(回车确认，输入其他内容重新配置): ")

    if confirm == '':
        # 使用加载的配置
        llm_base_url = config.get('llm_base_url')
        llm_api_key = config.get('llm_api_key')
        tts_api_choice = config.get('tts_api_choice')
        tts_api_url = config.get('tts_api_url')
        vits_speaker_id = config.get('vits_speaker_id')
        system_prompt = config.get('system_prompt') # 获取系统提示词

        # 检查加载的配置是否完整 (与之前逻辑相同)
        if not all([llm_base_url, llm_api_key, tts_api_choice, tts_api_url]):
             print("加载的配置不完整，请重新输入。")
             # 加载的配置不完整时，仍然使用加载的数据作为默认值源
             # current_config_values 已经保留了加载的数据
             config = None # 标记为需要重新输入
        elif tts_api_choice and tts_api_choice.lower() == 'vits_simple_api' and vits_speaker_id is None:
             print("加载的VITS配置缺少发言人ID，请重新输入。")
             # 加载的配置不完整时，仍然使用加载的数据作为默认值源
             # current_config_values 已经保留了加载的数据
             config = None # 标记为需要重新输入

    else:
        # 用户选择重新输入
        print("请重新输入配置：")
        # current_config_values 已经保留了加载的数据，作为默认值源
        config = None # 标记为需要重新输入

# 如果没有加载成功或者用户选择重新输入
# 此时 current_config_values 应该包含加载的数据 (如果存在)，或者是一个空字典
if not config:
    # 使用 current_config_values 提供默认值
    default_llm_base_url = current_config_values.get('llm_base_url', '')
    default_llm_api_key = current_config_values.get('llm_api_key', '')
    default_tts_api_choice = current_config_values.get('tts_api_choice', '')
    default_tts_api_url = current_config_values.get('tts_api_url', '')
    default_vits_speaker_id = current_config_values.get('vits_speaker_id', '')
    default_system_prompt = current_config_values.get('system_prompt', "你是一个人工智能助手，输出格式为文本文档模式，请不要输出markdown格式") # 添加默认系统提示词

    llm_base_url_input = input(f"请输入LLM API的Base URL (例如 https://api.deepseek.com) [{default_llm_base_url}]: ")
    llm_base_url = llm_base_url_input if llm_base_url_input else default_llm_base_url

    llm_api_key_input = input(f"请输入LLM API Key [{default_llm_api_key}]: ")
    llm_api_key = llm_api_key_input if llm_api_key_input else default_llm_api_key

    tts_api_choice_input = input(f"请选择TTS API (gpt_sovits 或 vits_simple_api) [{default_tts_api_choice}]: ").lower()
    tts_api_choice = tts_api_choice_input if tts_api_choice_input else default_tts_api_choice.lower() # 使用 lower()

    tts_api_url_input = input(f"请输入 {tts_api_choice} API 的地址 [{default_tts_api_url}]: ")
    tts_api_url = tts_api_url_input if tts_api_url_input else default_tts_api_url
    tts_api_url = tts_api_url.rstrip('/') # 移除末尾的斜杠以避免双斜杠问题

    vits_speaker_id = None # 重置VITS ID
    if tts_api_choice == 'vits_simple_api':
        default_vits_speaker_id_str = str(current_config_values.get('vits_speaker_id', '')) # 从 current_config_values 获取并转换为字符串
        vits_speaker_id_input = input(f"请输入VITS Simple API 的发言人ID (例如 0, 1, 2...) [{default_vits_speaker_id_str}]: ")
        vits_speaker_id_str = vits_speaker_id_input if vits_speaker_id_input else default_vits_speaker_id_str
        # 尝试将输入的ID转换为整数，如果失败则保持为 None 或原始字符串（取决于后续需求）
        try:
             vits_speaker_id = int(vits_speaker_id_str) if vits_speaker_id_str else None
        except ValueError:
             print(f"警告: 输入的发言人ID ' {vits_speaker_id_str} ' 不是有效的数字，将不保存此ID。")
             vits_speaker_id = None # 输入无效时也设置为 None

    system_prompt_input = input(f"请输入AI的系统提示词 (人设) [{default_system_prompt}]: ") # 添加系统提示词输入
    system_prompt = system_prompt_input if system_prompt_input else default_system_prompt

    # 将新输入的配置存储在一个临时字典中，用于后续验证和保存
    temp_config_values = {
        'llm_base_url': llm_base_url,
        'llm_api_key': llm_api_key,
        'tts_api_choice': tts_api_choice,
        'tts_api_url': tts_api_url,
        'vits_speaker_id': vits_speaker_id,
        'system_prompt': system_prompt # 添加系统提示词到临时字典
    }

# 初始化LLM客户端 (使用获取到的 llm_base_url 和 llm_api_key)
# 使用加载的或新输入的配置值
used_llm_base_url = temp_config_values.get('llm_base_url') if not config else llm_base_url
used_llm_api_key = temp_config_values.get('llm_api_key') if not config else llm_api_key
used_tts_api_choice = temp_config_values.get('tts_api_choice') if not config else tts_api_choice
used_tts_api_url = temp_config_values.get('tts_api_url') if not config else tts_api_url
used_vits_speaker_id = temp_config_values.get('vits_speaker_id') if not config else vits_speaker_id
used_system_prompt = temp_config_values.get('system_prompt') if not config else system_prompt # 获取使用的系统提示词

try:
    print("正在尝试初始化LLM客户端...")
    client = OpenAI(api_key=used_llm_api_key, base_url=used_llm_base_url)
    # 尝试一个简单的调用来验证key是否有效
    # 注意：这可能会产生微小的费用，但可以有效验证配置
    # 或者可以跳过此验证，直接进入聊天循环，让第一次API调用失败来提示用户
    # 这里选择不进行额外的验证调用，依赖后续聊天中的实际调用来暴露问题
    print("LLM客户端初始化成功。")

    # LLM客户端初始化成功后，如果配置是新输入或修改的，询问是否保存
    # config 为 None 表示是新输入或用户选择了重新输入
    if not config:
        save_confirm = input("LLM客户端初始化成功。是否保存本次配置供下次使用？(回车保存，输入其他内容不保存): ")
        if save_confirm == '':
            # 保存 temp_config_values 中的配置
            save_config(temp_config_values, config_file_path)
        else:
            print("本次配置未保存。")

except Exception as e:
    print(f"LLM客户端初始化失败: {e}")
    print("请检查您的API Base URL 和 API Key 是否正确。")
    sys.exit() # 初始化失败则退出

# 使用获取到的TTS配置 (无论是加载的还是新输入的)
used_tts_api_choice = tts_api_choice if config else temp_config_values.get('tts_api_choice')
used_tts_api_url = tts_api_url if config else temp_config_values.get('tts_api_url')
used_vits_speaker_id = vits_speaker_id if config else temp_config_values.get('vits_speaker_id')

# 检查必要的TTS配置，VITS需要ID
if used_tts_api_choice and used_tts_api_choice.lower() == 'vits_simple_api' and used_vits_speaker_id is None:
    print("错误：VITS Simple API 需要发言人ID，但未提供或加载失败。")
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
                {"role": "system", "content": used_system_prompt}, # 使用配置的系统提示词
                {"role": "user", "content": user_input},
            ],
            stream=False
        )

        llm_text = response.choices[0].message.content
        print(f"AI: {llm_text}")

        # 2. 调用TTS API获取语音数据
        # 这里需要根据您选择的TTS API接口来构建请求
        print("正在调用TTS...")
        if used_tts_api_choice == 'gpt_sovits':
            # GPT-SoVITS可能需要更多参数，例如语音角色等
            # 请根据实际API文档调整，假设合成端点是 /synthesize，使用POST，JSON格式
            tts_payload = {"text": llm_text}
            tts_response = requests.post(f"{used_tts_api_url}/synthesize", json=tts_payload)
        elif used_tts_api_choice == 'vits_simple_api':
            # VITS Simple API 根据用户提供的日志，使用GET方法，端点是 /voice/vits
            # 文本和ID作为查询参数
            # 这里已经通过前面的检查确保 used_vits_speaker_id 不是 None
            tts_url = f"{used_tts_api_url}/voice/vits?text={requests.utils.quote(llm_text)}&id={used_vits_speaker_id}"
            tts_response = requests.get(tts_url)
        else:
            print(f"不支持的TTS API选择: {used_tts_api_choice}")
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
            # Windows下使用 playsound 库实现无窗口播放
            try:
                playsound.playsound(audio_filepath, block=True)
            except playsound.PlaysoundException as e:
                print(f"播放音频失败: {e}")
                # 如果 playsound 失败，可以考虑回退到 Start-Process 或者提示用户
                # 为了简单起见，这里只打印错误
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
