import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

# Read the NRRD file
image = sitk.ReadImage('output/cmu_run2_montage.nrrd')

# Convert to numpy array
array = sitk.GetArrayFromImage(image)

# Display the image
plt.figure(figsize=(10, 10))
plt.imshow(array, cmap='gray')
plt.colorbar()
plt.title('Montage Image')
plt.show() 