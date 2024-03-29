from __future__ import generators, division, absolute_import, with_statement, print_function, unicode_literals

import numpy as np
import matplotlib.pyplot as plt
# from tensorflow.keras.datasets import mnist

from sklearn.model_selection import train_test_split

class Dataset(object):
	images_train = np.array([])
	images_test = np.array([])
	labels_train = np.array([])
	labels_test = np.array([])
	unique_train_label = np.array([])
	map_train_label_indices = dict()

	def _get_siamese_similar_pair(self):
		label =np.random.choice(self.unique_train_label)
		l, r = np.random.choice(self.map_train_label_indices[label], 2, replace=False)
		return l, r, 1

	def _get_siamese_dissimilar_pair(self):
		label_l, label_r = np.random.choice(self.unique_train_label, 2, replace=False)
		l = np.random.choice(self.map_train_label_indices[label_l])
		r = np.random.choice(self.map_train_label_indices[label_r])
		return l, r, 0

	def _get_siamese_pair(self):
		if np.random.random() < 0.5:
			return self._get_siamese_similar_pair()
		else:
			return self._get_siamese_dissimilar_pair()

	def get_siamese_batch(self, n):
		idxs_left, idxs_right, labels = [], [], []
		for _ in range(n):
			l, r, x = self._get_siamese_pair()
			idxs_left.append(l)
			idxs_right.append(r)
			labels.append(x)
		return self.images_train[idxs_left,:], self.images_train[idxs_right, :], np.expand_dims(labels, axis=1)

def _iter_loadtxt(filename, delimiter=',', skiprows=0, dtype=float):
    def iter_func():
        with open(filename, 'r') as infile:
            for _ in range(skiprows):
                next(infile)
            for line in infile:
                line = line.rstrip().split(delimiter)
                for item in line:
                    yield dtype(item)
        _iter_loadtxt.rowlength = len(line)

    data = np.fromiter(iter_func(), dtype=dtype)
    data = data.reshape((-1, _iter_loadtxt.rowlength))
    return data

class CarsDataset(Dataset):
    def __init__(self):
        print("===Loading Cars Dataset===")
        # load training images
        img_data = _iter_loadtxt('cars_dataset/images_train.csv')
#         np.genfromtxt('cars_dataset/images_train.csv', delimiter=',')
        label_data = np.genfromtxt(
            'cars_dataset/labels_train.csv', delimiter=',')

        self.images_train, self.images_test, self.labels_train, self.labels_test = train_test_split(
            img_data, label_data, test_size=0.25, random_state=42)

        self.images_train = self.images_train.reshape((6108, 40000, 3, )) / 255.0
        self.images_test = self.images_test.reshape((2036, 40000, 3)) / 255.0

        self.labels_train = np.expand_dims(self.labels_train, axis=1)
        self.unique_train_label = np.unique(self.labels_train)
        self.map_train_label_indices = {label: np.flatnonzero(
            self.labels_train == label) for label in self.unique_train_label}

        print("Images train :", self.images_train.shape)
        print("Labels train :", self.labels_train.shape)
        print("Images test  :", self.images_test.shape)
        print("Labels test  :", self.labels_test.shape)
        print("Unique label :", self.unique_train_label)
        
    
class MNISTDataset(Dataset):
	def __init__(self):
		print("===Loading MNIST Dataset===")
		(self.images_train, self.labels_train), (self.images_test, self.labels_test) = mnist.load_data()
		self.images_train = np.expand_dims(self.images_train, axis=3) / 255.0
		self.images_test = np.expand_dims(self.images_test, axis=3) / 255.0
		self.labels_train = np.expand_dims(self.labels_train, axis=1)
		self.unique_train_label = np.unique(self.labels_train)
		self.map_train_label_indices = {label: np.flatnonzero(self.labels_train == label) for label in self.unique_train_label}
		print("Images train :", self.images_train.shape)
		print("Labels train :", self.labels_train.shape)
		print("Images test  :", self.images_test.shape)
		print("Labels test  :", self.labels_test.shape)
		print("Unique label :", self.unique_train_label)
		# print("Map label indices:", self.map_train_label_indices)
		
if __name__ == "__main__":
	# Test if it can load the dataset properly or not. use the train.py to run the training
	a = CarsDataset()
	batch_size = 4
	ls, rs, xs = a.get_siamese_batch(batch_size)
	f, axarr = plt.subplots(batch_size, 2)
	for idx, (l, r, x) in enumerate(zip(ls, rs, xs)):
		print("Row", idx, "Label:", "similar" if x else "dissimilar")
		print("max:", np.squeeze(l, axis=2).max())
		axarr[idx, 0].imshow(np.squeeze(l, axis=2))
		axarr[idx, 1].imshow(np.squeeze(r, axis=2))
	plt.show()