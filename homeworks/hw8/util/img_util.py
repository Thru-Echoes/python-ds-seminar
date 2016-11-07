import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import warnings
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import joblib
import skimage
from skimage import io
from skimage.util.shape import view_as_windows
from skimage.util.montage import montage2d
from scipy.cluster.vq import kmeans2
from skimage.transform import resize
from skimage.filters import threshold_mean
from skimage.color import rgb2gray
from skimage.exposure import equalize_hist
from multiprocessing import Pool, cpu_count
from time import time

import os

def getWorkDir():
    return os.getcwd()

def setWorkDir(newPath):
    os.chdir(newPath)
    print("\nNew working directory: ", os.getcwd())
    return True
   
getWorkDir()  
setWorkDir(os.path.join(os.getcwd(), 'Documents/berkeley-courses/second-year/fall16/python-ds-seminar/homeworks/hw7'))


############################################################### 
############################################################### 
############################################################### 

# Image ploting function
def show_images(images, titles = None, interpolation = 'nearest'):
    """Display a list of images"""
    n_ims = len(images)
    if titles is None: titles = ['(%d)' % i for i in range(1, n_ims + 1)]
    fig = plt.figure()
    n = 1
    for image, title in zip(images, titles):
        a = fig.add_subplot(1 ,n_ims, n)
        if image.ndim == 2: plt.gray()
        plt.imshow(image, interpolation = interpolation)
        a.set_title(title)
        n += 1
    fig.set_size_inches(np.array(fig.get_size_inches()) * n_ims)
    plt.show()

def set_img_dict(is_sample = False):
    
    #Generates a {name : index} dictionary for each of the image categories.
      
    if is_sample:
        path = os.path.join(os.getcwd(), 'sample_img/') 
    else:
        path = os.path.join(os.getcwd(), '50_categories/')
    
    categories = []
    index = 0
    img_types = {}
    
    img_type_names = os.listdir(path)
    img_type_names.sort()
    
    for direc in img_type_names:
        if direc.startswith('.') == False:
            index = index + 1
            img_types[direc] = [index]
            
    return(img_types)

def montage_wb_ratio(input_image, patch_shape, n_filters, ele_print = False):

    patches = view_as_windows(input_image, patch_shape)
    patches = patches.reshape(-1, patch_shape[0] * patch_shape[1])[::8]
    fb, _ = kmeans2(patches, n_filters, minit = 'random')
    fb = fb.reshape((-1,) + patch_shape)
    fb_montage = montage2d(fb, fill = False, rescale_intensity = True)
    shape_var = np.ceil(np.sqrt(n_filters))
    elements = np.split(np.hstack(np.split(fb_montage, shape_var)), shape_var**2, axis = 1)
    del elements[n_filters:]
    wb_ratios = []
    bin_elements = []
    
    for element in elements:
        thresh = threshold_mean(element)
        binary = element > thresh
        ratio = np.sum(binary) / binary.size
        wb_ratios.append(ratio)
        
        if ele_print:
            bin_elements.append(binary)

    wb_ratios = sorted(wb_ratios, reverse = True)
    
    if ele_print:
        show_images(elements)
        show_images(bin_elements)
    
    return(wb_ratios)

def get_rgb_summary(img):

    print("\nWithin get_rgb_summary function...")
    print("img.shape(): ", img.shape())
    print("\n")

    img_r = img[:, :, 0]
    img_g = img[:, :, 1]
    img_b = img[:, :, 2]
    
    r_mean = np.mean(img_r)
    r_median = np.median(img_r)
    r_std = np.std(img_r)
    r_var = np.var(img_r)
    
    g_mean = np.mean(img_g)
    g_median = np.median(img_g)
    g_std = np.std(img_g)
    g_var = np.var(img_g)
    
    b_mean = np.mean(img_b)
    b_median = np.median(img_b)
    b_std = np.std(img_b)
    b_var = np.var(img_b)
    
    return list([r_mean, r_median, r_std, r_var, g_mean, g_median, g_std, g_var, b_mean, b_median, b_std, b_var])

# FUNCTION DEFINITIONS
# Quick function to divide up a large list into multiple small lists, 
# attempting to keep them all the same size. 
def split_seq(seq, size):
    newseq = []
    splitsize = 1.0 / size * len(seq)
    for i in range(size):
        newseq.append(seq[int(round(i * splitsize)):int(round((i + 1) * splitsize))])
    return newseq

def preprocess(input_image):
    gray = rgb2gray(input_image)
    hist = equalize_hist(gray)
    return hist

