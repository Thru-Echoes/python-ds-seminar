import numpy as np
import matplotlib.pyplot as plt
import skimage

from scipy.ndimage import convolve
from sklearn import linear_model, datasets, metrics
from sklearn.model_selection import train_test_split
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from skimage import data

# Taken from: 
# Scikit-learn example on Logistic Regression image processing 

def nudge_dataset(X, Y):
    """
    This produces a dataset 5 times bigger than the original one,
    by moving the 8x8 images in X around by 1px to left, right, down, up
    """
    direction_vectors = [
        [[0, 1, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [1, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 1],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 1, 0]]]

    shift = lambda x, w: convolve(x.reshape((8, 8)), mode='constant',
                                  weights=w).ravel()
    X = np.concatenate([X] +
                       [np.apply_along_axis(shift, 1, X, vector)
                        for vector in direction_vectors])
    Y = np.concatenate([Y for _ in range(5)], axis = 0)
    return X, Y

############################################################################
############################################################################
 
def show_images(images, titles = None):
    """Display a list of images"""
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1,n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image,title in zip(images, titles):
        a = fig.add_subplot(1,n_ims,n) # Make subplot
        if image.ndim == 2: # Is image grayscale?
            plt.gray() # Only place in this blog you can't replace 'gray' with 'grey'
        plt.imshow(image)
        a.set_title(title)
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show()
   
############################################################################
############################################################################
    
# Load Data
from skimage import io
from skimage import exposure, restoration
from skimage.color import rgb2gray

filename = os.path.join(os.getcwd(), 'sample_img/unicorn/unicorn_0004.jpg')
uniImg = io.imread(filename)
# uniImg.shape 
# (360, 480, 3)

def getRestoredImg(iimg):
    iimg_restore = restoration.denoise_bilateral(iimg)
    return iimg_restore

def getExposedImg(iimg, hEnhance = False):
    if hEnhance:
        iimg_equ = exposure.equalize_adapthist(iimg)
    else:
        iimg_equ = exposure.equalize_hist(iimg)
    return iimg_equ

uniImg_restore = getRestoredImg(uniImg)
uniImg_gray = rgb2gray(uniImg)
uniImg_equ = getExposedImg(uniImg, hEnhance = False)
uniImg_adapt = getExposedImg(uniImg, hEnhance = True)

show_images(images = [uniImg, uniImg_restore, uniImg, uniImg_gray, uniImg_equ, uniImg_adapt],
            titles = ["OG", "Restored", "Color", "Grayscale", "Hist Equal: normalized", "Hist Equal: adapt"]) 


############################################################################
############################################################################

X = np.asarray(uniImg, 'float32')
X, Y = nudge_dataset(X, uniImg)
X = (X - np.min(X, 0)) / (np.max(X, 0) + 0.0001)  # 0-1 scaling

X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
                                                    test_size=0.2,
                                                    random_state=0)

# Models we will use
logistic = linear_model.LogisticRegression()
rbm = BernoulliRBM(random_state=0, verbose=True)

classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])