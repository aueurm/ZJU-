"""
PDF文件解析服务
职责：解析PDF教材文件，提取章节结构和内容
"""
import re
import fitz  # PyMuPDF
from typing import List, Dict
from app.models import Chapter


class PDFParserService:
    """PDF解析服务"""

    def __init__(self):
        # 章节标题正则匹配模式
        self.chapter_pattern = re.compile(r'^第[一二三四五六七八九十百千万\d]+章\s*')

    def parse(self, file_path: str) -> Dict:
        """
        解析PDF文件
        返回：教材结构化数据
        """
        doc = fitz.open(file_path)
        chapters = []

        current_chapter = None
        current_content = []
        page_count = len(doc)

        for page_num, page in enumerate(doc):
            text = page.get_text()

            # 跳过页眉页脚（识别重复出现的短文本）
            text = self._filter_header_footer(text, page_num)

            # 检测章节标题
            chapter_title = self._detect_chapter_title(text)

            if chapter_title:
                # 保存之前的章节
                if current_chapter:
                    chapters.append(self._create_chapter(
                        current_chapter,
                        current_content,
                        page_num - len(current_content)
                    ))

                current_chapter = chapter_title
                current_content = [text]
            else:
                if current_chapter:
                    current_content.append(text)

        # 保存最后一个章节
        if current_chapter:
            chapters.append(self._create_chapter(
                current_chapter,
                current_content,
                page_num - len(current_content) + 1
            ))

        doc.close()

        return {
            "total_pages": page_count,
            "chapters": chapters
        }

    def _filter_header_footer(self, text: str, page_num: int) -> str:
        """过滤页眉页脚（简化版，实际需更复杂逻辑）"""
        lines = text.split('\n')
        # 移除首尾空白行
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        return '\n'.join(lines)

    def _detect_chapter_title(self, text: str) -> str:
        """检测章节标题"""
        lines = text.split('\n')
        for line in lines[:5]:  # 只检查前5行
            line = line.strip()
            if self.chapter_pattern.match(line):
                return line
        return None

    def _create_chapter(self, title: str, contents: List[str], start_page: int) -> Chapter:
        """创建章节对象"""
        content = '\n'.join(contents)
        char_count = len(content)

        return Chapter(
            chapter_id=f"ch_{len(contents):03d}",
            title=title,
            page_start=start_page,
            page_end=start_page + len(contents) - 1,
            content=content,
            char_count=char_count
        )