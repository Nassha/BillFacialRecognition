import face_recognition
import argparse
import pickle
import cv2


# load the trained faces through pickle. , I only used 17 image for my training set image
print("loading encodings...")
data = pickle.loads(open("encodings.pickle", "rb").read())

# load the input image and convert it from BGR to RGB
image = cv2.imread("examples/MoneySample4.jpg" )
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# detect the (x, y)-coordinates of the bounding boxes corresponding
# to each face in the input image, then compute the facial embeddings
# for each face
print("wait as we recognize faces...")
boxes = face_recognition.face_locations(rgb,
	model="cnn")
encodings = face_recognition.face_encodings(rgb, boxes)

# initialize the list of names for each face detected
names = []

# loop over the facial embeddings
for encoding in encodings:
	# attempt to match each face in the input image to our known
	# encodings
	matches = face_recognition.compare_faces(data["encodings"],
		encoding)
	name = "Unknown"


	# check to see if we have found a match
	if True in matches:
		# find the indexes of all matched faces then initialize a
		# dictionary to count the total number of times each face
		# was matched
		matchedIdxs = [i for (i, b) in enumerate(matches) if b]
		counts = {}

		# loop over the matched indexes and maintain a count for
		# each recognized face face
		for i in matchedIdxs:
			name = data["names"][i]
			counts[name] = counts.get(name, 0) + 1

		# determine the recognized face with the largest number of
		# votes (note: in the event of an unlikely tie Python will
		# select first entry in the dictionary)
		name = max(counts, key=counts.get)
	
	# update the list of names
	names.append(name)

# loop over the recognized faces

p500 = 0
p1000 = 0
pTotal = 0
for ((top, right, bottom, left), name) in zip(boxes, names):
        if name == "P500":
                if p500 % 2 == 0:
                        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                        pTotal = pTotal + int(name.split("P")[1])
                        y = top - 15 if top - 15 > 15 else top + 15
                        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)

                p500+=1
        elif name == "P1000":
                if p1000 % 3 == 0:
                        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                        pTotal = pTotal + int(name.split("P")[1])
                        y = top - 15 if top - 15 > 15 else top + 15
                        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
                p1000+=1
        else:
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
                pTotal = pTotal + int(name.split("P")[1])
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,0.75, (0, 255, 0), 2)
                

print("Total Peso amount: ", pTotal)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)

