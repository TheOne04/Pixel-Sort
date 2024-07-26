from PIL import Image
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: pixel_sort infile outfile")

image_file = sys.argv[1]

try:
    with Image.open(image_file) as im:
        # im = im.rotate(90)
        image_format = im.format.lower()
        im = im.convert("HSV")
        w = im.width
        h = im.height
        image_array = list(im.getdata())


except FileNotFoundError:
    sys.exit(f"{sys.argv[1]}: no such file")

new_array = image_array.copy()

data = []
for i in range(len(image_array)):
    if 190 > image_array[i][-1] > 30:
        data.append(image_array[i][-1])
    else:
        data.append(0)

temp_data = []
for i in range(h):
    k = []
    for j in range(w):
        k.append(data[i * w + j])
    temp_data.append(k)
data = temp_data

# Sort pixel values
for i in range(h):
    start = 0
    end = 0
    started = False
    for j in range(w):
        if data[i][j] != 0 and started == False:
            start = i * w + j
            started = True
        elif data[i][j] == 0 and started == True:
            end = i * w + j - 1

            for c in range(start, end + 1):
                for k in range(start, end):
                    if new_array[k] > new_array[k + 1]:
                        temp = new_array[k]
                        new_array[k] = new_array[k + 1]
                        new_array[k + 1] = temp
            started = False


n = Image.new("HSV", (w, h))
n.putdata(new_array)
n = n.convert(mode="RGB")

try:
    n.save(sys.argv[2])
except ValueError:
    response = input(f"outfile: invalid or  missing file extension, save instead to {sys.argv[2] + "."  + image_format}? [y/n] ")

    if response.lower() not in ["y", "yes"]:
        sys.exit("Operation Cancelled.")
        
    n.save(f"{sys.argv[2] + "."  + image_format}")
