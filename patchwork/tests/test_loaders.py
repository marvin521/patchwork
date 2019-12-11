# -*- coding: utf-8 -*-
import numpy as np
import tensorflow as tf
from patchwork.loaders import _image_file_dataset, dataset, stratified_training_dataset



def test_image_file_dataset(test_png_path):
    imfiles = [test_png_path]
    ds = _image_file_dataset(imfiles, imshape=(33,21),
                             norm=255, num_channels=3,
                             shuffle=False)
    for x in ds:
        x = x.numpy()
    
    assert isinstance(ds, tf.data.Dataset)
    assert isinstance(x, np.ndarray)
    assert x.max() <= 1
    assert x.min() >= 0
    assert x.shape == (33, 21, 3)



def test_dataset_without_augmentation(test_png_path):
    imfiles = [test_png_path]*10
    
    ds, ns = dataset(imfiles, ys=None, imshape=(11,17),
                     num_channels=3, norm=255,
                     batch_size=5, augment=False)
    
    for x in ds:
        x = x.numpy()
        break
    
    assert isinstance(ds, tf.data.Dataset)
    assert ns == 2
    assert x.shape == (5, 11, 17, 3)
    
    
def test_dataset_with_augmentation(test_png_path):
    imfiles = [test_png_path]*10
    
    ds, ns = dataset(imfiles, ys=None, imshape=(11,17),
                     num_channels=3, norm=255,
                     batch_size=5, augment={"rot90":False})
    
    for x in ds:
        x = x.numpy()
        break
    
    assert isinstance(ds, tf.data.Dataset)
    assert ns == 2
    assert x.shape == (5, 11, 17, 3)
    
    
def test_dataset_with_labels(test_png_path):
    imfiles = [test_png_path]*10
    labels = np.arange(10)
    
    ds, ns = dataset(imfiles, ys=labels, imshape=(11,17),
                     num_channels=3, norm=255,
                     batch_size=5, augment=False)
    
    for x,y in ds:
        x = x.numpy()
        y = y.numpy()
        break
    
    assert (y == np.arange(5)).all()
    
    
def test_dataset_with_unlabeled_images(test_png_path, test_tif_path):
    imfiles = [test_png_path]*10
    unlab_files = [test_tif_path]*15
    
    ds, ns = dataset(imfiles, unlab_fps=unlab_files, 
                     imshape=(11,17),
                     num_channels=3, norm=255,
                     batch_size=5, augment={"rot90":False})
    
    for x,y in ds:
        x = x.numpy()
        y = y.numpy()
        break
    
    assert x.shape == (5,11,17,3)
    assert y.shape == (5,11,17,3)
    
    
def test_dataset_with_both(test_png_path, test_tif_path):
    imfiles = [test_png_path]*10
    labels = np.arange(10)
    unlab_files = [test_tif_path]*15
    
    ds, ns = dataset(imfiles, ys=labels,
                     unlab_fps=unlab_files, 
                     imshape=(11,17),
                     num_channels=3, norm=255,
                     batch_size=5, augment={"rot90":False})
    
    for (w,x),(y,z) in ds:
        w = w.numpy()
        x = x.numpy()
        y = y.numpy()
        z = z.numpy()
        break
    
    assert w.shape == (5,11,17,3)
    assert x.shape == (5,11,17,3)
    assert y.shape == (5,)
    assert z.shape == (5,)
    
    
def test_stratified_training_dataset(test_png_path):
    imfiles = [test_png_path]*10
    labels = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    ds, ns = stratified_training_dataset(imfiles,
                                         labels, imshape=(13,11),
                                         num_channels=3,
                                         batch_size=10,
                                         mult=1,
                                         augment={"rot90":False})
    
    for x,y in ds:
        x = x.numpy()
        y = y.numpy()
        
    assert ns == 1
    # check to make sure it stratified correctly
    assert y.mean() == 0.5
    
    
    
    

    
    
    
    
    
    