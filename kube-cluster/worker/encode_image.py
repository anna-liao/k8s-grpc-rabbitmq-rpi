import base64

print("Load image obama.jpg")
img = open("obama.jpg", 'rb').read()
encoded_img = base64.b64encode(img).decode('utf-8')
print("Encoded image: {}".format(encoded_img))

print("Decoding img")
deser_image = base64.b64decode(encoded_img)
with open('deser_image.jpg', 'wb') as f:
	f.write(deser_image)
