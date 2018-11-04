# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 20:22:25 2018
@author: juliette
"""
import numpy as np
import cv2

class noisyImage :
    def __init__(self, path, file_name,                     # original image information
                 gauss_mu=0, gauss_sigma=0.3,               # default parameters for gaussian noise
                 sp_ratio=0.5, sp_amount=0.004,            # default parameters for salt and pepper noise
                 suppr_patch_size=10, suppr_patch_nb=1):    # default parameters for random patch suppression
        """ Create a class gathering all noisy version of an original image
        PARAMETERS
        path : path where is located the original image
        file_name : name of the original image
        gauss_mu : mean of gaussian noise
        gauss_sigma : variance of gaussian noise
        """
        
        self.method_nb = 5                      #How many denoising methods are available 
        self.Ilist = [None for i in range(self.method_nb)] #List of all available noisy images
        
        self.name = path+file_name
        self.Ioriginal = cv2.imread(self.name, 0)
        self.shape = (self.Ioriginal).shape
        self.size = (self.Ioriginal).size
    
        self.mu = gauss_mu
        self.sigma = gauss_sigma
        self.Igauss = np.empty(self.shape)

        self.s_vs_p = sp_ratio
        self.amount = sp_amount
        self.Isp = np.empty(self.shape)
        
        self.Ipoiss = np.empty(self.shape)
        
        self.Ispeckle = np.empty(self.shape)
        
        self.patch_size=suppr_patch_size
        self.patch_nb=suppr_patch_nb
        self.Isuppr = np.empty(self.shape)

        
    def add_gauss(self):
        """ Add gaussian noise to the original image """
        I_gauss = np.random.normal(self.mu, self.sigma, self.shape)
        I_gauss = self.Ioriginal+I_gauss
        I_gauss = (I_gauss-np.min(I_gauss))/(np.max(I_gauss)-np.min(I_gauss))
        self.Igauss = I_gauss
        self.Ilist[0] = I_gauss
        return()
    
    def salt_and_pepper(self):
        """ Apply salt and pepper noise on the original image """
        I_sp = np.copy(self.Ioriginal)
        # Salt mode
        num_salt = np.ceil(self.amount * self.size * self.s_vs_p)
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in self.shape]
        I_sp[coords] = 1
        # Pepper mode
        num_pepper = np.ceil(self.amount* self.size * (1. - self.s_vs_p))
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in self.shape]
        I_sp[coords] = 0
        self.Isp = I_sp
        self.Ilist[1]=self.Isp
        return()
        
    def poisson(self):
        """ Apply noise with poisson distribution on the original image """
        val = len(np.unique(self.Ioriginal))
        val = 2 ** np.ceil(np.log2(val))
        I_poisson = np.random.poisson(self.Ioriginal*val)/float(val)
        I_poisson = (I_poisson-np.min(I_poisson))/(np.max(I_poisson)-np.min(I_poisson))
        self.Ipoiss = I_poisson
        self.Ilist[2]=self.Ipoiss
        return()
    
    def speckle(self):
        """ Apply speckle noise on the original image """
        gauss = np.random.randn(self.shape[0],self.shape[1])      
        I_speckle = self.Ioriginal + self.Ioriginal * gauss
        I_speckle = (I_speckle-np.min(I_speckle))/(np.max(I_speckle)-np.min(I_speckle))
        self.Ispeckle =I_speckle
        self.Ilist[3]=self.Ispeckle
        return()
      
    def random_patch_suppression(self):
        """ Suppress random patch from the original image """
        I_lack=np.copy(self.Ioriginal)
        for i in range(self.patch_nb):
            x = np.random.randint(0,self.shape[0]-self.patch_size)
            y = np.random.randint(0,self.shape[1]-self.patch_size)
            I_lack[x:x+self.patch_size,y:y+self.patch_size]=255
        self.Isuppr = I_lack
        self.Ilist[4]=self.Isuppr
        return()
    
    def all_noise(self):
         """Apply all available noise methods on the original image """
         self.add_gauss()
         self.salt_and_pepper()
         self.poisson()
         self.speckle()
         self.random_patch_suppression()
         
    def show(self, I, title=''):
        """ Display the image I with window entitled 'title' """
        cv2.imshow(title, I)
        cv2.waitKey(0)
        cv2.destroyAllWindows() 
        
    def all_show(self):
         """Create and show all possible noise images """
         self.all_noise()
         print("Salt and Pepper noise")
         self.show(self.Isp, "Salt and Pepper noise")
         print("Speckle noise noise")
         self.show(self.Ispeckle, "Speckle noise noise")
         print("Poisson noise")
         self.show(self.Ipoiss, "Poisson noise")
         print("Gaussian additive noise")
         self.show(self.Igauss, "Gaussian additive noise")
         print("Missing part")
         self.show(self.Isuppr,"Missing part")



if (__name__ == "__main__"):
    path = "C://Users//juliette//Desktop//enpc//3A//Graphs_in_Machine_Learning//projet//images//"
    file_name ="lena.png"
    
    noise_class=noisyImage(path, file_name, 0.5, 0.1, 0.2, 0.3, 5, 3)
    noise_class.all_show()