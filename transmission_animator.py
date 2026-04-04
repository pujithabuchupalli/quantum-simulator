"""Transmission animation logic for quantum message transmission"""

import random
import tkinter as tk
from tkinter import messagebox
from config import COLORS, TRANSMISSION_DELAY, ERROR_PROBABILITY


class TransmissionAnimator:
    """Handles the animation and logic of message transmission"""
    
    def __init__(self, text_canvas, binary_canvas, status_label, progress_var):
        self.text_canvas = text_canvas
        self.binary_canvas = binary_canvas
        self.status_label = status_label
        self.progress_var = progress_var
        
        # State variables
        self.message = ""
        self.binaries = []
        self.binary_items = []
        self.text_items = []
        self.error_index = None
        self.error_bit_pos = None
        
    def prepare_transmission(self, message):
        """Prepare transmission data and visual elements"""
        self.message = message
        
        # Clear previous transmission
        self.text_canvas.delete("all")
        self.binary_canvas.delete("all")
        self.binaries = []
        self.binary_items = []
        self.text_items = []
        self.error_index = None
        self.error_bit_pos = None
        
        # Convert message to binary
        self.binaries = [format(ord(char), '08b') for char in self.message]
        
        # Create text items
        for i, char in enumerate(self.message):
            x = 50 + i * 30
            item = self.text_canvas.create_text(x, 50, text=char,
                                              fill=COLORS['text_secondary'],
                                              font=('Courier New', 14, 'bold'))
            self.text_items.append(item)
        
        # Create binary items
        for i, binary in enumerate(self.binaries):
            x = 50 + i * 90
            item = self.binary_canvas.create_text(x, 50, text=binary,
                                                fill=COLORS['text_secondary'],
                                                font=('Courier New', 10))
            self.binary_items.append(item)
    
    def start_animation(self, callback):
        """Start the transmission animation"""
        self.status_label.config(text="🚀 Starting quantum transmission...",
                               fg=COLORS['accent_primary'])
        self.animate_transmission(0, callback)
    
    def animate_transmission(self, index, callback):
        """Animate the transmission process"""
        if index >= len(self.message):
            self.status_label.config(text="✅ Transmission complete! Ready for error correction.",
                                   fg=COLORS['success'])
            self.progress_var.set(100)
            if callback:
                callback()
            return
        
        # Update progress
        progress = (index / len(self.message)) * 100
        self.progress_var.set(progress)
        
        # Highlight current character
        if index > 0:
            self.text_canvas.itemconfig(self.text_items[index-1], fill=COLORS['success'])
        self.text_canvas.itemconfig(self.text_items[index], fill=COLORS['accent_primary'])
        
        # Highlight current binary
        if index > 0:
            self.binary_canvas.itemconfig(self.binary_items[index-1], fill=COLORS['success'])
        self.binary_canvas.itemconfig(self.binary_items[index], fill=COLORS['accent_primary'])
        
        # Schedule next frame with error introduction
        def move():
            self._introduce_random_error(index)
            self.text_canvas.after(TRANSMISSION_DELAY, 
                                 lambda: self.animate_transmission(index + 1, callback))
        
        move()
    
    def _introduce_random_error(self, index):
        """Introduce random bit-flip error during transmission"""
        if random.random() < ERROR_PROBABILITY and self.error_index is None:
            self.error_index = index
            self.error_bit_pos = random.randint(0, 7)
            binary_item = self.binary_items[index]
            
            # Flip bit
            corrupted = list(self.binaries[index])
            corrupted[self.error_bit_pos] = ("1" if corrupted[self.error_bit_pos] == "0" else "0")
            corrupted_str = "".join(corrupted)
            
            self.binary_canvas.itemconfig(binary_item, text=corrupted_str, fill=COLORS['error'])
            self.binaries[index] = corrupted_str
            self.status_label.config(
                text=f"⚠️ Quantum error detected! Character {index+1}, bit position {self.error_bit_pos+1}",
                fg=COLORS['error']
            )
    
    def apply_error_correction(self):
        """Apply error correction to detected errors"""
        if self.error_index is None:
            messagebox.showinfo("No Error", "No error detected to correct!")
            return False
        
        # Correct the error
        corrected = list(self.binaries[self.error_index])
        corrected[self.error_bit_pos] = ("1" if corrected[self.error_bit_pos] == "0" else "0")
        corrected_str = "".join(corrected)
        
        self.binary_canvas.itemconfig(self.binary_items[self.error_index],
                                    text=corrected_str,
                                    fill=COLORS['success'])
        self.binaries[self.error_index] = corrected_str
        
        self.status_label.config(text="🔧 Quantum error correction applied successfully! ✨",
                               fg=COLORS['success'])
        return True
    
    def get_corrected_message(self):
        """Get the corrected message after error correction"""
        return "".join([chr(int(b, 2)) for b in self.binaries])
    
    def has_error(self):
        """Check if there's an error detected"""
        return self.error_index is not None
