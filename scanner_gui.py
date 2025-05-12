import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import ImageTk
from scanner_core import PHPAuthScanner


class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.scanner = PHPAuthScanner()
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
                    img = tk.Image.open(icon_path)
                    photo = ImageTk.PhotoImage(img)
                    self.root.iconphoto(False, photo)
                    self.icon_image = photo
                except Exception as e:
                    print(f"加载图标失败: {e}")

    def setup_ui(self):
        """初始化用户界面"""
        self.root.title("菜狗安全PHP鉴权代码扫描器 v1.1")
        self.root.geometry("800x600")

        # 主框架
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill="both", expand=True)

        # 目录选择部分
        dir_frame = ttk.LabelFrame(main_frame, text="扫描目录", padding=10)
        dir_frame.pack(fill=tk.X, pady=5)

        self.dir_listbox = tk.Listbox(dir_frame, height=4)
        self.dir_listbox.pack(fill=tk.X, expand=True)

        btn_frame = ttk.Frame(dir_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="添加目录", command=self.add_directory).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="添加ThinkPHP项目", command=self.detect_thinkphp_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="自定义工作目录", command=self.extract_controller_dirs).pack(side=tk.LEFT,
                                                                                                    padx=5)
        ttk.Button(btn_frame, text="移除目录", command=self.remove_directory).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="清空目录", command=self.clear_directories).pack(side=tk.LEFT, padx=5)

        # 关键词输入
        keyword_frame = ttk.LabelFrame(main_frame, text="鉴权关键词", padding=10)
        keyword_frame.pack(fill=tk.X, pady=5)
        self.keyword_entry = ttk.Entry(keyword_frame)
        self.keyword_entry.pack(fill=tk.X)
        self.keyword_entry.insert(0, "session auth login AdminBase AuthBase")

        # 正则表达式显示
        regex_frame = ttk.LabelFrame(main_frame, text="生成的正则表达式", padding=10)
        regex_frame.pack(fill=tk.X, pady=5)
        self.regex_display = scrolledtext.ScrolledText(regex_frame, height=4, wrap=tk.WORD)
        self.regex_display.pack(fill=tk.BOTH, expand=True)
        self.regex_display.config(state=tk.DISABLED)

        # 操作按钮
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="开始扫描", command=self.start_scan).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="保存结果", command=self.save_results).pack(side=tk.LEFT, padx=5)

        # 结果展示
        result_frame = ttk.LabelFrame(main_frame, text="扫描结果", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

    def add_directory(self):
        """添加普通目录"""
        directory = filedialog.askdirectory()
        if directory:
            self.dir_listbox.insert(tk.END, directory)

    def detect_thinkphp_project(self):
        """检测ThinkPHP项目并提取app/application中的controller目录"""
        project_dir = filedialog.askdirectory(title="选择ThinkPHP项目根目录")
        if not project_dir:
            return

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
        for dir_path in controller_dirs:
            if dir_path not in self.dir_listbox.get(0, tk.END):
                self.dir_listbox.insert(tk.END, dir_path)
                added += 1

        messagebox.showinfo("完成", f"已添加 {added} 个Controller目录")

    def extract_controller_dirs(self, base_dir=None):
        """从指定目录提取Controller目录"""
        if base_dir is None:
            base_dir = filedialog.askdirectory(title="选择包含Controller的目录")
            if not base_dir:
                return

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
        for dir_path in controller_dirs:
            if dir_path not in self.dir_listbox.get(0, tk.END):
                self.dir_listbox.insert(tk.END, dir_path)
                added += 1

        messagebox.showinfo("完成", f"已添加 {added} 个Controller目录")

    def remove_directory(self):
        if selection := self.dir_listbox.curselection():
            self.dir_listbox.delete(selection)

    def clear_directories(self):
        self.dir_listbox.delete(0, tk.END)

    def start_scan(self):
        """执行扫描操作"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

        directories = self.dir_listbox.get(0, tk.END)
        if not directories:
            messagebox.showerror("错误", "请至少添加一个扫描目录！")
            return

        keywords = self.keyword_entry.get().strip().split()
        if not keywords:
            messagebox.showerror("错误", "请输入至少一个关键词！")
            return

        pattern = self.scanner.generate_regex(keywords)

        # 更新正则表达式显示
        self.regex_display.config(state=tk.NORMAL)
        self.regex_display.delete(1.0, tk.END)
        self.regex_display.insert(tk.END, pattern.pattern)
        self.regex_display.config(state=tk.DISABLED)

        # 执行扫描
        total_results = []
        for directory in directories:
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
                        self.log_result(f"- {file_path}")

        self.scanner.scan_results = total_results

        if total_results:
            self.log_result("\n📊 扫描完成，发现以下未鉴权文件:")
            for dir_path, file_path in total_results:
                self.log_result(f"- [{dir_path}] {file_path}")
        else:
            self.log_result("\n🎉 扫描完成，所有目录中的PHP文件均包含鉴权代码！")

    def save_results(self):
        """保存扫描结果"""
        if not self.scanner.scan_results:
            messagebox.showwarning("警告", "没有可保存的扫描结果！")
            return

        default_path = os.path.join(os.getcwd(), "scan_results.txt")
        try:
            self.scanner.save_results(
                keywords=self.keyword_entry.get(),
                regex=self.regex_display.get("1.0", tk.END).strip(),
                directories=list(self.dir_listbox.get(0, tk.END)),
                results=self.scanner.scan_results,
                output_path=default_path
            )
            messagebox.showinfo("保存成功", f"扫描结果已保存到:\n{default_path}")
        except Exception as e:
            messagebox.showerror("保存失败", f"保存结果时出错:\n{str(e)}")

    def log_result(self, message):
        """在结果区域记录消息"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, message + "\n")
        self.result_text.config(state=tk.DISABLED)
        self.result_text.see(tk.END)