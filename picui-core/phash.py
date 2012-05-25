import Image
from bitarray import bitarray

class ImageHash(object):
	def __init__(self, path, size=8):
		self.image_path = path
		self.hash_size = size
		self.image = Image.open(path)

	def average_hash(self):
		image = self.image.resize((self.hash_size, self.hash_size), Image.NEAREST).convert("L")
		pixels = list(image.getdata())
		avg = sum(pixels) / len(pixels)
		diff = []
		for pixel in pixels:
			value = 1 if pixel > avg else 0
			diff.append(str(value))

		ba = bitarray("".join(diff), endian="little")
		return ba.tobytes().encode('hex')

	def dct_hash(self):
		image = self.image.resize((32,32), Image.NEAREST).convert("L")
		pixels = list(image.getdata())
		reduced = []
		for i in range(0,64):
			reduced.append(pixels[i])

		avg = (sum(reduced) - reduced[0]) / len(reduced)
		diff = []

		for pixel in reduced:
			value = 1 if pixel > avg else 0
			diff.append(str(value))

		ba = bitarray("".join(diff), endian="little")
		return ba.tobytes().encode('hex')


def hamming_distance(image1, image2): #image1 and image2 are two bitarrays encoded in hex
	dist = 0
	for i in range(0, len(image1)):
		if (image1[i] == image2[i]):
			pass
		else:
			dist += 1
	return dist

if __name__ == "__main__":
	print "STARTING"
	hash1 = ImageHash('obama1.jpg').dct_hash()
	hash2 = ImageHash('pp.png').dct_hash()
	print hash1
	print hash2
	print hamming_distance(hash1,hash2)