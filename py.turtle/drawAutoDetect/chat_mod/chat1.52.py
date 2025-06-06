import sys
import requests
import os
import tempfile
# import sys # Already imported
from openai import OpenAI
import time
import json
import winsound # For Windows audio playback
import random # Import random module

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QLineEdit, QPushButton
)
from PyQt6.QtCore import QThread, pyqtSignal, QTimer # Import QTimer for animation updates
# from PyQt6.QtGui import QOpenGLFunctions # Reverting import - Removed this line
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
# from PyQt6.OpenGL import QOpenGLFunctions # Corrected import - commented out
from PyQt6.QtGui import QSurfaceFormat # Import QSurfaceFormat for OpenGL context

# Import OpenGL functions directly
from OpenGL.GL import glEnable, glBlendFunc, GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glViewport, glMatrixMode, glLoadIdentity, glOrtho, GL_PROJECTION, GL_MODELVIEW, glEnableClientState, glDisableClientState, GL_VERTEX_ARRAY, GL_TEXTURE_COORD_ARRAY, glTranslate, glScale

# Import live2d-py modules
# from live2d import Live2DModel # Incorrect import
# from live2d.v3 import Live2DModel # Corrected import for Cubism 3.0+ models - still incorrect
# from live2d.v3.model import Live2DModel # Attempting import from live2d.v3.model - still incorrect
# from live2d.Live2D import Live2DModel # Attempting import from live2d.Live2D - still incorrect
import live2d.v3 # Import the v3 module directly
# from live2d.v3 import LAppModel # LAppModel is accessed via live2d.v3.LAppModel now
# from live2d.framework.lapparade import LAppPal # Attempting import for LAppPal - Incorrect
# from live2d.v3 import LAppPal # Corrected import for LAppPal based on .pyi - Still incorrect
# LAppPal functions are likely directly in live2d.v3

# Import MotionPriority from live2d.v3
from live2d.v3 import MotionPriority

# Define configuration and audio save paths
audio_save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "voice")
os.makedirs(audio_save_dir, exist_ok=True)
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# Function: Load config
def load_config(config_path):
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"加载配置失败或文件格式错误: {e}")
            return None
    return None

# Function: Save config (Optional in GUI, maybe a settings dialog later)
# def save_config(config_data, config_path):
#     try:
#         with open(config_path, 'w', encoding='utf-8') as f:
#             json.dump(config_data, f, ensure_ascii=False, indent=4)
#         print(f"配置已保存到: {config_path}")
#     except IOError as e:
#         print(f"保存配置失败: {e}")


# Worker thread for API calls to keep GUI responsive
class WorkerThread(QThread):
    # Signals to communicate with the main thread
    llm_response_signal = pyqtSignal(str)
    tts_audio_signal = pyqtSignal(str) # Emits filepath of saved audio
    error_signal = pyqtSignal(str)

    def __init__(self, client, user_input, tts_config, system_prompt):
        super().__init__()
        self.client = client
        self.user_input = user_input
        self.tts_config = tts_config
        self.system_prompt = system_prompt

    def run(self):
        try:
            # 1. Call LLM API
            # print("正在调用LLM...") # Avoid printing in thread directly, use signal
            response = self.client.chat.completions.create(
                model='deepseek-reasoner', # Assuming deepseek-reasoner, adjust if needed
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": self.user_input},
                ],
                stream=False
            )

            llm_text = response.choices[0].message.content
            self.llm_response_signal.emit(llm_text)
            # print(f"AI: {llm_text}") # Avoid printing in thread

            # 2. Call TTS API
            # print("正在调用TTS...") # Avoid printing in thread
            used_tts_api_choice = self.tts_config.get('tts_api_choice', '').lower()
            used_tts_api_url = self.tts_config.get('tts_api_url', '')
            used_vits_speaker_id = self.tts_config.get('vits_speaker_id')

            tts_response = None
            if used_tts_api_choice == 'gpt_sovits':
                tts_payload = {"text": llm_text}
                tts_response = requests.post(f"{used_tts_api_url}/synthesize", json=tts_payload)
            elif used_tts_api_choice == 'vits_simple_api':
                if used_vits_speaker_id is None:
                     self.error_signal.emit("错误：VITS Simple API 需要发言人ID。")
                     return
                tts_url = f"{used_tts_api_url}/voice/vits?text={requests.utils.quote(llm_text)}&id={used_vits_speaker_id}"
                tts_response = requests.get(tts_url)
            else:
                self.error_signal.emit(f"不支持的TTS API选择: {self.tts_config.get('tts_api_choice')}")
                return

            tts_response.raise_for_status()

            # 3. Save audio data
            timestamp = int(time.time())
            audio_filename = f"tts_{timestamp}.wav"
            audio_filepath = os.path.join(audio_save_dir, audio_filename)

            with open(audio_filepath, 'wb') as audio_file:
                audio_file.write(tts_response.content)

            self.tts_audio_signal.emit(audio_filepath)

        except requests.exceptions.RequestException as e:
            self.error_signal.emit(f"API请求错误: {e}")
        except Exception as e:
            self.error_signal.emit(f"发生错误: {e}")

