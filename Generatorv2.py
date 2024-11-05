import tkinter as tk
from tkinter import messagebox
import svgwrite
from svgwrite.path import Path

def generate_pegboard_svg(board_width, board_height, hole_width, hole_height, h_spacing, v_spacing, row_shift, edge_distance, output_file):
    # Define the drawing with explicit units in millimeters
    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(f"{board_width}mm", f"{board_height}mm"))
    dwg.viewbox(0, 0, board_width, board_height)

    def draw_hole(x, y, remove_hole):
        if not remove_hole:
            corner_radius = hole_width / 2

            # Define path data to create the rounded-rectangle hole
            path_data = [
                f"M {x - corner_radius} {y - hole_height / 2}",  # Start top-left of rounded rectangle
                f"h {hole_width - 2 * corner_radius}",  # Horizontal line to top-right corner
                f"a {corner_radius} {corner_radius} 0 0 1 {corner_radius} {corner_radius}",  # Top-right arc
                f"v {hole_height - 2 * corner_radius}",  # Vertical line down
                f"a {corner_radius} {corner_radius} 0 0 1 {-corner_radius} {corner_radius}",  # Bottom-right arc
                f"h {-hole_width + 2 * corner_radius}",  # Horizontal line to bottom-left corner
                f"a {corner_radius} {corner_radius} 0 0 1 {-corner_radius} {-corner_radius}",  # Bottom-left arc
                f"v {-hole_height + 2 * corner_radius}",  # Vertical line up
                f"a {corner_radius} {corner_radius} 0 0 1 {corner_radius} {-corner_radius}",  # Top-left arc
                "Z"  # Close the path
            ]
            dwg.add(Path(d=" ".join(path_data), fill='none', stroke='red', stroke_width='0.25mm'))

    # Determine number of columns and rows based on spacing and board dimensions
    num_cols = int((board_width - 2 * edge_distance) / h_spacing) + 1
    num_rows = int((board_height - 2 * edge_distance) / v_spacing) + 1

    # Draw holes on the board
    for row in range(num_rows):
        row_offset = row_shift / 2 if row % 2 != 0 else 0
        for col in range(num_cols):
            x = edge_distance + col * h_spacing + row_offset
            y = edge_distance + row * v_spacing
            if edge_distance <= x <= (board_width - edge_distance) and edge_distance <= y <= (board_height - edge_distance):
                remove_hole = col % 2 == 1
                draw_hole(x, y, remove_hole)

    # Add a board outline with the specified dimensions
    dwg.add(dwg.rect(insert=(0, 0), size=(f"{board_width}mm", f"{board_height}mm"), fill='none', stroke='red', stroke_width='0.25mm'))
    dwg.save()

def generate_board():
    try:
        board_width = int(width_entry.get())
        board_height = int(height_entry.get())
        board_name = name_entry.get()

        generate_pegboard_svg(
            board_width=board_width,
            board_height=board_height,
            hole_width=5,
            hole_height=15,
            h_spacing=20,
            v_spacing=20,
            row_shift=40,
            edge_distance=16,
            output_file=f'{board_name}.svg'
        )

        messagebox.showinfo("Success", f"Board '{board_name}' generated successfully!")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid dimensions (numbers only)")

# GUI setup
root = tk.Tk()
root.title("Pegboard Generator")

# Labels and Entries
tk.Label(root, text="Board Width in mm:").pack()
width_entry = tk.Entry(root)
width_entry.pack()

tk.Label(root, text="Board Height in mm:").pack()
height_entry = tk.Entry(root)
height_entry.pack()

tk.Label(root, text="Board Name:").pack()
name_entry = tk.Entry(root)
name_entry.pack()

# Generate Button
generate_button = tk.Button(root, text="Generate Board", command=generate_board)
generate_button.pack()

root.mainloop()
