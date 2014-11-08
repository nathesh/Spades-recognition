
import sys
import numpy as np
import cv2
import csv

###############################################################################
# Utility code from
# http://git.io/vGi60A
# Thanks to author of the sudoku example for the wonderful blog posts!
###############################################################################


def rectify(h):
    h = h.reshape((4, 2))
    hnew = np.zeros((4, 2), dtype=np.float32)

    add = h.sum(1)
    hnew[0] = h[np.argmin(add)]
    hnew[2] = h[np.argmax(add)]

    diff = np.diff(h, axis=1)
    hnew[1] = h[np.argmin(diff)]
    hnew[3] = h[np.argmax(diff)]

    return hnew


def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 2)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 1)
    return thresh

###############################################################################
# Card Extraction
###############################################################################


def getCards(im, numcards=4):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (1, 1), 1000)
    flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:numcards]

    for card in contours:
        peri = cv2.arcLength(card, True)
        approx = rectify(cv2.approxPolyDP(card, 0.02 * peri, True))

        # box = np.int0(approx)
        # cv2.drawContours(im,[box],0,(255,255,0),6)
        # imx = cv2.resize(im,(1000,600))
        # cv2.imshow('a',imx)

        h = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)

        transform = cv2.getPerspectiveTransform(approx, h)
        warp = cv2.warpPerspective(im, transform, (450, 450))

        yield warp


def get_training(training_labels_filename, training_image_filename, num_training_cards, avoid_cards=None):
    training = {}

    labels = {}
    for line in file(training_labels_filename):
        key, num, suit = line.strip().split()
        labels[int(key)] = (num, suit)

    print "Training"

    im = cv2.imread(training_image_filename)
    for i, c in enumerate(getCards(im, num_training_cards)):
        if avoid_cards is None or (labels[i][0] not in avoid_cards[0] and labels[i][1] not in avoid_cards[1]):
            training[i] = (labels[i], preprocess(c))

    print "Done training"
    return training


if __name__ == '__main__':
    training_image_filename = "training/train.png"
    training_labels_filename = "training/train.tsv"
    num_training_cards = 56

    training = get_training(
        training_labels_filename, training_image_filename, num_training_cards)
    f = open('training/train.csv', 'w')
    writer = csv.writer(f)
    for key in training:
        test = training[key]
        x, y = test[1].shape
        writer.writerow([test[0], [x, y], test[1].flatten()])
    f.close()
