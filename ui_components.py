"""Custom UI components with modern styling"""

import tkinter as tk
from tkinter import ttk
from config import COLORS


class ModernFrame(tk.Frame):
    """Custom frame with rounded corners effect"""
    def __init__(self, parent, bg_color=COLORS['bg_secondary'], **kwargs):
        super().__init__(parent, bg=bg_color, relief='flat', bd=2, **kwargs)


class ModernButton(tk.Button):
    """Custom button with modern styling"""
    def __init__(self, parent, **kwargs):
        default_style = {
            'bg': COLORS['accent_primary'],
            'fg': COLORS['bg_primary'],
            'activebackground': COLORS['accent_secondary'],
            'activeforeground': COLORS['text_primary'],
            'relief': 'flat',
            'bd': 0,
            'font': ('Segoe UI', 10, 'bold'),
            'cursor': 'hand2',
            'padx': 20,
            'pady': 8
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)


class ModernEntry(tk.Entry):
    """Custom entry with modern styling"""
    def __init__(self, parent, **kwargs):
        default_style = {
            'bg': COLORS['bg_tertiary'],
            'fg': COLORS['text_primary'],
            'insertbackground': COLORS['accent_primary'],
            'relief': 'flat',
            'bd': 2,
            'font': ('Segoe UI', 11),
            'selectbackground': COLORS['accent_primary'],
            'selectforeground': COLORS['bg_primary']
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)


class ModernLabel(tk.Label):
    """Custom label with modern styling"""
    def __init__(self, parent, **kwargs):
        default_style = {
            'bg': COLORS['bg_primary'],
            'fg': COLORS['text_primary'],
            'font': ('Segoe UI', 10)
        }
        default_style.update(kwargs)
        super().__init__(parent, **default_style)


def setup_progressbar_style():
    """Configure ttk progressbar style"""
    style = ttk.Style()
    style.theme_use('clam')
    
    # Configure progress bar
    style.configure('Custom.Horizontal.TProgressbar',
                   background=COLORS['accent_primary'],
                   troughcolor=COLORS['bg_tertiary'],
                   borderwidth=0,
                   lightcolor=COLORS['accent_primary'],
                   darkcolor=COLORS['accent_primary'])
