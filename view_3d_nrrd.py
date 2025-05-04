import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

# Read the NRRD file
image = sitk.ReadImage('output/dzz_t1_montage.nrrd')

# Convert to numpy array
array = sitk.GetArrayFromImage(image)

# Create figure and subplots
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 3, height_ratios=[4, 1])

# Create subplots for images
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

# Create subplots for sliders
ax_slider_z = fig.add_subplot(gs[1, 0])
ax_slider_y = fig.add_subplot(gs[1, 1])
ax_slider_x = fig.add_subplot(gs[1, 2])

# Initial slices
z_slice = array.shape[0] // 2
y_slice = array.shape[1] // 2
x_slice = array.shape[2] // 2

# Create image plots
img1 = ax1.imshow(array[z_slice, :, :], cmap='gray')
ax1.set_title('Z Slice')
ax1.axis('off')

img2 = ax2.imshow(array[:, y_slice, :], cmap='gray')
ax2.set_title('Y Slice')
ax2.axis('off')

img3 = ax3.imshow(array[:, :, x_slice], cmap='gray')
ax3.set_title('X Slice')
ax3.axis('off')

# Create sliders
slider_z = Slider(ax_slider_z, 'Z', 0, array.shape[0]-1, valinit=z_slice, valstep=1)
slider_y = Slider(ax_slider_y, 'Y', 0, array.shape[1]-1, valinit=y_slice, valstep=1)
slider_x = Slider(ax_slider_x, 'X', 0, array.shape[2]-1, valinit=x_slice, valstep=1)

# Update functions for sliders
def update_z(val):
    z = int(val)
    img1.set_data(array[z, :, :])
    fig.canvas.draw_idle()

def update_y(val):
    y = int(val)
    img2.set_data(array[:, y, :])
    fig.canvas.draw_idle()

def update_x(val):
    x = int(val)
    img3.set_data(array[:, :, x])
    fig.canvas.draw_idle()

# Register update functions
slider_z.on_changed(update_z)
slider_y.on_changed(update_y)
slider_x.on_changed(update_x)

plt.tight_layout()
plt.show() 