def extract_features(image_path_list):
    
    feature_list = []
    
    for image_path in image_path_list:
        one_row = []
        category = image_path.split('/')[-2]
        one_row.extend([image_path, category])
        image_array = io.imread(image_path)
        processed_image = preprocess(image_array)
        
        ##############
        
        #with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = montage_wb_ratio(processed_image, (8, 8), 25, ele_print = False)
        
        #get RGB summary stats 
        rgb_summary = get_rgb_summary(image_array)
        
        #concatenate features
        wb_and_rgb = wb + rgb_summary

        #one_row.extend(wb)
        one_row.extend(wb_and_rgb)
        feature_list.append(one_row)
        
    return feature_list

def new_data_read(image_path):
    image_array = io.imread('test6.jpg')
    processed_image = preprocess(image_array)
    warnings.simplefilter("ignore")
    wb = montage_wb_ratio(processed_image, (8, 8), 25, ele_print = False)
    return wb
 
 
############################################################### 
############################################################### 
############################################################### 
    
def get_data_feat(is_sample = False):

    MYDIRECTORY = os.getcwd()
    
    if is_sample:
        categories = os.listdir(MYDIRECTORY + '/sample_img')
    else:
        categories = os.listdir(MYDIRECTORY + '/50_categories')
    image_paths = []

    for category in categories:
        if not category.startswith('.'):
            if is_sample:
                image_names = os.listdir(MYDIRECTORY + "/sample_img/" + category)
            else:
                image_names = os.listdir(MYDIRECTORY + "/50_categories/" + category)
                
            for name in image_names:
                if is_sample:
                    image_paths.append(MYDIRECTORY + "/sample_img/" + category + "/" + name)
                else:
                    image_paths.append(MYDIRECTORY + "/50_categories/" + category + "/" + name)

    # Then, we run the feature extraction function using multiprocessing.Pool so 
    # so that we can parallelize the process and run it much faster.
    numprocessors = cpu_count() 

    # We have to cut up the image_paths list into the number of processes we want to
    # run. 
    split_image_paths = split_seq(image_paths, numprocessors)

    # Ok, this block is where the parallel code runs. We time it so we can get a 
    # feel for the speed up.
    start_time = time()
    p = Pool(numprocessors)
    result = p.map_async(extract_features, split_image_paths)
    poolresult = result.get()
    end_time = time()
    
    # All done, print timing results.
    print ("Finished extracting features. Total time: " + 
        str(round(end_time-start_time, 3)) + " s, or " + 
        str(round((end_time-start_time) / len(image_paths), 5)) + " s/image.")

    # To tidy-up a bit, we loop through the poolresult to create a final list of
    # the feature extraction results for all images.
    combined_result = []
    for single_proc_result in poolresult:
        for single_image_result in single_proc_result:
            combined_result.append(single_image_result)
            
    if is_sample: 
        cate = set_img_dict(is_sample = True) 
    else:
        cate = set_img_dict(is_sample = False)
        
    combined_result = np.array(combined_result)
    X = combined_result[:, 2:]
    Y = combined_result[:, 1]
    for i in range(len(Y)):
        Y[i] = cate[Y[i]][0]
    return X, Y
    
  
############################################################### 
############################################################### 
############################################################### 
  
    
def model_fitting(X, Y, dump_file = 'model.p'):
    grid_models = GridSearchCV(RandomForestClassifier(),
                       {'n_estimators':range(200, 1000, 100)}, n_jobs = 8, cv = 10)
    fit_models = grid_models.fit(X, Y)
    return fit_models

def get_pickle_model(modelz, dump_file = 'model.p'):
    
    # Save out only best model 
    if dump_file:
        with open(dump_file, "wb") as fp:
            #joblib.dump(modelz.best_estimator_, fp, protocol = pickle.HIGHEST_PROTOCOL, compression = 9)
            joblib.dump(modelz.best_estimator_, fp, protocol = pickle.HIGHEST_PROTOCOL)
    return modelz.best_estimator_

def load_model(model_file = 'model.p'):
    with open(model_file, "rb") as fp:
        model_instance = joblib.load(fp)
    return model_instance


############################################################### 
############################################################### 
###############################################################

#X, Y = get_data_feat(is_sample = True)
X, Y = get_data_feat(is_sample = False)

#sample_fits = model_fitting(X, Y, dump_file = 'model.p')
#pickle_model = get_pickle_model(sample_fits, dump_file = 'model.p')
fitted_models = model_fitting(X, Y, dump_file = 'model.p')
pickle_model = get_pickle_model(fitted_models, dump_file = 'model.p')