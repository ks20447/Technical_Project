from PIL import Image, ImageDraw

# Parameters
W, H = 250, 250  # Size of the pattern
L = 25  # Size of each square
num_hor = W // L
num_vert = H // L
name = "intensity_rgb"

# Create a new image with RGBA mode to support opacity
background = Image.new('RGB', (W, H), (255, 255, 255)) 
draw = ImageDraw.Draw(background)

for i in range(num_vert):
    intensity = int(255 - (i * (255 / num_vert)))  # Linear decrease in intensity
    for j in range(num_hor):
        # Alternate color between blue, yellow and white
        if j % 3 == 0:
            color = (intensity, 0, 0)  # 
        elif j % 3 == 1:
            color = (0, intensity, 0)
        else:
            color = (0, 0, intensity)  # White with varying intensity
        
        # Calculate the position of the square
        top_left = (j * L, i * L)
        bottom_right = (j * L + L, i * L + L)
        
        # Draw the rectangle
        draw.rectangle([top_left, bottom_right], fill=color)

# Save the image
background.save(f'Patterns/pattern_{name}.png')
