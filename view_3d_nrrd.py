import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
import sys
import os

def view_3d_nrrd(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Read the NRRD file
    print(f"Reading file: {file_path}")
    image = sitk.ReadImage(file_path)
    
    # Get image information
    size = image.GetSize()
    spacing = image.GetSpacing()
    origin = image.GetOrigin()
    
    # Print image information
    print(f"Image size: {size}")
    print(f"Pixel spacing: {spacing}")
    print(f"Image origin: {origin}")
    
    # Convert to numpy array
    array = sitk.GetArrayFromImage(image)
    
    # Determine dimensionality
    ndim = len(array.shape)
    if ndim != 3:
        print(f"This is a {ndim}D image, not a 3D image. For 2D visualization, please use view_nrrd.py")
        return
    
    # Get min and max for contrast adjustment
    data_min = np.min(array)
    data_max = np.max(array)
    data_range = data_max - data_min
    
    # Create figure and subplots
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, height_ratios=[5, 5, 1])
    
    # Create subplots for images
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    
    # Create subplot for contrast
    ax_slider_contrast = fig.add_subplot(gs[1, 0])
    ax_slider_brightness = fig.add_subplot(gs[1, 1])
    ax_colormap = fig.add_subplot(gs[1, 2])
    
    # Create subplots for sliders
    ax_slider_z = fig.add_subplot(gs[2, 0])
    ax_slider_y = fig.add_subplot(gs[2, 1])
    ax_slider_x = fig.add_subplot(gs[2, 2])
    
    # Initial slices
    z_slice = array.shape[0] // 2
    y_slice = array.shape[1] // 2
    x_slice = array.shape[2] // 2
    
    # Available colormaps
    cmaps = ['gray', 'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'hot']
    current_cmap = cmaps[0]
    
    # Create image plots
    img1 = ax1.imshow(array[z_slice, :, :], cmap=current_cmap, 
                     vmin=data_min, vmax=data_max)
    ax1.set_title(f'Z Slice: {z_slice}')
    
    img2 = ax2.imshow(array[:, y_slice, :], cmap=current_cmap,
                     vmin=data_min, vmax=data_max)
    ax2.set_title(f'Y Slice: {y_slice}')
    
    img3 = ax3.imshow(array[:, :, x_slice], cmap=current_cmap,
                     vmin=data_min, vmax=data_max)
    ax3.set_title(f'X Slice: {x_slice}')
    
    # Create annotations for each view
    annot1 = ax1.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
    annot1.set_visible(False)
    
    annot2 = ax2.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
    annot2.set_visible(False)
    
    annot3 = ax3.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                         bbox=dict(boxstyle="round", fc="w"), arrowprops=dict(arrowstyle="->"))
    annot3.set_visible(False)
    
    # Create sliders
    slider_z = Slider(ax_slider_z, 'Z', 0, array.shape[0]-1, valinit=z_slice, valstep=1)
    slider_y = Slider(ax_slider_y, 'Y', 0, array.shape[1]-1, valinit=y_slice, valstep=1)
    slider_x = Slider(ax_slider_x, 'X', 0, array.shape[2]-1, valinit=x_slice, valstep=1)
    
    # Create contrast and brightness sliders
    slider_contrast = Slider(ax_slider_contrast, 'Contrast', 0.1, 3.0, valinit=1.0)
    slider_brightness = Slider(ax_slider_brightness, 'Brightness', -0.5, 0.5, valinit=0.0)
    
    # Create colormap radio buttons
    radio = RadioButtons(ax_colormap, cmaps)
    
    # Update functions for sliders
    def update_z(val):
        z = int(val)
        img1.set_data(array[z, :, :])
        ax1.set_title(f'Z Slice: {z}')
        fig.canvas.draw_idle()
    
    def update_y(val):
        y = int(val)
        img2.set_data(array[:, y, :])
        ax2.set_title(f'Y Slice: {y}')
        fig.canvas.draw_idle()
    
    def update_x(val):
        x = int(val)
        img3.set_data(array[:, :, x])
        ax3.set_title(f'X Slice: {x}')
        fig.canvas.draw_idle()
    
    def update_contrast_brightness(val=None):
        contrast = slider_contrast.val
        brightness = slider_brightness.val
        vmin = data_min * contrast - brightness * data_range
        vmax = data_max * contrast + brightness * data_range
        img1.set_clim(vmin, vmax)
        img2.set_clim(vmin, vmax)
        img3.set_clim(vmin, vmax)
        fig.canvas.draw_idle()
    
    def update_colormap(label):
        nonlocal current_cmap
        current_cmap = label
        img1.set_cmap(current_cmap)
        img2.set_cmap(current_cmap)
        img3.set_cmap(current_cmap)
        fig.canvas.draw_idle()
    
    # Mouse hover functions
    def update_annot1(event):
        if event.inaxes == ax1:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= y < array.shape[1] and 0 <= x < array.shape[2]:
                z = int(slider_z.val)
                annot1.xy = (x, y)
                text = f"Position: ({x}, {y}, {z})\nValue: {array[z, y, x]:.2f}"
                annot1.set_text(text)
                annot1.set_visible(True)
                fig.canvas.draw_idle()
            else:
                annot1.set_visible(False)
                fig.canvas.draw_idle()
        else:
            if annot1.get_visible():
                annot1.set_visible(False)
                fig.canvas.draw_idle()
                
    def update_annot2(event):
        if event.inaxes == ax2:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= y < array.shape[0] and 0 <= x < array.shape[2]:
                yi = int(slider_y.val)
                annot2.xy = (x, y)
                text = f"Position: ({x}, {yi}, {y})\nValue: {array[y, yi, x]:.2f}"
                annot2.set_text(text)
                annot2.set_visible(True)
                fig.canvas.draw_idle()
            else:
                annot2.set_visible(False)
                fig.canvas.draw_idle()
        else:
            if annot2.get_visible():
                annot2.set_visible(False)
                fig.canvas.draw_idle()
                
    def update_annot3(event):
        if event.inaxes == ax3:
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= y < array.shape[0] and 0 <= x < array.shape[1]:
                xi = int(slider_x.val)
                annot3.xy = (x, y)
                text = f"Position: ({xi}, {x}, {y})\nValue: {array[y, x, xi]:.2f}"
                annot3.set_text(text)
                annot3.set_visible(True)
                fig.canvas.draw_idle()
            else:
                annot3.set_visible(False)
                fig.canvas.draw_idle()
        else:
            if annot3.get_visible():
                annot3.set_visible(False)
                fig.canvas.draw_idle()
    
    # Register update functions
    slider_z.on_changed(update_z)
    slider_y.on_changed(update_y)
    slider_x.on_changed(update_x)
    slider_contrast.on_changed(update_contrast_brightness)
    slider_brightness.on_changed(update_contrast_brightness)
    radio.on_clicked(update_colormap)
    
    # Connect mouse hover events
    fig.canvas.mpl_connect("motion_notify_event", update_annot1)
    fig.canvas.mpl_connect("motion_notify_event", update_annot2)
    fig.canvas.mpl_connect("motion_notify_event", update_annot3)
    
    plt.suptitle(f'3D NRRD Viewer: {os.path.basename(file_path)}', fontsize=16)
    plt.tight_layout()
    plt.subplots_adjust(top=0.95)
    plt.show()

if __name__ == "__main__":
    # If no argument provided, use default file
    if len(sys.argv) < 2:
        file_path = 'output/dzz_t1_montage.nrrd'
        print("No file specified, using default:", file_path)
    else:
        file_path = sys.argv[1]
    
    view_3d_nrrd(file_path) 