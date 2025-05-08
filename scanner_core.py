import os
import re
from datetime import datetime


class PHPAuthScanner:
    def __init__(self):
        self.scan_results = []

    def generate_regex(self, keywords):
        """生成鉴权正则表达式"""
        patterns = []
        for keyword in keywords:
            escaped_keyword = re.escape(keyword)
            patterns.extend([
                rf'\b{escaped_keyword}\b',
                rf'\${escaped_keyword}\[',
                rf'{escaped_keyword}\(',
                rf'require.*{escaped_keyword}\.php',
                rf'extends\s+{escaped_keyword}',
                rf'use\s+.*{escaped_keyword}',
                rf'\${escaped_keyword}\b',
                rf'\$_{escaped_keyword}\b',
                rf'\${escaped_keyword}\s*[=!]=\s*[\'"]?\d[\'"]?'
            ])
        return re.compile('|'.join(patterns), re.IGNORECASE)

    def scan_directory(self, directory, pattern):
        """扫描指定目录中的PHP文件"""
        no_auth_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.php'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            stripped_content = content.strip()
                            if len(stripped_content) <= 5 and stripped_content.startswith('<?php'):
                                continue
                            if not pattern.search(content):
                                rel_path = os.path.relpath(file_path, start=directory)
                                no_auth_files.append(rel_path)
                    except Exception as e:
                        yield f"⚠️ 无法读取文件 {file_path}: {str(e)}"
        yield from no_auth_files

    def save_results(self, keywords, regex, directories, results, output_path):
        """保存扫描结果到文件"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"PHP鉴权代码扫描结果 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            f.write("【扫描配置】\n")
            f.write(f"关键词: {keywords}\n")
            f.write(f"正则表达式: {regex}\n")
            f.write(f"扫描目录: {directories}\n\n")
            f.write("【扫描结果】\n")
            if not results:
                f.write("所有PHP文件均包含鉴权代码！\n")
            else:
                f.write(f"共发现 {len(results)} 个文件未检测到鉴权代码:\n\n")
                for dir_path, file_path in results:
                    f.write(f"[{dir_path}] {file_path}\n")
