"""Configuration constants and color scheme for the Quantum Simulator"""

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

# Application constants
WINDOW_TITLE = "🔬 Quantum Error Correction Simulator"
WINDOW_GEOMETRY = "1200x950"
WINDOW_MIN_SIZE = (1000, 850)
PROGRESS_STYLE = 'Custom.Horizontal.TProgressbar'

# Animation constants
TRANSMISSION_DELAY = 800
ERROR_PROBABILITY = 0.3
PROGRESS_UPDATE_INTERVAL = 100

# Quantum circuit constants
DEFAULT_SHOTS = 1024
QUBIT_COUNT = 3
