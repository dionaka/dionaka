from astrbot.api.event import AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.all import *
import aiohttp
import random
import struct
from io import BytesIO


async def image_obfus_fast(img_data):
    """快速图片哈希破坏 - 减小视觉变化"""
    """
    if len(img_data) < 200:
        return img_data
    try:
        img_bytes = bytearray(img_data)
        file_size = len(img_bytes)
        modifications = 1
        start_pos = int(file_size * 0.4)
        end_pos = int(file_size * 0.9)
        valid_positions = list(range(start_pos, end_pos))
        if len(valid_positions) < modifications:
            return img_data
        selected_positions = random.sample(valid_positions, modifications)
        
        for pos in selected_positions:
            original_byte = img_bytes[pos]
            # 保持微小的修改幅度
            modification = random.choice([-1, 1])
            new_byte = (original_byte + modification) % 256
            img_bytes[pos] = new_byte
        return bytes(img_bytes)
    except Exception as e:
        logger.warning(f"哈希破坏失败: {e}")
        return img_data
    """
    return img_data


# 装饰器、插件注册声明
@register(
    "astrbot_plugin_setu",
    "flash_back__",
    "Astrbot色图插件，支持自定义配置与标签指定",
    "1.2.4",
    "https://github.com/Raven95676/astrbot_plugin_setu",
)

