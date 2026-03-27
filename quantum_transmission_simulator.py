import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Enhanced Color Scheme
COLORS = {
    'bg_primary': '#0d1421',
    'bg_secondary': '#1a2332',
    'bg_tertiary': '#2d3748',
    'accent_primary': '#4fd1c7',
    'accent_secondary': '#38b2ac',
    'text_primary': '#ffffff',
    'text_secondary': '#a0aec0',
    'success': '#48bb78',
    'error': '#f56565',
    'warning': '#ed8936'
}

# --- Backend: Bit-Flip QEC ---
def run_bitflip_qec(logical_state="0", error_qubit=None, shots=1024):
    # Encoding circuit
    qc_encode = QuantumCircuit(3, 1)
    if logical_state == "1":
        qc_encode.x(0)
    qc_encode.cx(0, 1)
    qc_encode.cx(0, 2)

    # Error circuit
    qc_error = qc_encode.copy()
    error_info = "No error introduced"
    if error_qubit in [0, 1, 2]:
        qc_error.x(error_qubit)
        error_info = f"Bit-flip error in qubit {error_qubit}"

    # Full correction circuit
    qc_full = qc_error.copy()
    qc_full.cx(0, 1)
    qc_full.cx(0, 2)
    qc_full.ccx(1, 2, 0)
    qc_full.measure(0, 0)

    # Simulation
    simulator = AerSimulator()
    compiled = transpile(qc_full, simulator)
    result = simulator.run(compiled, shots=shots).result()
    counts = result.get_counts()
    fidelity = counts.get("0", 0) / shots if logical_state == "0" else counts.get("1", 0) / shots

    return qc_encode, qc_error, qc_full, counts, fidelity, error_info


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


