import os
import itk
from pathlib import Path

# Set up paths
input_dir = Path("examples/SampleData_DzZ_T1")
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)
output_file = output_dir / "dzz_t1_montage.nrrd"

dimension = 3  # Changed to 3D

# Read tile configuration
stage_tiles = itk.TileConfiguration[dimension]()
stage_tiles.Parse(str(input_dir / "TileConfiguration.txt"))

# Read images
color_images = []  # for mosaic creation
grayscale_images = []  # for registration
for t in range(stage_tiles.LinearSize()):
    origin = stage_tiles.GetTile(t).GetPosition()
    filename = str(input_dir / stage_tiles.GetTile(t).GetFileName())
    image = itk.imread(filename)
    spacing = image.GetSpacing()

    # Convert pixel coordinates to physical coordinates
    for d in range(dimension):
        origin[d] *= spacing[d]

    image.SetOrigin(origin)
    color_images.append(image)

    image = itk.imread(filename, itk.F)  # read as grayscale
    image.SetOrigin(origin)
    grayscale_images.append(image)

# Create montage
print("Computing tile registration transforms")
montage = itk.TileMontage[type(grayscale_images[0]), itk.F].New()
montage.SetMontageSize(stage_tiles.GetAxisSizes())
for t in range(stage_tiles.LinearSize()):
    montage.SetInputTile(t, grayscale_images[t])
montage.Update()

# Write transforms
print("Writing tile transforms")
actual_tiles = stage_tiles
for t in range(stage_tiles.LinearSize()):
    index = stage_tiles.LinearIndexToNDIndex(t)
    regTr = montage.GetOutputTransform(index)
    tile = stage_tiles.GetTile(t)
    itk.transformwrite([regTr], str(output_dir / (tile.GetFileName() + ".tfm")))

    # Update positions
    pos = tile.GetPosition()
    for d in range(dimension):
        pos[d] -= regTr.GetOffset()[d] / spacing[d]
    tile.SetPosition(pos)
    actual_tiles.SetTile(t, tile)
actual_tiles.Write(str(output_dir / "TileConfiguration.registered.txt"))

# Create final mosaic
print("Producing the mosaic")
input_pixel_type = itk.template(color_images[0])[1][0]
try:
    input_rgb_type = itk.template(input_pixel_type)[0]
    accum_type = input_rgb_type[itk.F]  # RGB or RGBA input/output images
except KeyError:
    accum_type = itk.D  # scalar input / output images

resampleF = itk.TileMergeImageFilter[type(color_images[0]), accum_type].New()
resampleF.SetMontageSize(stage_tiles.GetAxisSizes())
for t in range(stage_tiles.LinearSize()):
    resampleF.SetInputTile(t, color_images[t])
    index = stage_tiles.LinearIndexToNDIndex(t)
    resampleF.SetTileTransform(index, montage.GetOutputTransform(index))
resampleF.Update()
itk.imwrite(resampleF.GetOutput(), str(output_file))
print("Resampling complete")
print(f"Output saved to {output_file}") 