# --- Live2D Widget for rendering the model ---
class Live2DWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # QOpenGLFunctions.__init__(self) # Removed QOpenGLFunctions initialization

        self.model: live2d.v3.LAppModel | None = None # Use live2d.v3.LAppModel type hint
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update) # Connect timer to update the widget
        self.timer.start(16) # Update at roughly 60 FPS (1000ms / 60 = 16.67ms)

        self._last_frame_time = time.time() # Add attribute to track last frame time

    def initializeGL(self):
        print("Live2DWidget: Initializing OpenGL and Live2D...")
        try:
            # Initialize OpenGL functions using live2d.v3
            live2d.v3.init() # Initialize Live2D framework
            live2d.v3.glInit() # Initialize OpenGL functions
            print("Live2D Framework and OpenGL initialized.")

            # Set clear color (transparent black) using live2d.v3
            live2d.v3.clearBuffer(0.0, 0.0, 0.0, 0.0)
            print("OpenGL buffer cleared.")

            # Enable blending for transparency using live2d.v3 (assuming these wrap gl functions)
            try:
                # Try using live2d.v3 wrapped functions first
                live2d.v3.glEnable(live2d.v3.GL_BLEND)
                live2d.v3.glBlendFunc(live2d.v3.GL_SRC_ALPHA, live2d.v3.GL_ONE_MINUS_SRC_ALPHA)
                print("OpenGL blending enabled using live2d.v3.")
            except AttributeError:
                # Fallback to direct PyOpenGL calls if live2d.v3 doesn't wrap them like this
                print("Warning: live2d.v3 blending functions not found. Attempting direct PyOpenGL calls.")
                # The necessary imports for PyOpenGL are now at the top of the file
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                print("OpenGL blending enabled using PyOpenGL.")


            # TODO: Load a default model here or provide a method to load models later
            # self.load_model("path/to/your/model/file.model3.json")

            # Example (replace with your model path):
            # Please replace the path in this line with the actual path to your .model3.json file, using forward slashes / or raw strings r"..."
            # Example (using forward slashes):
            self.load_model("C:/Users/hp/Desktop/uncomm/py.turtle/drawAutoDetect/chat_mod/live2d_mod/丛雨live2d第二版/Murasame.model3.json")
            # Example (using raw strings):
            # self.load_model(r"")
            print("Live2D model loading attempted in initializeGL.")

        except Exception as e:
            print(f"Error during Live2D/OpenGL initialization: {e}")
            # Optionally disable rendering if initialization fails
            self.model = None

    def paintGL(self):
        # Clear the color buffer using live2d.v3
        live2d.v3.clearBuffer(0.0, 0.0, 0.0, 0.0) # Clear with transparency each frame

        # Render the Live2D model if loaded
        if self.model:
            # print("Rendering Live2D model...") # Avoid spamming print

            # --- Set up OpenGL matrices for 2D rendering ---
            # Ensure OpenGL context is current (QOpenGLWidget handles this, but good practice)
            self.makeCurrent()

            # Set up projection matrix
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            # Set up orthographic projection based on widget size
            # This maps the widget's pixel coordinates (0,0) to (width, height) to the OpenGL coordinate system
            glOrtho(0, self.width(), self.height(), 0, -1, 1) # (left, right, bottom, top, near, far)

            # Set up modelview matrix
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()

            # Adjust model position and scale
            # Assume model is defined in 0..2 range, translate its bottom-left to the origin (0,0) in widget coords
            glTranslate(0.0, self.height(), 0.0) # Move origin to bottom-left of widget
            glScale(self.width() / 2.0, -self.height() / 2.0, 1.0) # Scale to fit widget and flip Y axis (OpenGL Y is up)
            # The scaling factor self.width() / 2.0 and self.height() / 2.0 assumes the model canvas is 2x2 units
            # You might need to adjust the scale based on your model's actual canvas size defined in .model3.json
            # For example, if your model canvas size is 1000x1500, scale factors might be self.width()/1000, -self.height()/1500
            # Let's try a simple scale to fit the height for now, maintaining aspect ratio
            # Calculate aspect ratios
            widget_aspect = self.width() / self.height()
            # Assume model canvas is roughly 2 units wide for a typical humanoid model scaled to fit height
            model_width_in_widget_coords = 2.0 * (self.height() / 2.0) / (self.height() / 2.0)
            # Let's try scaling based on height, assuming model canvas height is 2.0 units
            scale_factor = self.height() / 2.0
            glTranslate(self.width() / 2.0, self.height(), 0.0) # Move origin to bottom-center of widget
            glScale(scale_factor, -scale_factor, 1.0) # Scale to fit height and flip Y
            glTranslate(-1.0, -1.0, 0.0) # Move model's center (assuming -1 to 1 range) to new origin


            # Enable client states for vertex and texture coordinate arrays
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

            # Calculate time delta and update model
            current_time = time.time()
            time_delta = current_time - self._last_frame_time

            # Update model animation and physics
            self.model.Update(time_delta) # Pass time delta to update animation
            # Attempt to update physics - method name is an assumption
            try:
                self.model.UpdatePhysics(time_delta) # Try a common method name for physics update
                # Or potentially ApplyPhysics or something similar
                # If UpdatePhysics doesn't exist, this will print an AttributeError
            except AttributeError:
                 # print("Model does not have UpdatePhysics method.") # Avoid spamming console if not found
                 pass # Ignore if the method doesn't exist

            self._last_frame_time = current_time # Update last frame time

            # Draw the model
            self.model.Draw() # Corrected method name

            # Disable client states
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
            glDisableClientState(GL_VERTEX_ARRAY)

            # --- End OpenGL setup ---

        # else:
            # print("Model not loaded, skipping rendering.") # Avoid spamming print

    def resizeGL(self, width, height):
        print(f"Live2DWidget: Resizing to {width}x{height}")
        # Adjust viewport using OpenGL.GL.glViewport
        glViewport(0, 0, width, height) # Use glViewport from PyOpenGL
        # Update model matrix if needed based on aspect ratio
        if self.model:
             # This might need adjustment based on how live2d-py handles projection
             # For simplicity, not adjusting projection here, might need a custom method in model
             # Use self.model.Resize if available and needed
             try:
                 self.model.Resize(width, height)
                 print("Model resize method called.")
             except AttributeError:
                 # Resize method might not exist or work as expected, ignore for now
                 print("Model does not have a Resize method or it failed.")
                 pass

    def load_model(self, model_json_path):
        print(f"Attempting to load model from: {model_json_path}")
        if self.model:
            self.model.release() # Release previous model resources
            self.model = None
            print("Released previous model resources.")

        try:
            # LAppModel is accessed via live2d.v3.LAppModel
            self.model = live2d.v3.LAppModel() # Use live2d.v3.LAppModel
            print("Created LAppModel instance.")
            self.model.LoadModelJson(model_json_path) # Use LoadModelJson method
            print(f"Live2D模型加载成功: {model_json_path}")

            # --- Print available animation groups and motions ---
            try:
                # Attempt to access motion groups and print them
                print("Available Motion Groups:")
                # The exact attribute name for motion groups might vary based on live2d-py implementation
                # We will try a common pattern: accessing motions or motion_groups attribute
                if hasattr(self.model, 'motions'):
                    motions_data = self.model.motions
                    if isinstance(motions_data, dict):
                        for group_name, motion_list in motions_data.items():
                            print(f"  Group '{group_name}': {len(motion_list)} motions")
                            # Optionally print motion names/paths if available
                            # for i, motion in enumerate(motion_list):
                            #     print(f"    Motion {i}: {motion.get('File') if hasattr(motion, 'get') else motion}")
                    else:
                         print(f"  Motions attribute found, but not a dictionary: {type(motions_data)}")
                elif hasattr(self.model, 'motion_groups'): # Try another possible attribute name
                     motion_groups_data = self.model.motion_groups
                     if isinstance(motion_groups_data, dict):
                         for group_name, motion_list in motion_groups_data.items():
                             print(f"  Group '{group_name}': {len(motion_list)} motions")
                     else:
                         print(f"  motion_groups attribute found, but not a dictionary: {type(motion_groups_data)}")
                else:
                    print("  Could not find 'motions' or 'motion_groups' attributes on the model object.")

            except Exception as e:
                print(f"Error listing motions: {e}")
            # --- End Print available animation groups and motions ---

            # Trigger a repaint after loading the model
            self.update()
        except Exception as e:
            print(f"Live2D模型加载失败: {e}")
            self.model = None

    def cleanupGL(self):
        print("Live2DWidget: Cleaning up OpenGL and Live2D...")
        try:
            # Release OpenGL resources and Live2D framework
            if self.model:
                self.model.release()
                self.model = None
                print("Released model resources.")
            # Release OpenGL shaders etc. using live2d.v3
            live2d.v3.glRelease()
            print("OpenGL resources released.")
            # Dispose Live2D framework using live2d.v3
            live2d.v3.dispose()
            print("Live2D framework disposed.")
        except Exception as e:
             print(f"Error during Live2D/OpenGL cleanup: {e}")

    def handle_llm_response(self, response_text):
        # Display AI response in chat history
        self.chat_history.append(f"AI: {response_text}")

        # --- Trigger model animation based on response_text ---
        if self.model_display_area and self.model_display_area.model:
            model = self.model_display_area.model
            available_motions = {
                'Idle': [0],
                'Tapface': [0, 1],
                'Taphair': [0, 1],
                'Tapxiongbu': [0, 1],
                'Tapqunzi': [0, 1],
                'Tapleg': [0, 1, 2]
            } # Define available motions based on the log output

            triggered = False

            # Simple keyword mapping (can be expanded)
            if any(keyword in response_text for keyword in ['你好', '您好', '哈喽', '谢谢', '再见']):
                # Trigger a friendly animation, e.g., from Tapface or Idle
                if 'Tapface' in available_motions:
                    group = 'Tapface'
                    index = random.choice(available_motions[group])
                    model.StartMotion(group, index, 2) # Using priority 2 (Normal)
                    print(f"Triggered animation: {group}_{index} based on keyword.")
                    triggered = True
                elif 'Idle' in available_motions:
                     group = 'Idle'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered animation: {group}_{index} (Idle) based on keyword fallback.")
                     triggered = True

            # Add more keyword mappings as needed
            elif any(keyword in response_text for keyword in ['头发']):
                 if 'Taphair' in available_motions:
                     group = 'Taphair'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered animation: {group}_{index} based on keyword.")
                     triggered = True

            elif any(keyword in response_text for keyword in ['腿']):
                 if 'Tapleg' in available_motions:
                     group = 'Tapleg'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered animation: {group}_{index} based on keyword.")
                     triggered = True

            # Fallback: if no specific keyword matched, play a random general animation or Idle
            if not triggered:
                general_groups = ['Tapface', 'Tapqunzi', 'Tapleg', 'Taphair'] # Consider these as general interaction animations
                valid_general_groups = [g for g in general_groups if g in available_motions and available_motions[g]]

                if valid_general_groups:
                    group = random.choice(valid_general_groups)
                    index = random.choice(available_motions[group])
                    model.StartMotion(group, index, 2)
                    print(f"Triggered random general animation: {group}_{index} as fallback.")
                elif 'Idle' in available_motions:
                     group = 'Idle'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered random Idle animation: {group}_{index} as final fallback.")
                else:
                     print("No suitable animation found to trigger.")

        # --- End Trigger model animation ---

        # TODO: Trigger model talking animation based on response_text
        # This would involve calling methods on self.model_display_area.model (now LAppModel)
        # For example: self.model_display_area.model.StartMotion("talk", motion_index, priority)

    def play_audio(self, audio_filepath):
        # Play the generated audio file
        print(f"正在播放语音: {audio_filepath}")
        # Use winsound for Windows
        if sys.platform == "win32":
            try:
                # winsound.SND_ASYNC plays without blocking the GUI
                winsound.PlaySound(audio_filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                self.chat_history.append(f"系统: 播放音频失败: {e}")
        elif sys.platform == "darwin":
            # macOS
            os.system(f"afplay {audio_filepath}") # This might block, consider QProcess
        else:
            # Linux
            os.system(f"aplay {audio_filepath}") # This might block, consider QProcess
        # TODO: Clean up audio file after playback finishes (more complex with async)

class DesktopPetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("DesktopPetApp: Initializing main window...")

        self.setWindowTitle("桌面宠物")
        self.setGeometry(100, 100, 600, 800) # 初始窗口大小

        # --- 加载配置并初始化API客户端 ---
        print("DesktopPetApp: Loading config and initializing API client...")
        self.config = load_config(config_file_path)
        self.client = None
        self.tts_config = {}
        self.system_prompt = "你是一个人工智能助手，输出格式为文本文档模式，请不要输出markdown格式"

        if self.config:
            try:
                self.client = OpenAI(api_key=self.config.get('llm_api_key'), base_url=self.config.get('llm_base_url'))
                self.tts_config = {
                    'tts_api_choice': self.config.get('tts_api_choice'),
                    'tts_api_url': self.config.get('tts_api_url'),
                    'vits_speaker_id': self.config.get('vits_speaker_id')
                }
                self.system_prompt = self.config.get('system_prompt', self.system_prompt)
                print("配置加载成功，API客户端已初始化。")
            except Exception as e:
                print(f"API客户端初始化失败: {e}\n请检查 config.json 文件。")
                # Optionally disable input if API init fails
                # self.user_input.setEnabled(False)
                # self.send_button.setEnabled(False)
        else:
            print("config.json 未找到或加载失败，请确保文件存在且包含有效配置。")
            print("您可以使用 chat1.4.py 运行一次来生成 config.json 文件。")
            # Optionally disable input if no config
            # self.user_input.setEnabled(False)
            # self.send_button.setEnabled(False)

        # 创建主布局和中心部件
        print("DesktopPetApp: Setting up layouts and widgets...")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- 模型显示区域 (使用 Live2DWidget) ---
        self.model_display_area = Live2DWidget() # 使用 Live2DWidget
        # self.model_display_area.setStyleSheet("background-color: lightgrey;") # Remove background style
        main_layout.addWidget(self.model_display_area, 4) # 4倍拉伸因子

        # --- 聊天交互区域 ---
        chat_area_layout = QVBoxLayout()

        # 聊天历史显示框
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True) # 设置为只读
        chat_area_layout.addWidget(self.chat_history) # 1倍拉伸因子

        # 用户输入区域 (输入框 + 发送按钮)
        input_layout = QHBoxLayout()
        self.user_input = QLineEdit()
        self.send_button = QPushButton("发送")
        self.switch_model_button = QPushButton("切换模型") # Add new button

        input_layout.addWidget(self.user_input)
        input_layout.addWidget(self.send_button)
        input_layout.addWidget(self.switch_model_button) # Add switch model button

        chat_area_layout.addLayout(input_layout)

        # 将聊天区域布局添加到主布局中
        main_layout.addLayout(chat_area_layout, 1) # 1倍拉伸因子

        # 连接信号和槽 (例如，发送按钮点击事件)
        self.send_button.clicked.connect(self.send_message)
        self.user_input.returnPressed.connect(self.send_message) # 回车也发送
        self.switch_model_button.clicked.connect(self.switch_model) # Connect switch model button

        # Initialize worker thread attribute
        self.worker = None

        # --- Model switching attributes ---
        # Add your model paths here
        self.model_paths = [
            "C:/Users/hp/Desktop/uncomm/py.turtle/drawAutoDetect/chat_mod/live2d_mod/丛雨live2d第二版/Murasame.model3.json",
            # Add paths to other .model3.json files for switching
            # Example: "/path/to/your/second/model/model.model3.json",
            # Example: "/path/to/your/third/model/model.model3.json",
        ]
        self.current_model_index = 0
        # --- End Model switching attributes ---

    def send_message(self):
        if not self.client or not self.config:
            self.chat_history.append("系统: API客户端未初始化或配置丢失，无法发送消息。")
            return

        # Get user input text
        message = self.user_input.text()
        if not message:
            return # Do nothing if input is empty

        # Display user message in chat history
        self.chat_history.append(f"你: {message}")

        # Clear input box
        self.user_input.clear()

        # Disable input while waiting for response
        self.user_input.setEnabled(False)
        self.send_button.setEnabled(False)

        # Create and start worker thread for API calls
        self.worker = WorkerThread(self.client, message, self.tts_config, self.system_prompt)
        self.worker.llm_response_signal.connect(self.handle_llm_response)
        self.worker.tts_audio_signal.connect(self.play_audio)
        self.worker.error_signal.connect(self.handle_error)
        # Connect finished signal to re-enable input
        self.worker.finished.connect(self.re_enable_input)
        self.worker.start()

    def handle_llm_response(self, response_text):
        # Display AI response in chat history
        self.chat_history.append(f"AI: {response_text}")

        # --- Trigger model animation based on response_text ---
        if self.model_display_area and self.model_display_area.model:
            model = self.model_display_area.model
            available_motions = {
                'Idle': [0],
                'Tapface': [0, 1],
                'Taphair': [0, 1],
                'Tapxiongbu': [0, 1],
                'Tapqunzi': [0, 1],
                'Tapleg': [0, 1, 2]
            } # Define available motions based on the log output

            triggered = False

            # Simple keyword mapping (can be expanded)
            if any(keyword in response_text for keyword in ['你好', '您好', '哈喽', '谢谢', '再见']):
                # Trigger a friendly animation, e.g., from Tapface or Idle
                if 'Tapface' in available_motions:
                    group = 'Tapface'
                    index = random.choice(available_motions[group])
                    model.StartMotion(group, index, 2) # Using priority 2 (Normal)
                    print(f"Triggered animation: {group}_{index} based on keyword.")
                    triggered = True
                elif 'Idle' in available_motions:
                     group = 'Idle'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered animation: {group}_{index} (Idle) based on keyword fallback.")
                     triggered = True

            # Add more keyword mappings as needed
            elif any(keyword in response_text for keyword in ['头发']):
                 if 'Taphair' in available_motions:
                     group = 'Taphair'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered animation: {group}_{index} based on keyword.")
                     triggered = True

            elif any(keyword in response_text for keyword in ['腿']):
                 if 'Tapleg' in available_motions:
                     group = 'Tapleg'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered animation: {group}_{index} based on keyword.")
                     triggered = True

            # Fallback: if no specific keyword matched, play a random general animation or Idle
            if not triggered:
                general_groups = ['Tapface', 'Tapqunzi', 'Tapleg', 'Taphair'] # Consider these as general interaction animations
                valid_general_groups = [g for g in general_groups if g in available_motions and available_motions[g]]

                if valid_general_groups:
                    group = random.choice(valid_general_groups)
                    index = random.choice(available_motions[group])
                    model.StartMotion(group, index, 2)
                    print(f"Triggered random general animation: {group}_{index} as fallback.")
                elif 'Idle' in available_motions:
                     group = 'Idle'
                     index = random.choice(available_motions[group])
                     model.StartMotion(group, index, 2)
                     print(f"Triggered random Idle animation: {group}_{index} as final fallback.")
                else:
                     print("No suitable animation found to trigger.")

        # --- End Trigger model animation ---

        # TODO: Trigger model talking animation based on response_text
        # This would involve calling methods on self.model_display_area.model (now LAppModel)
        # For example: self.model_display_area.model.StartMotion("talk", motion_index, priority)

    def play_audio(self, audio_filepath):
        # Play the generated audio file
        print(f"正在播放语音: {audio_filepath}")
        # Use winsound for Windows
        if sys.platform == "win32":
            try:
                # winsound.SND_ASYNC plays without blocking the GUI
                winsound.PlaySound(audio_filepath, winsound.SND_FILENAME | winsound.SND_ASYNC)
            except Exception as e:
                self.chat_history.append(f"系统: 播放音频失败: {e}")
        elif sys.platform == "darwin":
            # macOS
            os.system(f"afplay {audio_filepath}") # This might block, consider QProcess
        else:
            # Linux
            os.system(f"aplay {audio_filepath}") # This might block, consider QProcess
        # TODO: Clean up audio file after playback finishes (more complex with async)

    def handle_error(self, error_message):
        # Display error message in chat history
        self.chat_history.append(f"系统: 错误: {error_message}")

    def re_enable_input(self):
        # Re-enable input fields after API calls finish
        self.user_input.setEnabled(True)
        self.send_button.setEnabled(True)
        self.user_input.setFocus() # Put focus back to input field

    # --- Model Switching Method ---
    def switch_model(self):
        if not self.model_paths:
            print("No model paths configured for switching.")
            return

        # Move to the next model in the list
        self.current_model_index = (self.current_model_index + 1) % len(self.model_paths)
        next_model_path = self.model_paths[self.current_model_index]

        print(f"Switching to model: {next_model_path}")

        # Load the new model in the Live2DWidget
        if self.model_display_area:
            self.model_display_area.load_model(next_model_path)
        else:
            print("Model display area not initialized.")
    # --- End Model Switching Method ---


