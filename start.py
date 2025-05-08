import tkinter as tk
from scanner_gui import ScannerGUI

def main():
    root = tk.Tk()
    app = ScannerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
