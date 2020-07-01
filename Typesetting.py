from PIL import Image

# opens an image:
im = Image.open("img.jpg")
# creates a new empty image, RGB mode, and size 400 by 400.
new_im = Image.new('RGB', (6030, 3690))


# Here I resize my opened image, so it is no bigger than 100,100
# im.thumbnail((860, 1230))
im.resize((860, 1230))
# Iterate through a 4 by 4 grid with 100 spacing, to place my image
for i in range(0, 6020, 860):
    for j in range(0, 3690, 1230):
        # I change brightness of the images, just to emphasise they are unique copies.
        # im = Image.eval(im, lambda x: x + (i + j) / 30)
        # paste the image at location i,j:
        new_im.paste(im, (i, j))

new_im.show()
