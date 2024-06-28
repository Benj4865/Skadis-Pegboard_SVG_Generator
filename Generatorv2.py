import tkinter as tk
from tkinter import messagebox
import svgwrite
from svgwrite.path import Path

def generate_pegboard_svg(board_width, board_height, hole_width, hole_height, h_spacing, v_spacing, row_shift, edge_distance, output_file):
    dwg = svgwrite.Drawing(output_file, profile='tiny', size=(board_width, board_height))

    def draw_hole(x, y, remove_hole): # The function for drawing the holes
        if not remove_hole:
            rect_height = hole_height -  (2 * hole_width)  # Height of the rectangular part
            rect_y = y - rect_height / 2  # Center the rectangle vertically

            # Create the rectangle part of the hole
            dwg.add(dwg.rect(insert=(x - hole_width / 2, rect_y), size=(hole_width, rect_height), fill='none', stroke='red', stroke_width='0.25'))

            # Create the top and bottom semi-circles using paths
            top_arc_path = Path(d=f"M {x - hole_width / 2} {rect_y} A {hole_width / 2} {hole_width / 2} 0 0 1 {x + hole_width / 2} {rect_y}", fill='none', stroke='red', stroke_width='0.25')
            dwg.add(top_arc_path)

            bottom_arc_path = Path(d=f"M {x - hole_width / 2} {rect_y + rect_height} A {hole_width / 2} {hole_width / 2} 0 0 0 {x + hole_width / 2} {rect_y + rect_height}", fill='none', stroke='red', stroke_width='0.25')
            dwg.add(bottom_arc_path)

    num_cols = int((board_width - 2 * edge_distance) // h_spacing) + 1
    num_rows = int((board_height - 2 * edge_distance) // v_spacing) + 1

    for row in range(num_rows): #Drawing holes
        row_offset = row_shift if row % 2 != 0 else 0
        for col in range(num_cols):
            x = edge_distance + col * h_spacing - row_offset
            y = edge_distance + row * v_spacing
            if edge_distance <= x <= (board_width - edge_distance) and edge_distance <= y <= (board_height - edge_distance):
                remove_hole = col % 2 == 1
                draw_hole(x, y, remove_hole)

    dwg.add(dwg.rect(insert=(0, 0), size=(board_width, board_height), fill='none', stroke='red', stroke_width=0.25))
    dwg.save()

def generate_board(): #Generating the board without holes first
    try:
        board_width = int(width_entry.get())
        board_height = int(height_entry.get())
        board_name = name_entry.get()

        generate_pegboard_svg(
            board_width=board_width,
            board_height=board_height,
            hole_width=5,
            hole_height=20,  # Adjust the height to create the elongated hole
            h_spacing=20,
            v_spacing=20,
            row_shift=20,
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
