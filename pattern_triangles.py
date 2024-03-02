from PIL import Image, ImageDraw

# Parameters
name = "triangles"
scale = 50  # Scale of the pattern
num_triangles = 7
tri_colors_top = ["#00eaff", "#ff00ff", "#0024ff", "#ff0000", "#00ff00", "#fcff00", "#fcff00"]
tri_colors_bottom = ["#ff0000", "#00ff00", "#fcff00", "#00eaff", "#ff00ff", "#0024ff", "#0024ff"]
# tri_colors_top = ["white"] * 7
# tri_colors_bottom = ["white"] * 7

circle_color = "white"
outline_color = "white"
width, height = 1000, 1000

# Create a base pattern image
base_pattern_size = scale
base_pattern = Image.new('RGB', (base_pattern_size * 3, base_pattern_size * 2), 'white')
draw = ImageDraw.Draw(base_pattern)

# Create top row of triangles
for tri_num_top in range(-1, num_triangles - 1):
    # Flips triangle every other triangle
    if tri_num_top % 2 == 0:
        rotation = 1
    else:
        rotation = 0

    triangle = [(tri_num_top * scale / 2, scale * rotation), ((tri_num_top + 1) * scale / 2, scale - scale * rotation), ((tri_num_top + 2) * scale / 2, scale * rotation)]
    draw.polygon(triangle, fill=tri_colors_top[tri_num_top])
    
# Create bottom row of triangles
for tri_num_top in range(-1, num_triangles - 1):
    # Flips triangle every other triangle
    if tri_num_top % 2 == 0:
        rotation = 0
    else:
        rotation = 1

    triangle = [(tri_num_top * scale / 2, scale + scale * rotation), ((tri_num_top + 1) * scale / 2, 2*scale - scale * rotation), ((tri_num_top + 2) * scale / 2, scale + scale * rotation)]
    draw.polygon(triangle, fill=tri_colors_bottom[tri_num_top])
 
# Create top and bottom row circles     
for circ_top_bottom in range(0, 3):
    circle_coords = [(scale/4 + scale * circ_top_bottom, -scale/4), (3*scale/4 + scale * circ_top_bottom, scale/4)]
    draw.pieslice(circle_coords, 0, 360, fill=circle_color)
    
    circle_coords = [(scale/4 + scale * circ_top_bottom, 7*scale/4), (3*scale/4 + scale * circ_top_bottom, 9*scale/4)]
    draw.pieslice(circle_coords, 0, 360, fill=circle_color)
    
# Create middle row circles
for circ_mid in range(0, 4):
    circle_coords = [(-scale/4 + scale * circ_mid, 3*scale/4), (scale/4 + scale * circ_mid, 5*scale/4)]
    draw.pieslice(circle_coords, 0, 360, fill=circle_color)
  
# Show base pattern 
# base_pattern.show()

# Create the final image
final_image = Image.new('RGB', (width, height), 'white')

# Paste the base pattern across the final image
for x in range(0, width, base_pattern_size * 3):
    for y in range(0, height, base_pattern_size * 2):
        final_image.paste(base_pattern, (x, y))

# Display the final image
# final_image.show()

# Save the final image
final_image.save(f'Patterns/pattern_{name}.pdf')
final_image.save(f'Patterns/pattern_{name}.png')