if __name__ == "__main__":
    print("Main application started.")
    app = QApplication(sys.argv)
    # Need to set OpenGL format before creating QApplication instance for consistent behavior
    # Re-enable OpenGL format setting
    # from PyQt6.QtGui import QSurfaceFormat # Already imported at the top
    # Import OpenGLContextProfile
    # from PyQt6.QtGui import QOpenGLContextProfile # Import OpenGLContextProfile - Incorrect path
    # from PyQt6.QtOpenGL import QOpenGLContextProfile # Corrected import path - Still incorrect

    fmt = QSurfaceFormat()
    # Use a compatible OpenGL version, 3.3 is often a good default
    fmt.setVersion(3, 3)
    # Use CoreProfile for modern OpenGL, CompatibilityProfile if needed for older features
    # fmt.setProfile(QSurfaceFormat.CoreProfile)
    # Using NoProfile as it's sometimes more compatible across drivers/versions for simple cases
    # Corrected profile access
    fmt.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile) # Request CompatibilityProfile
    QSurfaceFormat.setDefaultFormat(fmt)
    print("OpenGL surface format set.")

    window = DesktopPetApp()
    print("DesktopPetApp window created.")
    window.show()
    print("DesktopPetApp window show() called.")

    # Ensure cleanupGL is called when the application quits
    app.aboutToQuit.connect(window.model_display_area.cleanupGL)
    print("CleanupGL connected to aboutToQuit.")

    print("Starting application event loop...")
    sys.exit(app.exec())
    print("Application event loop finished.") 