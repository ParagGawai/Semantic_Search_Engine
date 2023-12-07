from absl import logging

import tensorflow as tf

import tensorflow_hub as hub
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import re
import seaborn as sns

embed_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
embed = hub.load(embed_url)
embeddings = tf.make_ndarray(tf.make_tensor_proto(embed(["The quick brown fox jumps over the lazy dog."]))).tolist()[0]
# if we dont use tolist and ndarry and proto_tensor and all, it will return us the tf.tensor which we dont want, we want a list to pass it to the elastic search.


print(type(embeddings))
print(len(embeddings))    # see it is 512 dimensional vector
print(embeddings)


# after this code, our model is loaded into the memory (which is around 1 to 1.5GB), now we just have to pass the snetences and we get the 512d vectors.