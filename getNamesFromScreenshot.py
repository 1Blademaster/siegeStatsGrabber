import cv2
import pytesseract as tes

def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def getPlayersInLobby(image, f=False):
	if f:
		img = cv2.imread(image)
	else:
		img = image

	friendly = img[365:565, 467:900]
	enemy = img[595:790, 467:900]

	friendly1 = thresholding(grayscale(friendly))
	enemy1 = thresholding(grayscale(enemy))

	friendly2 = grayscale(friendly)
	enemy2 = grayscale(enemy)

	# cv2.imwrite('friendly.png', friendly)
	# cv2.imwrite('enemy.png', enemy)

	f1 = list(filter(lambda x: x, tes.image_to_string(friendly1, lang='eng').strip().split('\n')))
	e1 = list(filter(lambda x: x, tes.image_to_string(enemy1, lang='eng').strip().split('\n')))

	f2 = list(filter(lambda x: x, tes.image_to_string(friendly2, lang='eng').strip().split('\n')))
	e2 = list(filter(lambda x: x, tes.image_to_string(enemy2, lang='eng').strip().split('\n')))

	# print(f1)
	# print(f2)
	# print('\n - \n')
	# print(e1)
	# print(e2)

	f = []
	e = []

	if len(f1) == len(f2):
		for i in range(len(f1)):
			if f1[i] == f2[i]:
				f.append(f1[i])
			elif len(f1[i].split()) > 1 and len(f2[i].split()) == 1:
				f.append(f2[i])
			elif len(f1[i].split()) == 1 and len(f2[i].split()) > 1:
				f.append(f1[i])
		
		print(f)
	else:
		print('Lengths of friendly lists are not equal.')

	if len(e1) == len(e2):
		for i in range(len(e1)):
			if e1[i] == e2[i]:
				e.append(e1[i])
			elif len(e1[i].split()) > 1 and len(e2[i].split()) == 1:
				e.append(e2[i])
			elif len(e1[i].split()) == 1 and len(e2[i].split()) > 1:
				e.append(e1[i])

		print(e)
	else:
		print('Lengths of enemy lists are not equal.')

	return f, e