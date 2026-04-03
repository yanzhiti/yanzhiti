#!/usr/bin/env python3
"""
衍智体 (YANZHITI) 推广视频生成器
使用 OpenCV 生成 PPT 幻灯片视频，配合 edge-tts 生成真人语音解说
修复中文显示问题 - 使用 Pillow 绘制中文
"""

import cv2
import numpy as np
import os
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
import asyncio
from PIL import Image, ImageDraw, ImageFont


@dataclass
class Slide:
    """幻灯片数据类"""
    title: str
    content: List[str]
    duration: int  # 秒数
    narration: str  # 解说文字


class VideoGenerator:
    """视频生成器"""
    
    def __init__(self, output_dir: str = "."):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 视频参数
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # 颜色配置
        self.bg_color = (102, 126, 234)  # 渐变色起始 (BGR)
        self.bg_color2 = (118, 75, 162)  # 渐变色结束 (BGR)
        self.text_color = (255, 255, 255)
        self.accent_color = (168, 237, 234)
        
        # 尝试加载中文字体
        self.font_paths = [
            "/System/Library/Fonts/PingFang.ttc",  # macOS 苹方字体
            "/System/Library/Fonts/STHeiti Light.ttc",  # macOS 黑体
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",  # Linux 文泉驿
            "C:/Windows/Fonts/simhei.ttf",  # Windows 黑体
            "C:/Windows/Fonts/msyh.ttc",  # Windows 雅黑
        ]
        self.font = self._load_font()
        
    def _load_font(self):
        """加载中文字体"""
        for font_path in self.font_paths:
            if os.path.exists(font_path):
                try:
                    # 尝试不同字号
                    return {
                        'large': ImageFont.truetype(font_path, 72),
                        'medium': ImageFont.truetype(font_path, 48),
                        'normal': ImageFont.truetype(font_path, 36),
                        'small': ImageFont.truetype(font_path, 28),
                        'table': ImageFont.truetype(font_path, 24),
                    }
                except Exception as e:
                    print(f"无法加载字体 {font_path}: {e}")
                    continue
        
        print("警告: 未找到中文字体，使用默认字体")
        return {
            'large': ImageFont.load_default(),
            'medium': ImageFont.load_default(),
            'normal': ImageFont.load_default(),
            'small': ImageFont.load_default(),
            'table': ImageFont.load_default(),
        }
    
    def create_gradient_background(self) -> Image.Image:
        """创建渐变背景"""
        img = Image.new('RGB', (self.width, self.height))
        draw = ImageDraw.Draw(img)
        
        for y in range(self.height):
            ratio = y / self.height
            r = int(self.bg_color[2] * (1 - ratio) + self.bg_color2[2] * ratio)
            g = int(self.bg_color[1] * (1 - ratio) + self.bg_color2[1] * ratio)
            b = int(self.bg_color[0] * (1 - ratio) + self.bg_color2[0] * ratio)
            draw.line([(0, y), (self.width, y)], fill=(r, g, b))
        
        return img
    
    def draw_text(self, draw: ImageDraw.Draw, text: str, position: Tuple[int, int],
                  font_size: str = 'normal', color: Tuple[int, int, int] = None,
                  center: bool = True) -> Tuple[int, int]:
        """绘制文字，返回文字尺寸"""
        if color is None:
            color = self.text_color
        
        font = self.font.get(font_size, self.font['normal'])
        
        # 获取文字尺寸
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        if center:
            x = position[0] - text_width // 2
        else:
            x = position[0]
        y = position[1] - text_height // 2
        
        # 绘制阴影
        shadow_offset = 2
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font, fill=(0, 0, 0, 128))
        
        # 绘制主文字
        draw.text((x, y), text, font=font, fill=color)
        
        return (text_width, text_height)
    
    def draw_badge(self, draw: ImageDraw.Draw, text: str, position: Tuple[int, int]) -> int:
        """绘制徽章，返回徽章宽度"""
        font = self.font['small']
        
        # 获取文字尺寸
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        padding = 15
        x, y = position
        
        # 绘制圆角矩形背景
        badge_width = text_width + padding * 2
        badge_height = text_height + padding
        
        # 使用白色半透明背景
        overlay = Image.new('RGBA', (self.width, self.height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rounded_rectangle(
            [(x, y - badge_height // 2), (x + badge_width, y + badge_height // 2)],
            radius=20,
            fill=(255, 255, 255, 180)
        )
        
        # 合并到主图像
        # 这里简化处理，直接绘制
        draw.rounded_rectangle(
            [(x, y - badge_height // 2), (x + badge_width, y + badge_height // 2)],
            radius=20,
            fill=(255, 255, 255),
            outline=(200, 200, 200),
            width=1
        )
        
        # 绘制文字
        draw.text((x + padding, y - text_height // 2), text, font=font, fill=(102, 126, 234))
        
        return badge_width + 20  # 返回宽度加间距
    
    def pil_to_cv2(self, pil_img: Image.Image) -> np.ndarray:
        """将 PIL Image 转换为 OpenCV 格式"""
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    
    def create_title_slide(self, slide: Slide) -> List[np.ndarray]:
        """创建标题幻灯片"""
        frames = []
        total_frames = slide.duration * self.fps
        
        for i in range(total_frames):
            # 创建渐变背景
            img = self.create_gradient_background()
            draw = ImageDraw.Draw(img)
            
            # 主标题
            self.draw_text(draw, slide.title, (self.width // 2, self.height // 2 - 80), 
                          font_size='large')
            
            # 副标题
            if slide.content:
                subtitle = slide.content[0]
                self.draw_text(draw, subtitle, (self.width // 2, self.height // 2 + 20), 
                              font_size='normal')
            
            # 徽章
            badges = ["开源免费", "Python 3.10+", "40+ 工具集"]
            badge_y = self.height // 2 + 120
            total_width = sum([self.font['small'].getlength(b) for b in badges]) + 60 + len(badges) * 20
            start_x = (self.width - int(total_width)) // 2
            
            current_x = start_x
            for badge in badges:
                width = self.draw_badge(draw, badge, (current_x, badge_y))
                current_x += width
            
            # 转换为 OpenCV 格式
            frame = self.pil_to_cv2(img)
            frames.append(frame)
        
        return frames
    
    def create_content_slide(self, slide: Slide) -> List[np.ndarray]:
        """创建内容幻灯片"""
        frames = []
        total_frames = slide.duration * self.fps
        
        for i in range(total_frames):
            img = self.create_gradient_background()
            draw = ImageDraw.Draw(img)
            
            # 标题
            self.draw_text(draw, slide.title, (self.width // 2, 100), 
                          font_size='medium')
            
            # 内容行
            y_start = 220
            line_height = 90
            
            for j, line in enumerate(slide.content):
                y = y_start + j * line_height
                
                # 动画效果 - 逐行显示
                if i > j * 10:
                    self.draw_text(draw, line, (self.width // 2, y), 
                                  font_size='normal')
            
            frame = self.pil_to_cv2(img)
            frames.append(frame)
        
        return frames
    
    def create_comparison_slide(self, slide: Slide) -> List[np.ndarray]:
        """创建对比表格幻灯片"""
        frames = []
        total_frames = slide.duration * self.fps
        
        for i in range(total_frames):
            img = self.create_gradient_background()
            draw = ImageDraw.Draw(img)
            
            # 标题
            self.draw_text(draw, slide.title, (self.width // 2, 80), 
                          font_size='medium')
            
            # 表格配置
            table_y = 160
            row_height = 70
            col_widths = [350, 500, 500]
            start_x = (self.width - sum(col_widths)) // 2
            
            # 表头
            headers = ["特性", "衍智体(YANZHITI)", "Claude Code"]
            
            # 绘制表头背景
            draw.rectangle(
                [(start_x, table_y - 10), (start_x + sum(col_widths), table_y + 50)],
                fill=(118, 75, 162)
            )
            
            x = start_x
            for header, width in zip(headers, col_widths):
                self.draw_text(draw, header, (x + width // 2, table_y + 20), 
                              font_size='small', center=True)
                x += width
            
            # 表格内容
            for j, line in enumerate(slide.content):
                if i > j * 15:  # 逐行显示动画
                    y = table_y + 70 + j * row_height
                    
                    # 分隔线
                    draw.line(
                        [(start_x, y + 30), (start_x + sum(col_widths), y + 30)],
                        fill=(200, 200, 200),
                        width=1
                    )
                    
                    # 解析行内容
                    parts = line.split("|")
                    if len(parts) == 3:
                        x = start_x
                        for part, width in zip(parts, col_widths):
                            color = self.text_color
                            if "✓" in part or "支持" in part or "免费" in part or "开源" in part:
                                color = (150, 255, 150)  # 绿色
                            elif "✗" in part or "闭源" in part or "付费" in part:
                                color = (150, 150, 255)  # 红色
                            
                            self.draw_text(draw, part.strip(), (x + width // 2, y), 
                                          font_size='table', center=True, color=color)
                            x += width
            
            frame = self.pil_to_cv2(img)
            frames.append(frame)
        
        return frames
    
    def create_code_slide(self, slide: Slide) -> List[np.ndarray]:
        """创建代码展示幻灯片"""
        frames = []
        total_frames = slide.duration * self.fps
        
        for i in range(total_frames):
            img = self.create_gradient_background()
            draw = ImageDraw.Draw(img)
            
            # 标题
            self.draw_text(draw, slide.title, (self.width // 2, 80), 
                          font_size='medium')
            
            # 代码背景
            code_x = (self.width - 1000) // 2
            code_y = 160
            code_height = len(slide.content) * 50 + 40
            
            draw.rectangle(
                [(code_x, code_y), (code_x + 1000, code_y + code_height)],
                fill=(40, 40, 40),
                outline=(100, 100, 100),
                width=2
            )
            
            # 代码内容
            for j, line in enumerate(slide.content):
                y = code_y + 30 + j * 50
                
                if i > j * 8:
                    # 代码高亮颜色
                    color = (200, 200, 200)
                    if line.startswith("git"):
                        color = (255, 150, 100)  # 橙色
                    elif line.startswith("pip"):
                        color = (100, 200, 255)  # 蓝色
                    elif line.startswith("export"):
                        color = (150, 255, 150)  # 绿色
                    elif "yanzhiti" in line:
                        color = (255, 255, 150)  # 黄色
                    
                    self.draw_text(draw, line, (code_x + 30, y), 
                                  font_size='table', color=color, center=False)
            
            frame = self.pil_to_cv2(img)
            frames.append(frame)
        
        return frames
    
    async def generate_narration(self, slides: List[Slide], output_path: str):
        """生成语音解说"""
        try:
            import edge_tts
        except ImportError:
            print("正在安装 edge-tts...")
            subprocess.run(["pip", "install", "edge-tts"], check=True)
            import edge_tts
        
        # 合并所有解说文字
        full_text = "\n\n".join([f"{slide.title}。{slide.narration}" for slide in slides])
        
        # 使用中文女声 (Xiaoxiao)
        voice = "zh-CN-XiaoxiaoNeural"
        
        communicate = edge_tts.Communicate(full_text, voice)
        await communicate.save(output_path)
        print(f"语音已保存: {output_path}")
    
    def create_video(self, slides: List[Slide], video_path: str):
        """创建视频"""
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_path, fourcc, self.fps, (self.width, self.height))
        
        for slide in slides:
            print(f"正在生成幻灯片: {slide.title}")
            
            if "对比" in slide.title:
                frames = self.create_comparison_slide(slide)
            elif slide.title == "快速开始":
                frames = self.create_code_slide(slide)
            elif slide.title == "衍智体 (YANZHITI)":
                frames = self.create_title_slide(slide)
            else:
                frames = self.create_content_slide(slide)
            
            for frame in frames:
                out.write(frame)
        
        out.release()
        print(f"视频已保存: {video_path}")
    
    def merge_video_audio(self, video_path: str, audio_path: str, output_path: str):
        """合并视频和音频"""
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"最终视频已生成: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"合并失败: {e}")
            print("请确保已安装 ffmpeg")
    
    async def generate(self):
        """生成完整推广视频"""
        # 定义幻灯片内容 - 使用简化符号避免乱码
        slides = [
            Slide(
                title="衍智体 (YANZHITI)",
                content=["开源 AI 智能编程助手 - Python 实现"],
                duration=5,
                narration="欢迎使用衍智体，一个完全开源免费的 AI 智能编程助手，基于 Python 实现。"
            ),
            Slide(
                title="为什么选择衍智体？",
                content=[
                    "完全开源 (MIT 许可证)",
                    "永久免费，无订阅费用",
                    "本地部署，保护隐私",
                    "Python 原生，易于扩展"
                ],
                duration=8,
                narration="与闭源的 Claude Code 不同，衍智体完全开源免费，支持本地部署，您的代码不会上传云端，完美保护隐私安全。"
            ),
            Slide(
                title="与 Claude Code 对比",
                content=[
                    "开源许可|完全开源|闭源商业",
                    "使用成本|永久免费|需要付费",
                    "自托管支持|本地部署|仅云服务",
                    "数据隐私|代码本地|上传云端",
                    "Python 生态|原生 Python|TypeScript"
                ],
                duration=12,
                narration="让我们看看衍智体与 Claude Code 的对比。衍智体完全开源免费，支持本地部署，代码完全在本地处理，采用原生 Python 开发。"
            ),
            Slide(
                title="40+ 开发工具集",
                content=[
                    "文件操作 - 读写、搜索、监控",
                    "Shell 执行 - Bash PowerShell",
                    "Git 操作 - 版本控制集成",
                    "Web 操作 - 网页获取 API 调用",
                    "任务管理 - 任务跟踪 分解"
                ],
                duration=10,
                narration="衍智体提供 40 多种开发工具，包括文件操作、Shell 执行、Git 操作、Web 操作和任务管理等功能。"
            ),
            Slide(
                title="技术架构",
                content=[
                    "智能查询引擎 - 高级查询处理",
                    "模块化工具系统 - 动态扩展",
                    "桥接通信系统 - 远程控制",
                    "MCP 支持 - 多模型集成"
                ],
                duration=8,
                narration="衍智体采用先进的技术架构，包括智能查询引擎、模块化工具系统、桥接通信系统，并支持 Model Context Protocol。"
            ),
            Slide(
                title="快速开始",
                content=[
                    "git clone https://github.com/yanzhiti/yanzhiti.git",
                    "pip install -e .[dev]",
                    "export YANZHITI_API_KEY=your-key",
                    "yanzhiti"
                ],
                duration=8,
                narration="开始使用衍智体非常简单。克隆仓库，安装依赖，设置 API 密钥，然后运行 yanzhiti 命令即可。"
            ),
            Slide(
                title="参与贡献",
                content=[
                    "衍智体是开源项目，欢迎社区贡献",
                    "提交 Issue 报告问题",
                    "提交 Pull Request",
                    "给项目点个 Star 支持我们"
                ],
                duration=7,
                narration="衍智体是一个开源项目，欢迎社区贡献。您可以通过提交 Issue、Pull Request 或给项目点 Star 来支持我们。"
            ),
            Slide(
                title="衍智体 (YANZHITI)",
                content=["让 AI 助力您的编程之旅", "https://github.com/yanzhiti/yanzhiti"],
                duration=5,
                narration="衍智体，让 AI 助力您的编程之旅。访问 GitHub 了解更多信息。"
            )
        ]
        
        # 生成临时文件路径
        temp_video = str(self.output_dir / "temp_video.mp4")
        temp_audio = str(self.output_dir / "temp_audio.mp3")
        final_output = str(self.output_dir / "yanzhiti_promo.mp4")
        
        print("=" * 50)
        print("开始生成推广视频")
        print("=" * 50)
        
        # 步骤 1: 生成视频
        print("\n步骤 1/3: 生成视频幻灯片...")
        self.create_video(slides, temp_video)
        
        # 步骤 2: 生成语音
        print("\n步骤 2/3: 生成语音解说...")
        await self.generate_narration(slides, temp_audio)
        
        # 步骤 3: 合并视频和音频
        print("\n步骤 3/3: 合并视频和音频...")
        self.merge_video_audio(temp_video, temp_audio, final_output)
        
        # 清理临时文件
        print("\n清理临时文件...")
        Path(temp_video).unlink(missing_ok=True)
        Path(temp_audio).unlink(missing_ok=True)
        
        print("\n" + "=" * 50)
        print(f"推广视频生成完成!")
        print(f"输出文件: {final_output}")
        print("=" * 50)


async def main():
    """主函数"""
    generator = VideoGenerator()
    await generator.generate()


if __name__ == "__main__":
    asyncio.run(main())
