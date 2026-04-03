#!/usr/bin/env python3
"""
衍智体 (YANZHITI) 推广视频生成器
使用 OpenCV 生成 PPT 幻灯片视频，配合 edge-tts 生成真人语音解说
"""

import cv2
import numpy as np
import os
import subprocess
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import List, Tuple
import asyncio


@dataclass
class Slide:
    """幻灯片数据类"""
    title: str
    content: List[str]
    duration: int  # 秒数
    narration: str  # 解说文字


class VideoGenerator:
    """视频生成器"""
    
    def __init__(self, output_dir: str = "promo_video"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 视频参数
        self.width = 1920
        self.height = 1080
        self.fps = 30
        
        # 颜色配置
        self.bg_color = (102, 126, 234)  # 渐变色起始
        self.bg_color2 = (118, 75, 162)  # 渐变色结束
        self.text_color = (255, 255, 255)
        self.accent_color = (168, 237, 234)
        
    def create_gradient_background(self, frame: np.ndarray) -> np.ndarray:
        """创建渐变背景"""
        for y in range(self.height):
            ratio = y / self.height
            r = int(self.bg_color[0] * (1 - ratio) + self.bg_color2[0] * ratio)
            g = int(self.bg_color[1] * (1 - ratio) + self.bg_color2[1] * ratio)
            b = int(self.bg_color[2] * (1 - ratio) + self.bg_color2[2] * ratio)
            frame[y, :] = (b, g, r)
        return frame
    
    def add_text(self, frame: np.ndarray, text: str, position: Tuple[int, int], 
                 font_scale: float = 1.0, color: Tuple[int, int, int] = None,
                 thickness: int = 2, center: bool = True) -> np.ndarray:
        """添加文字到帧"""
        if color is None:
            color = self.text_color
            
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # 获取文字大小
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        if center:
            x = position[0] - text_width // 2
        else:
            x = position[0]
        y = position[1]
        
        # 添加阴影
        shadow_offset = 2
        cv2.putText(frame, text, (x + shadow_offset, y + shadow_offset), 
                    font, font_scale, (0, 0, 0), thickness + 1)
        
        # 添加主文字
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
        
        return frame
    
    def add_badge(self, frame: np.ndarray, text: str, position: Tuple[int, int]) -> np.ndarray:
        """添加徽章标签"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 1
        
        (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        # 绘制圆角矩形背景
        padding = 10
        x, y = position
        cv2.rectangle(frame, (x, y - text_height - padding), 
                      (x + text_width + padding * 2, y + padding),
                      (255, 255, 255, 100), -1, cv2.LINE_AA)
        cv2.rectangle(frame, (x, y - text_height - padding), 
                      (x + text_width + padding * 2, y + padding),
                      (255, 255, 255), 1, cv2.LINE_AA)
        
        # 添加文字
        cv2.putText(frame, text, (x + padding, y), font, font_scale, 
                    (102, 126, 234), thickness)
        
        return frame
    
    def create_title_slide(self, slide: Slide) -> List[np.ndarray]:
        """创建标题幻灯片"""
        frames = []
        total_frames = slide.duration * self.fps
        
        for i in range(total_frames):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            frame = self.create_gradient_background(frame)
            
            # 动画效果 - 渐入
            alpha = min(1.0, i / (self.fps * 0.5))
            
            # 主标题
            title = slide.title
            self.add_text(frame, title, (self.width // 2, self.height // 2 - 50), 
                         font_scale=2.5, thickness=3)
            
            # 副标题
            if slide.content:
                subtitle = slide.content[0]
                self.add_text(frame, subtitle, (self.width // 2, self.height // 2 + 50), 
                             font_scale=1.2, thickness=2)
            
            # 徽章
            badges = ["⭐ 开源免费", "🐍 Python 3.10+", "🔧 40+ 工具集"]
            badge_y = self.height // 2 + 150
            total_badge_width = sum([cv2.getTextSize(b, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)[0][0] + 40 for b in badges])
            start_x = (self.width - total_badge_width) // 2
            
            for j, badge in enumerate(badges):
                self.add_badge(frame, badge, (start_x + j * 250, badge_y))
            
            frames.append(frame)
        
        return frames
    
    def create_content_slide(self, slide: Slide) -> List[np.ndarray]:
        """创建内容幻灯片"""
        frames = []
        total_frames = slide.duration * self.fps
        
        for i in range(total_frames):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            frame = self.create_gradient_background(frame)
            
            # 标题
            self.add_text(frame, slide.title, (self.width // 2, 100), 
                         font_scale=2.0, thickness=3)
            
            # 内容行
            y_start = 250
            line_height = 80
            
            for j, line in enumerate(slide.content):
                y = y_start + j * line_height
                
                # 动画效果
                if i > j * 10:  # 逐行显示
                    self.add_text(frame, line, (self.width // 2, y), 
                                 font_scale=1.0, thickness=2)
            
            frames.append(frame)
        
        return frames
    
    def create_comparison_slide(self, slide: Slide) -> List[np.ndarray]:
        """创建对比表格幻灯片"""
        frames = []
        total_frames = slide.duration * self.fps
        
        for i in range(total_frames):
            frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
            frame = self.create_gradient_background(frame)
            
            # 标题
            self.add_text(frame, slide.title, (self.width // 2, 80), 
                         font_scale=1.8, thickness=3)
            
            # 表格内容
            table_y = 180
            row_height = 70
            
            # 表头
            headers = ["特性", "衍智体 (YANZHITI)", "Claude Code"]
            col_widths = [300, 500, 500]
            start_x = (self.width - sum(col_widths)) // 2
            
            # 绘制表头背景
            cv2.rectangle(frame, (start_x, table_y - 40), 
                         (start_x + sum(col_widths), table_y + 20),
                         (118, 75, 162), -1)
            
            x = start_x + 20
            for header, width in zip(headers, col_widths):
                self.add_text(frame, header, (x + width // 2, table_y), 
                             font_scale=0.8, thickness=2, center=True)
                x += width
            
            # 表格内容
            for j, line in enumerate(slide.content):
                if i > j * 15:  # 逐行显示动画
                    y = table_y + 60 + j * row_height
                    
                    # 分隔线
                    cv2.line(frame, (start_x, y + 20), (start_x + sum(col_widths), y + 20),
                            (255, 255, 255, 100), 1)
                    
                    # 解析行内容 (格式: "特性|YANZHITI值|Claude值")
                    parts = line.split("|")
                    if len(parts) == 3:
                        x = start_x + 20
                        for part, width in zip(parts, col_widths):
                            color = self.text_color
                            if "✅" in part:
                                color = (100, 255, 100)  # 绿色
                            elif "❌" in part:
                                color = (100, 100, 255)  # 红色
                            
                            self.add_text(frame, part.strip(), (x + width // 2, y), 
                                         font_scale=0.6, thickness=1, center=True, color=color)
                            x += width
            
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
        # 定义幻灯片内容
        slides = [
            Slide(
                title="🚀 衍智体 (YANZHITI)",
                content=["开源 AI 智能编程助手 - Python 实现"],
                duration=5,
                narration="欢迎使用衍智体，一个完全开源免费的 AI 智能编程助手，基于 Python 实现。"
            ),
            Slide(
                title="🌟 为什么选择衍智体？",
                content=[
                    "✅ 完全开源 (MIT 许可证)",
                    "✅ 永久免费，无订阅费用",
                    "✅ 本地部署，保护隐私",
                    "✅ Python 原生，易于扩展"
                ],
                duration=8,
                narration="与闭源的 Claude Code 不同，衍智体完全开源免费，支持本地部署，您的代码不会上传云端，完美保护隐私安全。"
            ),
            Slide(
                title="📊 与 Claude Code 对比",
                content=[
                    "开源许可|✅ 完全开源|❌ 闭源商业",
                    "使用成本|✅ 永久免费|❌ 需要付费",
                    "自托管支持|✅ 本地部署|❌ 仅云服务",
                    "数据隐私|✅ 代码本地|❌ 上传云端",
                    "Python 生态|✅ 原生 Python|❌ TypeScript"
                ],
                duration=12,
                narration="让我们看看衍智体与 Claude Code 的对比。衍智体完全开源免费，支持本地部署，代码完全在本地处理，采用原生 Python 开发。"
            ),
            Slide(
                title="🔧 40+ 开发工具集",
                content=[
                    "📁 文件操作 - 读写、搜索、监控",
                    "⚡ Shell 执行 - Bash/PowerShell",
                    "🔀 Git 操作 - 版本控制集成",
                    "🌐 Web 操作 - 网页获取、API 调用",
                    "📋 任务管理 - 任务跟踪、分解"
                ],
                duration=10,
                narration="衍智体提供 40 多种开发工具，包括文件操作、Shell 执行、Git 操作、Web 操作和任务管理等功能。"
            ),
            Slide(
                title="🏗️ 技术架构",
                content=[
                    "⚙️ 智能查询引擎 - 高级查询处理",
                    "🧩 模块化工具系统 - 动态扩展",
                    "🌉 桥接通信系统 - 远程控制",
                    "📡 MCP 支持 - 多模型集成"
                ],
                duration=8,
                narration="衍智体采用先进的技术架构，包括智能查询引擎、模块化工具系统、桥接通信系统，并支持 Model Context Protocol。"
            ),
            Slide(
                title="🚀 快速开始",
                content=[
                    "git clone https://github.com/yanzhiti/yanzhiti.git",
                    "pip install -e '.[dev]'",
                    "export YANZHITI_API_KEY=your-key",
                    "yanzhiti"
                ],
                duration=8,
                narration="开始使用衍智体非常简单。克隆仓库，安装依赖，设置 API 密钥，然后运行 yanzhiti 命令即可。"
            ),
            Slide(
                title="🤝 参与贡献",
                content=[
                    "衍智体是开源项目，欢迎社区贡献",
                    "🐛 提交 Issue 报告问题",
                    "🔀 提交 Pull Request",
                    "⭐ 给项目点个 Star 支持我们！"
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
        print(f"✅ 推广视频生成完成!")
        print(f"📁 输出文件: {final_output}")
        print("=" * 50)


async def main():
    """主函数"""
    generator = VideoGenerator()
    await generator.generate()


if __name__ == "__main__":
    asyncio.run(main())