# PluginSetu继承父Start类
class PluginSetu(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config or {}
        self.allow_r18 = self.config.get("allow_r18", False)
        self.allow_r18_groups = self.config.get("allow_r18_groups", [])
        self.disallow_r18_groups = self.config.get("disallow_r18_groups", [])
        self.exclude_ai = self.config.get("exclude_ai", False)
        self.image_hash_break = self.config.get("image_hash_break", False)
        self.send_forward = self.config.get("send_forward", False)
        self.image_size = self.config.get("image_size", "regular")
        self.image_info = self.config.get("image_info", "基本信息")
        self.session = None
        self.semaphore = asyncio.Semaphore(5)
        
        
    async def initialize_session(self):
        """初始化全局的、带连接池的ClientSession"""
        if self.session is None or self.session.closed:
            # 创建TCP连接器，配置连接池
            connector = aiohttp.TCPConnector(
                limit=50,        # 连接池总数限制
                limit_per_host=15, # 对同一目标主机（lolicon API）的最大连接数
                ttl_dns_cache=600, # DNS缓存时间（秒），减少DNS查询
                enable_cleanup_closed=True, # 自动清理关闭的连接
                use_dns_cache=True  # 显式启用DNS缓存
            )
            # 配置超时策略
            timeout = aiohttp.ClientTimeout(
                total=120,       # 总操作超时
                connect=10,      # 连接建立超时
                sock_read=60     # 从socket读取数据的超时
            )
            # 创建会话
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers={'User-Agent': 'YourBot/1.0'}  # 可设置默认UA
            )
        return self.session

        
    async def cleanup(self):
        """插件卸载或机器人退出时调用，用于清理资源"""
        if self.session and not self.session.closed:
            await self.session.close()
            logger.info("aiohttp ClientSession已关闭。")

        
    def parse_tags(self, tags: str) -> list:
        """标签解析，在setu函数中调用，确保与API兼容"""
        stripped = tags.strip()
        
        # 若tags为空返回空列表
        if not tags or not stripped:
            return []

        # 去除setu前缀
        if stripped.lower().startswith("setu"):
            stripped = stripped[4:].strip()
            
        # 若指令后内容为空返回空列表
        if not stripped:
            return []

        # 内容支持多种分隔符
        if " " in stripped:
            tags_list = [tag.strip() for tag in stripped.split() if tag.strip()]
        elif "," in stripped:
            tags_list = [tag.strip() for tag in stripped.split(",") if tag.strip()]
        elif "/" in stripped:
            tags_list = [tag.strip() for tag in stripped.split("/") if tag.strip()]   
        else:
            tags_list = [stripped]

        # 限制最多20个标签
        return tags_list[:20]
        
        
    # 装饰器，修饰setu函数为命令行命令
    @command("setu")
    async def setu(self, event: AstrMessageEvent):
        tags = event.message_str
        
        # 若tags参数为空，返回空列表
        if tags is None:
            parsed_tags = []
            
        # 若tags参数不为空，调用类内parse_tags函数将内容拆分成列表返回
        else:
            parsed_tags = self.parse_tags(tags)

        # 有效列表检查首个内容是否为help，将预置文本返回框架，结束函数
        if parsed_tags and parsed_tags[0].lower() == "help":
            yield event.plain_result(
                "使用方法：\n"
                "  输入 `setu` 获取一张随机色图\n"
                "  输入 `setu 标签` 获取特定标签的色图\n"
                "  输入 `setu 标签1 标签2` 或 `setu 标签1,标签2` 或 `setu 标签1/标签2` 获取多个标签的色图\n"
                "  示例：`setu diona`、`setu 原神 萝莉`、`setu 原神,萝莉`、`setu 原神/萝莉`"
            )
            return
        
        # R18权限判断
        # self.allow_r18_groups列表留空为允许所有群r18
        allow_r18 = self.allow_r18
        if allow_r18:
            group_id = event.get_group_id()
            if group_id:
            
                # 将禁止r18群组权限设为False
                if self.allow_r18_groups and group_id not in self.allow_r18_groups:
                    allow_r18 = False
                elif self.disallow_r18_groups and group_id in self.disallow_r18_groups:
                    allow_r18 = False
                    
        # 转发权限判断
        send_forward = self.send_forward
        if send_forward and event.get_platform_name() != "aiocqhttp":
            send_forward = False
            logger.warning("当前平台不支持合并转发，已禁用该功能")
        
        # 确保会话已初始化
        if self.session is None:
            await self.initialize_session()
                
        # 调用api，尝试3次
        retry_count = 0
        while retry_count < 3:
            try:
                async with self.semaphore:
                    # 构建请求数据
                    # r18标签，size标签，excludeAI标签，num标签(固定每次返回1张)
                    data = {
                        "r18": 2 if allow_r18 else 0,
                        "size": [self.image_size],
                        "excludeAI": self.exclude_ai,
                        "num": 1
                    }
                    
                    # tag标签
                    if parsed_tags:
                        data["tag"] = parsed_tags
                    
                    # 输出data日志
                    logger.info(f"[色图插件] 请求API: {data}")

                    async with self.session.post(
                        "https://api.lolicon.app/setu/v2",
                        json=data,
                        timeout=aiohttp.ClientTimeout(total=120),
                    ) as response:
                        response.raise_for_status()
                        resp = await response.json()
                        
                        #若api返回到data数据为空，退出函数
                        if not resp["data"]:
                            if parsed_tags:
                                yield event.plain_result(f"未找到标签为 {'/'.join(parsed_tags)} 的图片，请尝试其他标签。")
                            else:
                                yield event.plain_result("未获取到任何图片数据。")
                            return

                        img_info = resp["data"][0]
                        img_url = img_info["urls"][self.image_size]
                        img_title = img_info["title"]
                        img_author = img_info["author"]
                        img_pid = img_info["pid"]
                        img_tags = img_info["tags"]

                        # ↓严格的标签验证
                        # ↑删了，有什么用嘛

                        logger.info(f"获取到图片: {img_title} by {img_author}, 标签: {img_tags}")

                        try:
                            async with self.session.get(img_url, timeout=aiohttp.ClientTimeout(total=120)) as img_response:
                                img_response.raise_for_status()
                                # 使用流式读取，避免大文件内存峰值
                                chunk_size = 8192
                                chunks = []
                                async for chunk in img_response.content.iter_chunked(chunk_size):
                                    chunks.append(chunk)
                                img_data = b''.join(chunks)

                                if self.image_hash_break:
                                    img_data = await image_obfus_fast(img_data)

                                # 构造消息链
                                if self.image_info == "只有图片":
                                    chain = [Image.fromBytes(img_data)]
                                elif self.image_info == "基本信息":
                                    chain = [
                                        Image.fromBytes(img_data),
                                        Plain(f"标题：{img_title}\n作者：{img_author}\nPID：{img_pid}")
                                    ]
                                else:  # 包含标签
                                    tag_text = ' '.join(f'#{tag}' for tag in (img_tags or []))
                                    chain = [
                                        Image.fromBytes(img_data),
                                        Plain(f"标题：{img_title}\n作者：{img_author}\nPID：{img_pid}\n标签：{tag_text}")
                                    ]

                                # 是否使用合并转发
                                if send_forward:
                                    node = Node(
                                        uin=event.get_self_id(),
                                        name="色图姬",
                                        content=chain
                                    )
                                    yield event.chain_result([node])
                                else:
                                    yield event.chain_result(chain)
                                return

                        except aiohttp.ClientError as e:
                            retry_count += 1
                            logger.warning(f"图片下载失败（第{retry_count}次）: {e}")
                            continue

            except asyncio.TimeoutError:
                retry_count += 1
                logger.warning(f"请求超时（第{retry_count}次重试）")
            except aiohttp.ClientError as e:
                retry_count += 1
                logger.error(f"网络请求失败（第{retry_count}次）: {e}")
            except Exception as e:
                logger.error(f"未知错误: {e}", exc_info=True)
                yield event.plain_result(f"发生错误: {str(e)}")
                return
        yield event.plain_result(f"获取图片失败，已重试 {retry_count} 次。")
