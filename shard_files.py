# coding=utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from os import listdir, remove
from os.path import isfile, join
import os
import sys
import tarfile
import tempfile

from absl import app as absl_app
from absl import flags as absl_flags
import tensorflow as tf


directory = "/content/drive/My Drive/german-speechdata-package-v2/"
new_dir = "/content/drive/My Drive/TUDA/"


def shard_files():
 
    paths = ["test", "dev", "train"]
    
    for path in paths:

        folder = os.path.join(directory, path)
        exists = os.path.isdir(folder)

        if not exists:
            os.makedirs("/content/drive/My Drive/german-speechdata-package-v2/" + path+ "/text_files")
        text_dir = os.path.join(directory, path , "text_files")