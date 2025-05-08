import os
import PyInstaller.__main__


def build():
    # 确保图标文件存在
    if not os.path.exists('caigosec.ico'):
        raise FileNotFoundError("图标文件 caigosec.ico 不存在")

    # 打包参数
    params = [
        'start.py',
        '--name=PHPAuthScanner',
        '--onefile',
        '--windowed',  # 不显示控制台窗口
        '--icon=caigosec.ico',
        '--add-data=caigosec.ico;.',  # 包含图标文件
        '--clean',  # 清理临时文件
        '--noconfirm',  # 不确认提示
    ]

    # 执行打包
    PyInstaller.__main__.run(params)


if __name__ == '__main__':
    build()
