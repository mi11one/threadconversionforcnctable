import re
import tkinter as tk
from tkinter import filedialog

# Initialize Tkinter
root = tk.Tk()
root.withdraw()  # Hide the main Tkinter window

# Step 1: Extract PEG coordinates
def extract_peg_coordinates(text):
    peg_coordinates = {}
    peg_pattern = re.compile(r'PEG_(\d+): x=([\d.]+) ; y=([\d.]+)')
    conversion_factor = 25.4  # Millimeters to inches conversion factor
    for match in peg_pattern.findall(text):
        peg_id = int(match[0])
        x = float(match[1]) / conversion_factor  # Convert x to inches
        y = float(match[2]) / conversion_factor  # Convert y to inches
        peg_coordinates[peg_id] = (x, y)
    return peg_coordinates

# Step 2: Extract sequence of PEG commands
def extract_peg_sequence(text):
    sequence_pattern = re.compile(r'PEG_(\d+)')
    return [int(match) for match in sequence_pattern.findall(text)]

# Open a file dialog window to select the input file
input_file_path = filedialog.askopenfilename(title="Select a text file to open", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

try:
    with open(input_file_path, 'r') as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: The file at {input_file_path} was not found.")
    exit(1)
except IOError as e:
    print(f"Error reading the file: {e}")
    exit(1)

# Extract PEG coordinates
peg_coordinates = extract_peg_coordinates(content)

# Find the greatest y-coordinate and calculate the scaling factor
max_y = max(y for x, y in peg_coordinates.values())
scaling_factor = 20 / max_y

# Scale the coordinates
scaled_peg_coordinates = {peg_id: (x * scaling_factor, y * scaling_factor) for peg_id, (x, y) in peg_coordinates.items()}

# Recalculate the greatest x and y coordinates after scaling
max_x_scaled = max(x for x, y in scaled_peg_coordinates.values())
max_y_scaled = max(y for x, y in scaled_peg_coordinates.values())

# Calculate value1, value2, and value3
value1 = max_x_scaled / 2
value2 = max_y_scaled / 4
value3 = 3 * max_y_scaled / 4

# Extract sequence of PEG commands
sequence_start_keyword = "Then here are the steps of the thread:"
if sequence_start_keyword not in content:
    print(f"Error: The sequence start keyword '{sequence_start_keyword}' was not found in the text.")
    exit(1)

peg_sequence = extract_peg_sequence(content.split(sequence_start_keyword)[1])

# Ask where to save the output file
output_file_path = filedialog.asksaveasfilename(title="Save output file as", defaultextension=".txt", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

# Convert sequence to coordinates and apply conditions with movements
coordinates_sequence = []

with open(output_file_path, 'w') as output_file:
    # Add the new lines of text before writing the coordinates
    output_file.write("G20\n")
    output_file.write("G90\n")
    output_file.write("G53\n")
    
    for peg in peg_sequence:
        if peg in scaled_peg_coordinates:
            x, y = scaled_peg_coordinates[peg]
            
            # Apply conditions and offsets with movements
            if x > value1 and value2 < y < value3:
                offset_x = x - 0.2
                offset_y = y
                output_file.write(f"G0 X{offset_x:.4f} Y{offset_y:.4f} Z0\n")  # Rapid positioning
                output_file.write(f"G91\n")  # Incremental positioning mode
                output_file.write(f"G3 X0.4 Z-0.125 I0.2 F75\nG3 X-0.4 Z0.125 I-0.2 F75\n")  # Arc move with I parameter
                output_file.write(f"G1 X-0.2 Z0.5\n")  # Move Z axis down by 0.05 units
                output_file.write(f"G90\n")  # Absolute positioning mode
            elif x > value1 and y <= value2:
                offset_x = x - 0.15
                offset_y = y + 0.15
                output_file.write(f"G0 X{offset_x:.4f} Y{offset_y:.4f} Z0\n")  # Rapid positioning
                output_file.write(f"G91\n")  # Incremental positioning mode
                output_file.write(f"G3 X0.3 Y-0.3 Z-0.125 I0.15 J-0.15 F75\nG3 X-0.3 Y0.3 Z0.125 I-0.15 J0.15 F75\n")  # Arc move with I and J parameters
                output_file.write(f"G1 X-0.15 Y0.15 Z0.5\n")  # Move Z axis down by 0.05 units
                output_file.write(f"G90\n")  # Absolute positioning mode
            elif x <= value1 and value2 < y < value3:
                offset_x = x + 0.2
                offset_y = y
                output_file.write(f"G0 X{offset_x:.4f} Y{offset_y:.4f} Z0\n")  # Rapid positioning
                output_file.write(f"G91\n")  # Incremental positioning mode
                output_file.write(f"G3 X-0.4 Z-0.5 I-0.2 F75\nG3 X0.4 Z0.125 I0.2 F75\n")  # Arc move with I parameter
                output_file.write(f"G1 X0.2 Z0.5\n")  # Move Z axis down by 0.05 units
                output_file.write(f"G90\n")  # Absolute positioning mode
            elif x <= value1 and y <= value3:
                offset_x = x + 0.15
                offset_y = y + 0.15
                output_file.write(f"G0 X{offset_x:.4f} Y{offset_y:.4f} Z0\n")  # Rapid positioning
                output_file.write(f"G91\n")  # Incremental positioning mode
                output_file.write(f"G3 X-0.3 Y-0.3 Z-0.125 I-0.15 J-0.15 F75\nG3 X0.3 Y0.3 Z0.125 I0.15 J0.15 F75\n")  # Arc move with I and J parameters
                output_file.write(f"G1 X0.15 Y0.15 Z0.5\n")  # Move Z axis down by 0.05 units
                output_file.write(f"G90\n")  # Absolute positioning mode
            elif x <= value1 and y > value3:
                offset_x = x + 0.15
                offset_y = y - 0.15
                output_file.write(f"G0 X{offset_x:.4f} Y{offset_y:.4f} Z0\n")  # Rapid positioning
                output_file.write(f"G91\n")  # Incremental positioning mode
                output_file.write(f"G3 X-0.3 Y0.3 Z-0.125 I-0.15 J0.15 F75\nG3 X0.3 Y-0.3 Z0.125 I0.15 J-0.15 F75\n")  # Arc move with I and J parameters
                output_file.write(f"G1 X0.15 Y-0.15 Z0.5\n")  # Move Z axis down by 0.05 units
                output_file.write(f"G90\n")  # Absolute positioning mode
            elif x > value1 and y > value3:
                offset_x = x - 0.15
                offset_y = y - 0.15
                output_file.write(f"G0 X{offset_x:.4f} Y{offset_y:.4f} Z0\n")  # Rapid positioning
                output_file.write(f"G91\n")  # Incremental positioning mode
                output_file.write(f"G3 X0.3 Y0.3 Z-0.125 I0.15 J0.15 F75\nG3 X-0.3 Y-0.3 Z0.125 I-0.15 J-0.15 F75\n")  # Arc move with I and J parameters
                output_file.write(f"G1 X-0.15 Y-0.15 Z0.5\n")  # Move Z axis down by 0.05 units
                output_file.write(f"G90\n")  # Absolute positioning mode
            else:
                offset_x = x
                offset_y = y
            
            coordinates_sequence.append((offset_x, offset_y))
        else:
            print(f"Warning: PEG_{peg} does not have corresponding coordinates.")
            coordinates_sequence.append((None, None))  # Placeholder for missing coordinates

print(f"G-code commands have been saved to {output_file_path}.")
