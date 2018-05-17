#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 16 10:26:17 2018

@author: piperkeyes
"""
import tensorflow as tf
#from tf_utils import load_dataset, random_mini_batches, convert_to_one_hot, predict
from tensorflow.python.framework import ops
import matplotlib.pyplot as plt
import numpy as np
import pkmn_load_data as pkmn_data
from sklearn.utils import shuffle
from utilities import predict

#import data
X, Y = pkmn_data.load_pkmn_data(4000)
X = X/255
X_pred = X[:,0:1]
#Y = Y.T

##Remove cards with no HP from dataset
#for label in range(len(Y[0])):
#    if np.isnan(Y[0][label]):
#        Y[0][label] = 0
#    
#Randomize X and Y matrices
X_shuffled, Y_shuffled = shuffle(X.T, Y.T)
X_shuffled = X_shuffled.T
Y_shuffled = Y_shuffled.T

#Divide X and Y into train and dev groups
train_end_index = int(0.8 * X_shuffled.shape[1]) #use 80% of data for train
X_train = X_shuffled[:,:train_end_index]
X_dev = X_shuffled[:,train_end_index:]
n_x = X_train.shape[0]
Y_train = Y_shuffled[:,:train_end_index]
Y_dev = Y_shuffled[:,train_end_index:]
n_y = 1

def create_placeholders(n_x, n_y):
    X = tf.placeholder(tf.float32, shape = (n_x, None), name = 'X')
    Y = tf.placeholder(tf.float32, shape = (n_y, None), name = 'Y')
    return X, Y

def initialize_parameters(n_x):
    W1 = tf.get_variable('W1', [512, n_x], initializer = tf.contrib.layers.xavier_initializer())
    b1 = tf.get_variable('b1', [512, 1], initializer = tf.zeros_initializer())
    W2 = tf.get_variable('W2', [512, 512], initializer = tf.contrib.layers.xavier_initializer())
    b2 = tf.get_variable('b2', [512, 1], initializer = tf.zeros_initializer())
    W3 = tf.get_variable('W3', [256, 512], initializer = tf.contrib.layers.xavier_initializer())
    b3 = tf.get_variable('b3', [256, 1], initializer = tf.zeros_initializer())
    W4 = tf.get_variable('W4', [128, 256], initializer = tf.contrib.layers.xavier_initializer())
    b4 = tf.get_variable('b4', [128, 1], initializer = tf.zeros_initializer())
    W5 = tf.get_variable('W5', [1, 128], initializer = tf.contrib.layers.xavier_initializer())
    b5 = tf.get_variable('b5', [1, 1], initializer = tf.zeros_initializer())
    
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2,
                  "W3": W3,
                  "b3": b3,
                  "W4": W4,
                  "b4": b4,
                  "W5": W5,
                  "b5": b5}
    
    return parameters

def forward_propogation(X, parameters):
    W1 = parameters['W1']
    b1 = parameters['b1']
    W2 = parameters['W2']
    b2 = parameters['b2']
    W3 = parameters['W3']
    b3 = parameters['b3']
    W4 = parameters['W4']
    b4 = parameters['b4']
    W5 = parameters['W5']
    b5 = parameters['b5']
    
    #perform linear -> relu until generating Z matrix of output layer
    Z1 = tf.matmul(W1, X) + b1
    A1 = tf.nn.relu(Z1)
    Z2 = tf.matmul(W2, A1) + b2
    A2 = tf.nn.relu(Z2)
    Z3 = tf.matmul(W3, A2) + b3
    A3 = tf.nn.relu(Z3)
    Z4 = tf.matmul(W4, A3) + b4
    A4 = tf.nn.relu(Z4)
    Z5 = tf.matmul(W5, A4) + b5
    
    return Z5

def compute_cost(Z5, Y):    
    cost = tf.reduce_mean(tf.squared_difference(Z5, Y))
    
    return cost

def model(X_train, Y_train, X_dev, Y_dev, learning_rate = 0.0005, num_epochs = 150,  print_cost = True):
    ops.reset_default_graph()
    (n_x, m) = X_train.shape
    n_y = Y_train.shape[0]
    costs = []
    
    #Create placeholders
    X, Y = create_placeholders(n_x, n_y)
    
    #Initialize params
    parameters = initialize_parameters(n_x)
    
    #Run forward prop
    Z5 = forward_propogation(X, parameters)
    
    #compute cost
    cost = compute_cost(Z5, Y)
    
    #Run back prop
    optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
    
    #Initialize all variables
    init = tf.global_variables_initializer()
    
    #Start session
    with tf.Session() as sess:
        sess.run(init)
        
        for epoch in range(num_epochs):
            epoch_cost = 0
            
            #TODO: implement minibatches
            
            _ , curr_cost = sess.run([optimizer, cost], feed_dict = {X: X_train, Y:Y_train})
            epoch_cost += curr_cost
            
            # Print the cost every epoch
            if print_cost == True and epoch % 1 == 0:
                print ("Cost after epoch %i: %f" % (epoch, epoch_cost))
            if print_cost == True and epoch % 5 == 0:
                costs.append(epoch_cost)
        
        #Plot cost
        plt.plot(np.squeeze(costs))
        plt.ylabel('cost')
        plt.xlabel('iterations (per tens)')
        plt.title("Learning rate =" + str(learning_rate))
        plt.show()
        
        #Save trained parameters
        parameters = sess.run(parameters)
        print ("Parameters have been trained!")

        # Calculate the correct predictions
        correct_prediction = tf.equal(Z5, Y)

        # Calculate accuracy on the dev set
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

        print ("Train Accuracy:", accuracy.eval({X: X_train, Y: Y_train}))
        print ("Dev Accuracy:", accuracy.eval({X: X_dev, Y: Y_dev}))
        
        return parameters
    
    
if __name__ == "__main__":
    params = model(X_train, Y_train, X_dev, Y_dev, learning_rate = 0.0005, num_epochs = 100,  print_cost = True)
    prediction = predict(X_pred, params)
    print("predicted value is " + str(prediction))