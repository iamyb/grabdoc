#!/usr/bin/env python 
import os, time, cv2, sys, math
import tensorflow as tf
import numpy as np

cur_dirname = os.path.split(os.path.realpath(__file__))[0]
proj_root = os.path.split(cur_dirname)[0]
sys.path.append(proj_root)
sys.path.append(cur_dirname)

from ImageAdjust import ImageAdjust

##########################################################################################
def load_graph(frozen_graph_filename):
    # We load the protobuf file from the disk and parse it to retrieve the 
    # unserialized graph_def
    with tf.gfile.GFile(frozen_graph_filename, "rb") as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())

    # Then, we import the graph_def into a new Graph and returns it 
    with tf.Graph().as_default() as graph:
        # The name var will prefix every op/nodes in your graph
        # Since we load everything in a new graph, this is not needed
        tf.import_graph_def(graph_def, name="prefix")
    return graph

##########################################################################################
class DocSegModel():
    def __init__(self, size=512, dataset='pretrained', cpu=True):
        self.label_values = [[0],[255]]
        self.size = size
        num_classes = len(self.label_values)

        tf.reset_default_graph()
        config = tf.ConfigProto() 
        if cpu == True:
            config = tf.ConfigProto(device_count = {'GPU': 0})
        else:
            config.gpu_options.allow_growth = True
        graph = load_graph(os.path.join(proj_root, 'model', dataset, 'frozen_model.pb'))
        #graph = load_graph(os.path.join(proj_root, 'model', dataset, 'humanseg.pb'))
        self.sess = tf.Session(graph=graph, config=config)

    def predict(self, image, is_path=True):
        net_input = self.sess.graph.get_tensor_by_name('prefix/net_input:0')
        model = self.sess.graph.get_tensor_by_name('prefix/model:0')
        #net_input = self.sess.graph.get_tensor_by_name('prefix/Placeholder:0')
        #model = self.sess.graph.get_tensor_by_name('prefix/logits/BiasAdd:0')

        loaded =cv2.cvtColor(cv2.imread(image,-1),cv2.COLOR_BGR2RGB) if is_path else image

        img_adj = ImageAdjust(loaded, self.size)
        loaded_image = img_adj.resize(loaded)

        input_image = np.expand_dims(np.float32(loaded_image),axis=0)/255.0

        mask = self.sess.run(model, feed_dict={net_input:input_image})[0]    

        mask = np.argmax(mask, axis=-1)
        mask = np.array(self.label_values)[mask.astype(int)]

        mask = img_adj.recover(mask.astype(np.float32))
        ret_img = cv2.cvtColor(loaded, cv2.COLOR_BGR2BGRA)
        ret_img[:,:,-1] = mask 

        return mask, ret_img

