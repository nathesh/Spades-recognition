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
  h = h.reshape((4,2))
  hnew = np.zeros((4,2),dtype = np.float32)

  add = h.sum(1)
  hnew[0] = h[np.argmin(add)]
  hnew[2] = h[np.argmax(add)]
   
  diff = np.diff(h,axis = 1)
  hnew[1] = h[np.argmin(diff)]
  hnew[3] = h[np.argmax(diff)]

  return hnew

###############################################################################
# Image Matching
###############################################################################
def preprocess(img):
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray,(5,5),2 )
  thresh = cv2.adaptiveThreshold(blur,255,1,1,11,1)
  return thresh
  
def imgdiff(img1,img2):
  img1 = cv2.GaussianBlur(img1,(5,5),5)
  img2 = cv2.GaussianBlur(img2,(5,5),5)    
  diff = cv2.absdiff(img1,img2)  
  diff = cv2.GaussianBlur(diff,(5,5),5)    
  flag, diff = cv2.threshold(diff, 200, 255, cv2.THRESH_BINARY) 
  return np.sum(diff)  

def find_closest_card(training,img):
  features = preprocess(img)
  return sorted(training.values(), key=lambda x:imgdiff(x[1],features))[0][0]
  
   
###############################################################################
# Card Extraction
###############################################################################  
def getCards(im, numcards=4):
  gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
  blur = cv2.GaussianBlur(gray,(1,1),1000)
  flag, thresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY) 
       
  contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

  contours = sorted(contours, key=cv2.contourArea,reverse=True)[:numcards]  

  for card in contours:
    peri = cv2.arcLength(card,True)
    approx = rectify(cv2.approxPolyDP(card,0.02*peri,True))

    # box = np.int0(approx)
    # cv2.drawContours(im,[box],0,(255,255,0),6)
    # imx = cv2.resize(im,(1000,600))
    # cv2.imshow('a',imx)      
    
    h = np.array([ [0,0],[449,0],[449,449],[0,449] ],np.float32)

    transform = cv2.getPerspectiveTransform(approx,h)
    warp = cv2.warpPerspective(im,transform,(450,450))
    
    yield warp
###############################################################################
# Get Training 
###############################################################################
def get_trained_dataset(training_file):
    with open(training_file, 'rb') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',')
      training = {}
      i = 0
      for row in spamreader:
        tuple_image = eval(row[0])
        image = cv2.imread("training/"+str(i)+".jpg")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        training[i] = (tuple_image,image)
        i += 1
      return training

if __name__ == '__main__':
    filename = "test/test_image.jpg"
    test_filename = "training/trained.csv"
    num_cards = 1
    im = cv2.imread(filename)
    width = im.shape[0]
    height = im.shape[1]
    if width < height:
      im = cv2.transpose(im)
      im = cv2.flip(im,1)

    # Debug: uncomment to see registered images
    # for i,c in enumerate(getCards(im,num_cards)):
    #   card = find_closest_card(training,c,)
    #   cv2.imshow(str(card),c)
    # cv2.waitKey(0) 
    training = get_trained_dataset(test_filename)
    cards = [find_closest_card(training,c) for c in getCards(im,num_cards)]
    print cards