class UserTransmissionSimulator:
    def __init__(self, master):
        self.master = master
        self.setup_window()
        self.setup_styles()
        self.setup_variables()
        self.create_widgets()

    def setup_window(self):
        """Configure the main window"""
        self.master.title("🔬 Quantum Error Correction Simulator")
        self.master.configure(bg=COLORS['bg_primary'])
        self.master.geometry("1000x850")
        self.master.minsize(900, 750)
       
        # Center the window
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f'{width}x{height}+{x}+{y}')

    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
       
        # Configure progress bar
        style.configure('Custom.Horizontal.TProgressbar',
                       background=COLORS['accent_primary'],
                       troughcolor=COLORS['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=COLORS['accent_primary'],
                       darkcolor=COLORS['accent_primary'])

    def setup_variables(self):
        """Initialize variables"""
        self.message = ""
        self.binaries = []
        self.binary_items = []
        self.text_items = []
        self.error_index = None
        self.error_bit_pos = None

    def create_widgets(self):
        """Create and layout all widgets"""
        # Header
        self.create_header()
       
        # Main content area
        main_container = ModernFrame(self.master, bg_color=COLORS['bg_primary'])
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
       
        # Communication section
        self.create_communication_section(main_container)
       
        # Transmission visualization
        self.create_transmission_section(main_container)
       
        # Control panel
        self.create_control_panel(main_container)
       
        # Status bar
        self.create_status_bar()

    def create_header(self):
        """Create the header section"""
        header_frame = ModernFrame(self.master, bg_color=COLORS['bg_secondary'])
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
       
        self.input_var = tk.StringVar()
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
        self.progress_var = tk.DoubleVar()
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
       
        self.output_var = tk.StringVar()
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

    def create_status_bar(self):
        """Create the status bar"""
        status_frame = ModernFrame(self.master, bg_color=COLORS['bg_tertiary'])
        status_frame.pack(fill='x', side='bottom', padx=20, pady=(0, 20))
       
        self.status_label = ModernLabel(status_frame,
                                      text="💡 Ready to simulate quantum transmission",
                                      font=('Segoe UI', 10),
                                      fg=COLORS['text_secondary'],
                                      bg=COLORS['bg_tertiary'])
        self.status_label.pack(pady=8)

    def start_transmission(self):
        """Start the transmission animation"""
        self.message = self.input_var.get().strip()
        if not self.message:
            messagebox.showwarning("Input Required", "Please enter a message to transmit!")
            return
       
        # Clear previous transmission
        self.text_canvas.delete("all")
        self.binary_canvas.delete("all")
        self.binaries = []
        self.binary_items = []
        self.text_items = []
        self.error_index = None
        self.error_bit_pos = None
        self.output_var.set("")
       
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
       
        self.status_label.config(text="🚀 Starting quantum transmission...",
                               fg=COLORS['accent_primary'])
        self.animate_transmission(0)

    def animate_transmission(self, index):
        """Animate the transmission process"""
        if index >= len(self.message):
            self.status_label.config(text="✅ Transmission complete! Ready for error correction.",
                                   fg=COLORS['success'])
            self.progress_var.set(100)
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
       
        def move():
            # Introduce random error
            if random.random() < 0.3 and self.error_index is None:  # 30% chance
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
           
            self.master.after(800, lambda: self.animate_transmission(index + 1))
       
        move()

    def correct_error(self):
        """Apply error correction"""
        if self.error_index is None:
            messagebox.showinfo("No Error", "No error detected to correct!")
            return
       
        # Correct the error
        corrected = list(self.binaries[self.error_index])
        corrected[self.error_bit_pos] = ("1" if corrected[self.error_bit_pos] == "0" else "0")
        corrected_str = "".join(corrected)
       
        self.binary_canvas.itemconfig(self.binary_items[self.error_index],
                                    text=corrected_str,
                                    fill=COLORS['success'])
        self.binaries[self.error_index] = corrected_str
       
        # Update received text
        received_text = "".join([chr(int(b, 2)) for b in self.binaries])
        self.output_var.set(received_text)
       
        self.status_label.config(text="🔧 Quantum error correction applied successfully! ✨",
                               fg=COLORS['success'])

    def show_backend_circuit(self):
        """Show the quantum circuits in a popup"""
        if not self.message:
            messagebox.showwarning("No Data", "Please send a message first!")
            return
       
        logical_state = "1" if ord(self.message[0]) % 2 else "0"
        error_qubit = random.randint(0, 2)
        qc_encode, qc_error, qc_full, counts, fidelity, error_info = run_bitflip_qec(
            logical_state, error_qubit
        )
       
        popup = tk.Toplevel(self.master)
        popup.title("🔬 Quantum Circuit Analysis")
        popup.configure(bg=COLORS['bg_primary'])
        popup.geometry("800x900")
       
        # Create notebook for tabs
        notebook = ttk.Notebook(popup)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
       
        # Encoding tab
        encode_frame = tk.Frame(notebook, bg=COLORS['bg_primary'])
        notebook.add(encode_frame, text="Encoding Circuit")
       
        fig1 = qc_encode.draw("mpl", style={'backgroundcolor': COLORS['bg_primary']})
        canvas1 = FigureCanvasTkAgg(fig1, master=encode_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig1)
       
        # Error tab
        error_frame = tk.Frame(notebook, bg=COLORS['bg_primary'])
        notebook.add(error_frame, text="Error Circuit")
       
        fig2 = qc_error.draw("mpl", style={'backgroundcolor': COLORS['bg_primary']})
        canvas2 = FigureCanvasTkAgg(fig2, master=error_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig2)
       
        # Correction tab
        correction_frame = tk.Frame(notebook, bg=COLORS['bg_primary'])
        notebook.add(correction_frame, text="Full QEC Circuit")
       
        fig3 = qc_full.draw("mpl", style={'backgroundcolor': COLORS['bg_primary']})
        canvas3 = FigureCanvasTkAgg(fig3, master=correction_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig3)
       
        # Results tab
        results_frame = tk.Frame(notebook, bg=COLORS['bg_primary'])
        notebook.add(results_frame, text="Measurement Results")
       
        # Create subplot figure
        fig_results, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        fig_results.patch.set_facecolor(COLORS['bg_primary'])
       
        # Histogram
        plot_histogram(counts, ax=ax1, color=COLORS['accent_primary'])
        ax1.set_facecolor(COLORS['bg_secondary'])
        ax1.tick_params(colors=COLORS['text_primary'])
        ax1.set_title("Measurement Counts", color=COLORS['text_primary'])
       
        # Fidelity bar
        ax2.bar(["Fidelity"], [fidelity], color=COLORS['success'])
        ax2.set_ylim(0, 1)
        ax2.set_ylabel("Fidelity", color=COLORS['text_primary'])
        ax2.set_title("Quantum Fidelity", color=COLORS['text_primary'])
        ax2.set_facecolor(COLORS['bg_secondary'])
        ax2.tick_params(colors=COLORS['text_primary'])
       
        plt.tight_layout()
        canvas_results = FigureCanvasTkAgg(fig_results, master=results_frame)
        canvas_results.draw()
        canvas_results.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig_results)

    def show_fidelity_plot(self):
        """Show fidelity and accuracy plots"""
        popup = tk.Toplevel(self.master)
        popup.title("📊 Performance Metrics")
        popup.configure(bg=COLORS['bg_primary'])
        popup.geometry("700x500")
       
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor(COLORS['bg_primary'])
        ax.set_facecolor(COLORS['bg_secondary'])
       
        # Generate sample data
        runs = list(range(1, 11))
        fidelities = [random.uniform(0.85, 1.0) for _ in range(10)]
        accuracies = [random.uniform(80, 100) for _ in range(10)]
       
        ax.plot(runs, fidelities, 'o-', label="Fidelity",
                color=COLORS['accent_primary'], linewidth=3, markersize=8)
        ax.plot(runs, [a/100 for a in accuracies], 's-', label="Accuracy (normalized)",
                color=COLORS['success'], linewidth=3, markersize=8)
       
        ax.set_ylim(0, 1.1)
        ax.set_xlabel("Run Number", color=COLORS['text_primary'], fontsize=12)
        ax.set_ylabel("Performance Metric", color=COLORS['text_primary'], fontsize=12)
        ax.set_title("Quantum Error Correction Performance",
                    color=COLORS['text_primary'], fontsize=14, fontweight='bold')
        ax.legend(facecolor=COLORS['bg_tertiary'],
                 edgecolor=COLORS['accent_primary'],
                 labelcolor=COLORS['text_primary'])
        ax.tick_params(colors=COLORS['text_primary'])
        ax.grid(True, alpha=0.3, color=COLORS['text_secondary'])
       
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=20, pady=20)
        plt.close(fig)


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = UserTransmissionSimulator(root)
   
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

