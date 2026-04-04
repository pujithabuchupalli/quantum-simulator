"""Main application class for the Quantum Error Correction Simulator"""

import tkinter as tk
from tkinter import ttk, messagebox
from config import COLORS, WINDOW_TITLE, WINDOW_GEOMETRY, WINDOW_MIN_SIZE
from ui_components import (
    ModernFrame, ModernButton, ModernEntry, ModernLabel, 
    setup_progressbar_style
)
from transmission_animator import TransmissionAnimator
from circuit_visualizer import CircuitVisualizer


class QuantumTransmissionSimulator:
    """Main application class for quantum transmission simulation"""
    
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.setup_styles()
        self.setup_variables()
        self.create_widgets()
    
    def setup_window(self):
        """Configure the main window"""
        self.master.title(WINDOW_TITLE)
        self.master.configure(bg=COLORS['bg_primary'])
        self.master.geometry(WINDOW_GEOMETRY)
        self.master.minsize(*WINDOW_MIN_SIZE)
       
        # Center the window
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configure ttk styles"""
        setup_progressbar_style()
    
    def setup_variables(self):
        """Initialize variables"""
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        
        # Initialize animator and visualizer
        self.animator = None
        self.visualizer = None
    
    def create_scrollable_frame(self):
        """Create a scrollable frame for the main content"""
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(self.master, bg=COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ModernFrame(self.canvas, bg_color=COLORS['bg_primary'])
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack the canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def create_widgets(self):
        """Create and layout all widgets"""
        # Create scrollable frame
        self.create_scrollable_frame()
        
        # Header
        self.create_header()
       
        # Main content area
        main_container = ModernFrame(self.scrollable_frame, bg_color=COLORS['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
       
        # Communication section
        self.create_communication_section(main_container)
       
        # Transmission visualization
        self.create_transmission_section(main_container)
       
        # Control panel
        self.create_control_panel(main_container)
       
        # Status bar (create before animator needs it)
        self.create_status_bar()
        
        # Initialize animator after all widgets are created
        self.animator = TransmissionAnimator(
            self.text_canvas, self.binary_canvas, 
            self.status_label, self.progress_var
        )
    
    def create_header(self):
        """Create the header section"""
        header_frame = ModernFrame(self.scrollable_frame, bg_color=COLORS['bg_secondary'])
        header_frame.pack(fill='x', padx=20, pady=(20, 0))
       
        title_label = ModernLabel(header_frame,
                                text="Quantum Error Correction Simulator",
                                font=('Segoe UI', 20, 'bold'),
                                fg=COLORS['accent_primary'],
                                bg=COLORS['bg_secondary'])
        title_label.pack(pady=20)
       
        subtitle_label = ModernLabel(header_frame,
                                   text="Simulate quantum bit-flip error correction with visual transmission",
                                   font=('Segoe UI', 12),
                                   fg=COLORS['text_secondary'],
                                   bg=COLORS['bg_secondary'])
        subtitle_label.pack(pady=(0, 20))
    
    def create_communication_section(self, parent):
        """Create the user communication section"""
        comm_frame = ModernFrame(parent, bg_color=COLORS['bg_secondary'])
        comm_frame.pack(fill='x', pady=10)
       
        # Title
        comm_title = ModernLabel(comm_frame,
                               text="📡 Quantum Communication Channel",
                               font=('Segoe UI', 14, 'bold'),
                               fg=COLORS['accent_primary'],
                               bg=COLORS['bg_secondary'])
        comm_title.pack(pady=(15, 10))
       
        # Users container
        users_container = tk.Frame(comm_frame, bg=COLORS['bg_secondary'])
        users_container.pack(fill='x', padx=30, pady=15)
       
        # Sender (left side)
        sender_frame = ModernFrame(users_container, bg_color=COLORS['bg_tertiary'])
        sender_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
       
        sender_label = ModernLabel(sender_frame,
                                 text="👤 User 1 (Sender)",
                                 font=('Segoe UI', 12, 'bold'),
                                 fg=COLORS['success'],
                                 bg=COLORS['bg_tertiary'])
        sender_label.pack(pady=(15, 10))
       
        input_frame = tk.Frame(sender_frame, bg=COLORS['bg_tertiary'])
        input_frame.pack(fill='x', padx=20)
       
        self.input_entry = ModernEntry(input_frame, textvariable=self.input_var, width=35)
        self.input_entry.pack(fill='x', pady=5)
        self.input_entry.bind('<Return>', lambda e: self.start_transmission())
       
        send_btn = ModernButton(sender_frame,
                              text="🚀 Send Message",
                              command=self.start_transmission)
        send_btn.pack(pady=15)
       
        # Arrow in middle
        arrow_frame = tk.Frame(users_container, bg=COLORS['bg_secondary'], width=100)
        arrow_frame.pack(side='left')
        arrow_frame.pack_propagate(False)
       
        # Progress bar for transmission
        from tkinter import ttk
        self.progress_bar = ttk.Progressbar(arrow_frame,
                                          variable=self.progress_var,
                                          maximum=100,
                                          style='Custom.Horizontal.TProgressbar',
                                          orient='horizontal',
                                          length=80)
        self.progress_bar.pack(expand=True)
       
        arrow_label = ModernLabel(arrow_frame,
                                text="→",
                                font=('Arial', 20, 'bold'),
                                fg=COLORS['accent_primary'],
                                bg=COLORS['bg_secondary'])
        arrow_label.pack()
       
        # Receiver (right side)
        receiver_frame = ModernFrame(users_container, bg_color=COLORS['bg_tertiary'])
        receiver_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
       
        receiver_label = ModernLabel(receiver_frame,
                                   text="👤 User 2 (Receiver)",
                                   font=('Segoe UI', 12, 'bold'),
                                   fg=COLORS['warning'],
                                   bg=COLORS['bg_tertiary'])
        receiver_label.pack(pady=(15, 10))
       
        output_frame = ModernFrame(receiver_frame, bg_color=COLORS['bg_primary'])
        output_frame.pack(fill='x', padx=20, pady=10)
       
        self.output_display = ModernLabel(output_frame,
                                        textvariable=self.output_var,
                                        font=('Segoe UI', 11),
                                        width=35,
                                        height=2,
                                        anchor='center',
                                        bg=COLORS['bg_primary'],
                                        fg=COLORS['text_primary'],
                                        relief='sunken',
                                        bd=1)
        self.output_display.pack(fill='x', pady=10)
    
    def create_transmission_section(self, parent):
        """Create the transmission visualization section"""
        trans_frame = ModernFrame(parent, bg_color=COLORS['bg_secondary'])
        trans_frame.pack(fill='both', expand=True, pady=10)
       
        # Text transmission
        text_label = ModernLabel(trans_frame,
                               text="📝 Text Transmission Visualization",
                               font=('Segoe UI', 12, 'bold'),
                               fg=COLORS['accent_primary'],
                               bg=COLORS['bg_secondary'])
        text_label.pack(pady=(15, 5))
       
        self.text_canvas = tk.Canvas(trans_frame,
                                   width=800,
                                   height=100,
                                   bg=COLORS['bg_primary'],
                                   highlightthickness=1,
                                   highlightcolor=COLORS['bg_tertiary'])
        self.text_canvas.pack(pady=5)
       
        # Binary transmission
        binary_label = ModernLabel(trans_frame,
                                 text="🔢 Binary Transmission with Error Correction",
                                 font=('Segoe UI', 12, 'bold'),
                                 fg=COLORS['accent_primary'],
                                 bg=COLORS['bg_secondary'])
        binary_label.pack(pady=(15, 5))
       
        self.binary_canvas = tk.Canvas(trans_frame,
                                     width=800,
                                     height=150,
                                     bg=COLORS['bg_primary'],
                                     highlightthickness=1,
                                     highlightcolor=COLORS['bg_tertiary'])
        self.binary_canvas.pack(pady=(5, 15))
    
    def create_control_panel(self, parent):
        """Create the control panel"""
        control_frame = ModernFrame(parent, bg_color=COLORS['bg_secondary'])
        control_frame.pack(fill='x', pady=10)
       
        control_title = ModernLabel(control_frame,
                                  text="🔧 Quantum Circuit Analysis",
                                  font=('Segoe UI', 12, 'bold'),
                                  fg=COLORS['accent_primary'],
                                  bg=COLORS['bg_secondary'])
        control_title.pack(pady=(15, 10))
       
        button_frame = tk.Frame(control_frame, bg=COLORS['bg_secondary'])
        button_frame.pack(pady=15)
       
        circuit_btn = ModernButton(button_frame,
                                 text="🔬 Show Quantum Circuits",
                                 command=self.show_backend_circuit,
                                 bg=COLORS['accent_secondary'])
        circuit_btn.pack(side='left', padx=10)
       
        fidelity_btn = ModernButton(button_frame,
                                  text="📊 Show Performance Metrics",
                                  command=self.show_fidelity_plot,
                                  bg=COLORS['warning'])
        fidelity_btn.pack(side='left', padx=10)
       
        correct_btn = ModernButton(button_frame,
                                 text="🔧 Apply Error Correction",
                                 command=self.correct_error,
                                 bg=COLORS['success'])
        correct_btn.pack(side='left', padx=10)
        
        # Initialize visualizer
        self.visualizer = CircuitVisualizer(self.master)
    
    def create_status_bar(self):
        """Create the status bar"""
        status_frame = ModernFrame(self.scrollable_frame, bg_color=COLORS['bg_tertiary'])
        status_frame.pack(fill='x', padx=20, pady=(0, 20))
       
        self.status_label = ModernLabel(status_frame,
                                      text="💡 Ready to simulate quantum transmission",
                                      font=('Segoe UI', 10),
                                      fg=COLORS['text_secondary'],
                                      bg=COLORS['bg_tertiary'])
        self.status_label.pack(pady=8)
    
    def start_transmission(self):
        """Start the transmission animation"""
        message = self.input_var.get().strip()
        if not message:
            messagebox.showwarning("Input Required", "Please enter a message to transmit!")
            return
        
        # Clear output
        self.output_var.set("")
        
        # Prepare and start animation
        self.animator.prepare_transmission(message)
        self.animator.start_animation(self._on_transmission_complete)
    
    def _on_transmission_complete(self):
        """Callback when transmission animation completes"""
        pass
    
    def correct_error(self):
        """Apply error correction"""
        if self.animator.apply_error_correction():
            corrected_message = self.animator.get_corrected_message()
            self.output_var.set(corrected_message)
    
    def show_backend_circuit(self):
        """Show the quantum circuits in a popup"""
        message = self.input_var.get().strip()
        if not message:
            messagebox.showwarning("No Data", "Please send a message first!")
            return
        
        self.visualizer.show_quantum_circuits(message)
    
    def show_fidelity_plot(self):
        """Show fidelity and accuracy plots"""
        self.visualizer.show_performance_metrics()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = QuantumTransmissionSimulator(root)
   
    # Add some nice touches
    try:
        # Set window icon if available
        root.iconname("Quantum Simulator")
        # Make window resizable but with constraints
        root.resizable(True, True)
    except:
        pass
   
    root.mainloop()


if __name__ == "__main__":
    main()
