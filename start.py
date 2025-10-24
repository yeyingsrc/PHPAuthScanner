import customtkinter as ctk
from scanner_gui import ScannerGUI

def main():
    # 设置应用主题
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = ScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
