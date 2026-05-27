import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from Backend.database import ChefDB
from Frontend.app_chef import AppChef

if __name__ == '__main__':
    ChefDB.inicializar()
    root = tk.Tk()
    app = AppChef(root)
    root.mainloop()