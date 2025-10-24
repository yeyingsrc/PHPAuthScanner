import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from scanner_core import PHPAuthScanner

# 设置customtkinter主题和外观
ctk.set_appearance_mode("System")  # 可选: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # 可选: "blue", "green", "dark-blue"


class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.scanner = PHPAuthScanner()
        self.icon_image = None  # 保持对图标图片的引用
        self.setup_ui()
        self.setup_icon()

    def setup_icon(self):
        """设置应用图标"""
        icon_path = os.path.join(os.path.dirname(__file__), "caigosec.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except:
                try:
                    img = Image.open(icon_path)
                    photo = ImageTk.PhotoImage(img)
                    self.root.iconphoto(False, photo)
                    self.icon_image = photo
                except Exception as e:
                    print(f"加载图标失败: {e}")
    
    def toggle_theme(self):
        """切换应用主题（浅色/暗色）"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "Dark" if current_mode == "Light" else "Light"
        ctk.set_appearance_mode(new_mode)
        self.theme_switch.configure(text="暗色模式" if new_mode == "Light" else "亮色模式")

    def setup_ui(self):
        """初始化现代化用户界面"""
        self.root.title("菜狗安全PHP鉴权代码扫描器 v1.2")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)  # 设置最小窗口尺寸
        
        # 创建主框架
        main_frame = ctk.CTkFrame(self.root, corner_radius=10, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # 创建顶部工具栏
        toolbar_frame = ctk.CTkFrame(main_frame, corner_radius=8, height=40)
        toolbar_frame.pack(fill="x", pady=(0, 10))
        
        # 主题切换按钮
        self.theme_switch = ctk.CTkSwitch(
            toolbar_frame, 
            text="暗色模式", 
            command=self.toggle_theme,
            progress_color="#3b8ed0"
        )
        self.theme_switch.pack(side="right", padx=10, pady=5)
        
        # 标题标签
        title_label = ctk.CTkLabel(
            toolbar_frame, 
            text="PHP鉴权代码扫描器 v1.2", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(side="left", padx=10, pady=5)

        # 左侧配置区域
        config_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        config_frame.pack(fill="x", pady=(0, 10))
        
        # 目录选择部分
        dir_frame = ctk.CTkFrame(config_frame, corner_radius=8)
        dir_frame.pack(fill="x", pady=(10, 5), padx=10)
        
        # 目录选择标题
        dir_label = ctk.CTkLabel(
            dir_frame, 
            text="扫描目录", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        dir_label.pack(anchor="w", pady=(5, 5), padx=5)
        
        # 目录列表
        self.dir_listbox = ctk.CTkTextbox(
            dir_frame, 
            height=100, 
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.dir_listbox.pack(fill="x", expand=True, pady=(0, 10), padx=5)
        self.dir_listbox.insert("0.0", "")  # 初始化为空
        
        # 目录操作按钮
        dir_btn_frame = ctk.CTkFrame(dir_frame, fg_color="transparent")
        dir_btn_frame.pack(fill="x", pady=(0, 5), padx=5)
        
        self.add_dir_btn = ctk.CTkButton(
            dir_btn_frame, 
            text="添加目录", 
            command=self.add_directory,
            width=120,
            corner_radius=6,
            fg_color="#3b8ed0",
            hover_color="#2c7ed6"
        )
        self.add_dir_btn.pack(side="left", padx=3, pady=5)
        
        self.add_thinkphp_btn = ctk.CTkButton(
            dir_btn_frame, 
            text="添加ThinkPHP项目", 
            command=self.detect_thinkphp_project,
            width=120,
            corner_radius=6
        )
        self.add_thinkphp_btn.pack(side="left", padx=3, pady=5)
        
        self.custom_dir_btn = ctk.CTkButton(
            dir_btn_frame, 
            text="自定义工作目录", 
            command=self.extract_controller_dirs,
            width=120,
            corner_radius=6
        )
        self.custom_dir_btn.pack(side="left", padx=3, pady=5)
        
        self.remove_dir_btn = ctk.CTkButton(
            dir_btn_frame, 
            text="移除目录", 
            command=self.remove_directory,
            width=100,
            corner_radius=6,
            fg_color="#d32f2f",
            hover_color="#b71c1c"
        )
        self.remove_dir_btn.pack(side="left", padx=3, pady=5)
        
        self.clear_dirs_btn = ctk.CTkButton(
            dir_btn_frame, 
            text="清空目录", 
            command=self.clear_directories,
            width=100,
            corner_radius=6,
            fg_color="#ff9800",
            hover_color="#f57c00"
        )
        self.clear_dirs_btn.pack(side="left", padx=3, pady=5)

        # 关键词输入部分
        keyword_frame = ctk.CTkFrame(config_frame, corner_radius=8)
        keyword_frame.pack(fill="x", pady=5, padx=10)
        
        keyword_label = ctk.CTkLabel(
            keyword_frame, 
            text="鉴权关键词", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        keyword_label.pack(anchor="w", pady=(5, 5), padx=5)
        
        self.keyword_entry = ctk.CTkEntry(
            keyword_frame, 
            placeholder_text="输入鉴权关键词，用空格分隔",
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.keyword_entry.pack(fill="x", pady=(0, 10), padx=5)
        self.keyword_entry.insert(0, "session auth login AdminBase AuthBase")

        # 正则表达式显示部分
        regex_frame = ctk.CTkFrame(config_frame, corner_radius=8)
        regex_frame.pack(fill="x", pady=5, padx=10)
        
        regex_label = ctk.CTkLabel(
            regex_frame, 
            text="生成的正则表达式", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        regex_label.pack(anchor="w", pady=(5, 5), padx=5)
        
        self.regex_display = ctk.CTkTextbox(
            regex_frame, 
            height=80, 
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=10),
            state="disabled"
        )
        self.regex_display.pack(fill="x", expand=True, pady=(0, 10), padx=5)

        # 操作按钮部分
        action_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 10))
        
        self.scan_btn = ctk.CTkButton(
            action_frame, 
            text="开始扫描", 
            command=self.start_scan,
            width=200,
            height=50,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4caf50",
            hover_color="#388e3c"
        )
        self.scan_btn.pack(side="left", padx=10, pady=5)
        
        self.save_btn = ctk.CTkButton(
            action_frame, 
            text="保存结果", 
            command=self.save_results,
            width=200,
            height=50,
            corner_radius=8,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1976d2",
            hover_color="#1565c0"
        )
        self.save_btn.pack(side="left", padx=10, pady=5)

        # 结果展示部分
        result_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        result_frame.pack(fill="both", expand=True, pady=5)
        
        result_label = ctk.CTkLabel(
            result_frame, 
            text="扫描结果", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        result_label.pack(anchor="w", pady=(5, 5), padx=5)
        
        self.result_text = ctk.CTkTextbox(
            result_frame, 
            corner_radius=6,
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled"
        )
        self.result_text.pack(fill="both", expand=True, pady=(0, 10), padx=5)
        
        # 设置进度条（初始隐藏）
        self.progress_frame = ctk.CTkFrame(main_frame, corner_radius=10, fg_color="transparent")
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame, 
            width=300, 
            height=10,
            progress_color="#3b8ed0"
        )
        self.progress_label = ctk.CTkLabel(
            self.progress_frame, 
            text="准备扫描...", 
            font=ctk.CTkFont(size=12)
        )
        self.progress_bar.set(0)


    def add_directory(self):
        """添加普通目录"""
        directory = filedialog.askdirectory()
        if directory:
            # 获取当前文本内容
            current_text = self.dir_listbox.get("0.0", "end").strip()
            # 如果已有内容，添加换行符
            if current_text:
                self.dir_listbox.insert("end", "\n")
            self.dir_listbox.insert("end", directory)
            # 滚动到底部
            self.dir_listbox.see("end")

    def detect_thinkphp_project(self):
        """检测ThinkPHP项目并提取app/application中的controller目录"""
        project_dir = filedialog.askdirectory(title="选择ThinkPHP项目根目录")
        if not project_dir:
            return

        # 显示加载动画或进度
        self.log_result(f"🔍 正在分析ThinkPHP项目结构: {project_dir}")

        # 标准ThinkPHP目录结构
        possible_dirs = [
            os.path.join(project_dir, "app"),  # ThinkPHP 5.x/6.x
            os.path.join(project_dir, "application")  # ThinkPHP 3.2
        ]

        # 查找存在的目录
        found_dirs = [d for d in possible_dirs if os.path.exists(d)]

        if not found_dirs:
            messagebox.showwarning(
                "未找到标准目录",
                "未找到app或application目录，请使用'自定义工作目录'功能手动指定"
            )
            return

        # 从找到的目录中提取controller目录
        controller_dirs = []
        for base_dir in found_dirs:
            # 查找base_dir下的所有controller目录
            for root, dirs, _ in os.walk(base_dir):
                if os.path.basename(root).lower() == "controller":
                    # 检查目录中是否有PHP文件
                    if any(f.endswith('.php') for f in os.listdir(root)):
                        controller_dirs.append(root)

        if not controller_dirs:
            messagebox.showwarning(
                "未找到Controller目录",
                f"在{project_dir}的app/application目录中未找到有效的Controller目录"
            )
            return

        # 添加找到的Controller目录
        added = 0
        current_dirs = set(self.dir_listbox.get("0.0", "end").strip().split("\n"))
        
        # 获取当前文本内容
        current_text = self.dir_listbox.get("0.0", "end").strip()
        need_newline = bool(current_text)
        
        for dir_path in controller_dirs:
            if dir_path not in current_dirs:
                if need_newline:
                    self.dir_listbox.insert("end", "\n")
                    need_newline = False
                self.dir_listbox.insert("end", dir_path)
                need_newline = True
                added += 1

        # 滚动到底部
        self.dir_listbox.see("end")
        
        # 显示成功消息
        messagebox.showinfo("完成", f"已添加 {added} 个Controller目录")
        self.log_result(f"✅ 成功添加 {added} 个ThinkPHP Controller目录")

    def extract_controller_dirs(self, base_dir=None):
        """从指定目录提取Controller目录"""
        if base_dir is None:
            base_dir = filedialog.askdirectory(title="选择包含Controller的目录")
            if not base_dir:
                return

        # 显示正在扫描
        self.log_result(f"🔍 正在扫描目录结构: {base_dir}")

        # 查找所有controller目录（不区分大小写）
        controller_dirs = []
        for root, dirs, _ in os.walk(base_dir):
            if os.path.basename(root).lower() == "controller":
                # 检查目录中是否有PHP文件
                if any(f.endswith('.php') for f in os.listdir(root)):
                    controller_dirs.append(root)

        if not controller_dirs:
            messagebox.showwarning("警告", f"在 {base_dir} 中未找到有效的Controller目录")
            return

        # 添加找到的Controller目录
        added = 0
        current_dirs = set(self.dir_listbox.get("0.0", "end").strip().split("\n"))
        
        # 获取当前文本内容
        current_text = self.dir_listbox.get("0.0", "end").strip()
        need_newline = bool(current_text)
        
        for dir_path in controller_dirs:
            if dir_path not in current_dirs:
                if need_newline:
                    self.dir_listbox.insert("end", "\n")
                    need_newline = False
                self.dir_listbox.insert("end", dir_path)
                need_newline = True
                added += 1

        # 滚动到底部
        self.dir_listbox.see("end")
        
        messagebox.showinfo("完成", f"已添加 {added} 个Controller目录")
        self.log_result(f"✅ 成功添加 {added} 个Controller目录")

    def remove_directory(self):
        """移除选中的目录"""
        # 获取选中的文本
        try:
            selected_text = self.dir_listbox.get("sel.first", "sel.last")
            # 获取全部文本
            all_text = self.dir_listbox.get("0.0", "end")
            # 替换选中的文本为空
            new_text = all_text.replace(selected_text, "")
            # 清理多余的空行
            new_text = "\n".join([line for line in new_text.split("\n") if line.strip()])
            # 更新文本框
            self.dir_listbox.delete("0.0", "end")
            self.dir_listbox.insert("0.0", new_text)
            self.log_result(f"🗑️  已移除选中的目录")
        except:
            # 如果没有选中文本，显示提示
            messagebox.showinfo("提示", "请先选中要移除的目录")

    def clear_directories(self):
        """清空所有目录"""
        if messagebox.askyesno("确认", "确定要清空所有目录吗？"):
            self.dir_listbox.delete("0.0", "end")
            self.log_result("🗑️  已清空所有目录")

    def start_scan(self):
        """执行扫描操作，添加进度显示"""
        # 清空结果区域
        self.result_text.configure(state="normal")
        self.result_text.delete("0.0", "end")
        self.result_text.configure(state="disabled")

        # 获取目录列表
        dirs_text = self.dir_listbox.get("0.0", "end").strip()
        directories = [d.strip() for d in dirs_text.split("\n") if d.strip()]
        
        if not directories:
            messagebox.showerror("错误", "请至少添加一个扫描目录！")
            return

        keywords = self.keyword_entry.get().strip().split()
        if not keywords:
            messagebox.showerror("错误", "请输入至少一个关键词！")
            return

        # 生成正则表达式
        pattern = self.scanner.generate_regex(keywords)

        # 更新正则表达式显示
        self.regex_display.configure(state="normal")
        self.regex_display.delete("0.0", "end")
        self.regex_display.insert("0.0", pattern.pattern)
        self.regex_display.configure(state="disabled")
        
        # 显示进度条
        self.progress_frame.pack(fill="x", pady=(10, 5))
        self.progress_bar.pack(side="left", padx=10, pady=5)
        self.progress_label.pack(side="left", padx=10, pady=5)
        
        # 禁用扫描按钮
        self.scan_btn.configure(state="disabled")
        
        # 执行扫描（使用after来避免UI卡顿）
        self.root.after(100, self._execute_scan, directories, pattern)
    
    def _execute_scan(self, directories, pattern):
        """实际执行扫描操作的方法"""
        total_results = []
        total_dirs = len(directories)
        
        for i, directory in enumerate(directories):
            # 更新进度
            progress = (i + 1) / total_dirs
            self.progress_bar.set(progress)
            self.progress_label.configure(text=f"正在扫描 ({i+1}/{total_dirs}): {os.path.basename(directory)}")
            self.root.update_idletasks()
            
            self.log_result(f"\n🔎 开始扫描目录: {directory}")
            results = list(self.scanner.scan_directory(directory, pattern))
            total_results.extend([(directory, r) for r in results if not r.startswith("⚠️")])

            if not results:
                self.log_result("✅ 所有 PHP 文件均包含鉴权代码！")
            else:
                error_msgs = [r for r in results if r.startswith("⚠️")]
                valid_results = [r for r in results if not r.startswith("⚠️")]

                for msg in error_msgs:
                    self.log_result(msg)

                if valid_results:
                    self.log_result(f"❌ 共发现 {len(valid_results)} 个文件未检测到鉴权代码:")
                    for file_path in valid_results:
                        # 确保只显示文件路径，不包含目录前缀
                        self.log_result(f"- {file_path}")
        
        # 扫描完成后更新UI
        self.progress_label.configure(text="扫描完成！")
        self.root.update_idletasks()
        
        self.scanner.scan_results = total_results

        if total_results:
            self.log_result("\n📊 扫描完成，发现以下未鉴权文件:")
            for dir_path, file_path in total_results:
                # 只显示文件路径，不包含目录前缀
                self.log_result(f"- {file_path}")
        else:
            self.log_result("\n🎉 扫描完成，所有目录中的PHP文件均包含鉴权代码！")
        
        # 恢复按钮状态
        self.scan_btn.configure(state="normal")

    def save_results(self):
        """保存扫描结果"""
        if not self.scanner.scan_results:
            messagebox.showwarning("警告", "没有可保存的扫描结果！")
            return

        # 使用文件对话框让用户选择保存位置
        default_path = os.path.join(os.getcwd(), "scan_results.txt")
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile="scan_results.txt",
            initialdir=os.getcwd()
        )
        
        if not file_path:
            return  # 用户取消了保存
        
        try:
            # 获取目录列表
            dirs_text = self.dir_listbox.get("0.0", "end").strip()
            directories = [d.strip() for d in dirs_text.split("\n") if d.strip()]
            
            self.scanner.save_results(
                keywords=self.keyword_entry.get(),
                regex=self.regex_display.get("0.0", "end").strip(),
                directories=directories,
                results=self.scanner.scan_results,
                output_path=file_path
            )
            messagebox.showinfo("保存成功", f"扫描结果已保存到:\n{file_path}")
            self.log_result(f"💾 扫描结果已保存到: {file_path}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存结果时出错:\n{str(e)}")
            self.log_result(f"❌ 保存结果失败: {str(e)}")

    def log_result(self, message):
        """在结果区域记录消息"""
        self.result_text.configure(state="normal")
        self.result_text.insert("end", message + "\n")
        self.result_text.configure(state="disabled")
        self.result_text.see("end")