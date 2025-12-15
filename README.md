# 🍽️ Your foodie expert

A restaurant recommendation expert system built with Python, Tkinter, and Prolog.

## Features

- Intelligent filtering using Prolog logic
- Restaurant recommendations near Esmeralda 920
- Smart question generation
- Pastel pink interface with Tkinter

## Requirements

- Python 3.7+
- `tkinter` 
- `pyswip`
- SWI-Prolog installed on your system

## Installation

### 1. Install requirements
```
pip install -r requirements.txt
```

### 2. Install SWI-Prolog
- **Windows**: Download from [swipl.org](https://www.swi-prolog.org/download/stable)
- **macOS**: `brew install swi-prolog`
- **Linux**: `sudo apt-get install swi-prolog`

### 3. Files 
- `gui.py` - Tkinter GUI
- `expert.py` - expert system logic
- `places.pl` - Prolog knowledge base

## Usage
Run the application:
```bash
python gui.py
```

## How it works

1. **Start** - Click the Start button on the welcome screen
2. **Answer questions** - The system asks about your preferences (restaurant type, cuisine, budget, etc.)
3. **Get recommendations** - Based on your answers, you'll get personalized restaurant recommendations
4. **Restart** - Click the Restart button to start over
