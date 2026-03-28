# 🔬 Quantum Error Correction Simulator

A modern, interactive **Quantum Error Correction (QEC) Simulator** built in **Python** using **Tkinter** and **Qiskit**.  
Simulate quantum bit-flip error correction, visualize text and binary transmission, and analyze quantum circuits with interactive performance metrics.

---

## 🚀 Features

- **Text-to-Binary Transmission Visualization**  
  Simulate message transmission over a quantum channel with real-time binary representation.

- **Quantum Bit-Flip Error Simulation**  
  Introduce random bit-flip errors in transmitted qubits to emulate noisy quantum communication.

- **Error Correction Mechanism**  
  Automatically apply the **3-qubit bit-flip QEC code** to correct errors and recover the original message.

- **Interactive Quantum Circuit Display**  
  View **encoding**, **error**, and **full QEC circuits** in a tabbed interface.

- **Performance Metrics Visualization**  
  Generate plots for **fidelity** and **accuracy** of the quantum error correction process.

- **Modern GUI with Tkinter**  
  Custom-styled frames, buttons, progress bars, and visual feedback for a polished user experience.

---

## 🛠️ Technologies Used

- **Programming Language:** Python 3  
- **Libraries & Tools:**  
  - [Tkinter](https://docs.python.org/3/library/tkinter.html) – GUI design  
  - [Qiskit](https://qiskit.org/) – Quantum circuit simulation  
  - [Matplotlib](https://matplotlib.org/) – Circuit visualization and performance plots  
  - [Qiskit Aer Simulator](https://qiskit.org/documentation/apidoc/aer.html) – High-performance quantum simulation  

---

## 💡 How It Works

1. **User Input:**  
   Enter a text message to transmit.

2. **Binary Conversion:**  
   Each character is converted to its **8-bit binary representation**.

3. **Quantum Error Simulation:**  
   Random bit-flip errors are introduced in the binary qubits with a probability.

4. **Error Correction:**  
   The **3-qubit bit-flip code** corrects any single qubit error and restores the original data.

5. **Visualization:**  
   - Highlighted text and binary transmission in real time  
   - Tabbed display of **quantum circuits**  
   - Performance plots of **fidelity** and **accuracy**

---

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/pujithabuchupalli/quantum-simulator.git
cd quantum-simulator
Create a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
Install required packages:
pip install -r requirements.txt

requirements.txt should include:

qiskit
matplotlib
🎮 How to Run
python quantum_simulator.py
Enter a message in the input box.
Click Send Message to simulate quantum transmission.
Use Show Quantum Circuits and Show Performance Metrics for analysis.
Click Apply Error Correction to correct any detected errors.
