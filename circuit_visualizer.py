"""Quantum circuit visualization and analysis"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from qiskit.visualization import plot_histogram
import random
from config import COLORS
from quantum_backend import run_bitflip_qec


class CircuitVisualizer:
    """Handles quantum circuit visualization and performance metrics"""
    
    def __init__(self, parent):
        self.parent = parent
    
    def show_quantum_circuits(self, message):
        """Show quantum circuits in a popup window"""
        if not message:
            return
        
        logical_state = "1" if ord(message[0]) % 2 else "0"
        error_qubit = random.randint(0, 2)
        qc_encode, qc_error, qc_full, counts, fidelity, error_info = run_bitflip_qec(
            logical_state, error_qubit
        )
        
        popup = tk.Toplevel(self.parent)
        popup.title("🔬 Quantum Circuit Analysis")
        popup.configure(bg=COLORS['bg_primary'])
        popup.geometry("800x900")
        
        # Create notebook for tabs
        notebook = ttk.Notebook(popup)
        notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create tabs
        self._create_encoding_tab(notebook, qc_encode)
        self._create_error_tab(notebook, qc_error)
        self._create_correction_tab(notebook, qc_full)
        self._create_results_tab(notebook, counts, fidelity, error_info)
    
    def _create_encoding_tab(self, notebook, qc_encode):
        """Create encoding circuit tab"""
        encode_frame = tk.Frame(notebook, bg=COLORS['bg_primary'])
        notebook.add(encode_frame, text="Encoding Circuit")
        
        fig1 = qc_encode.draw("mpl", style={'backgroundcolor': COLORS['bg_primary']})
        canvas1 = FigureCanvasTkAgg(fig1, master=encode_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig1)
    
    def _create_error_tab(self, notebook, qc_error):
        """Create error circuit tab"""
        error_frame = tk.Frame(notebook, bg=COLORS['bg_primary'])
        notebook.add(error_frame, text="Error Circuit")
        
        fig2 = qc_error.draw("mpl", style={'backgroundcolor': COLORS['bg_primary']})
        canvas2 = FigureCanvasTkAgg(fig2, master=error_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig2)
    
    def _create_correction_tab(self, notebook, qc_full):
        """Create full QEC circuit tab"""
        correction_frame = tk.Frame(notebook, bg=COLORS['bg_primary'])
        notebook.add(correction_frame, text="Full QEC Circuit")
        
        fig3 = qc_full.draw("mpl", style={'backgroundcolor': COLORS['bg_primary']})
        canvas3 = FigureCanvasTkAgg(fig3, master=correction_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill='both', expand=True)
        plt.close(fig3)
    
    def _create_results_tab(self, notebook, counts, fidelity, error_info):
        """Create measurement results tab"""
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
    
    def show_performance_metrics(self):
        """Show fidelity and accuracy performance plots"""
        popup = tk.Toplevel(self.parent)
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
