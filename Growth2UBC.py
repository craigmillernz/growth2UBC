# -*- coding: utf-8 -*-
"""
Created on Fri Nov 06 15:09:46 2015

@author: craig miller, c.miller@gns.cri.nz
Script to read the Growth2.0 MAT.DAT file and convert it to a UBC model format
Also creates the UBC mesh file.

These can be loaded into Mira Geoscience Analyst for viewing.
http://www.mirageoscience.com/our-products/software-product/geoscience-analyst

For a large model it may take a minute or so to run.
"""
from __future__ import print_function
import sys
import numpy as np
import pandas as pd

#The directory where the Growth2.0 Mat.dat file is stored
moddir = ('c:\your_working_dir')
matfile = 'MAT.DAT'

#read grid dimension info from file
mtx = pd.read_csv(moddir + "/" + matfile, skiprows=6, nrows=3, header=None,
                  delim_whitespace=True)
mtx=mtx.T

print ('Number of rows = ', int(mtx[1]))
#mtx=[69,61,38] #cols, rows, pages

#load file
a = np.loadtxt(moddir + "/" + matfile, skiprows=9)
a[a==9999]=0 #change 9999 to 0

a=a/1000 #convert to g/cc for UBC/VPMG

#create grid ranges to iterate over
#d0=np.linspace(2256,-1,38)  #this is correct
d0 = np.linspace(((int(mtx[1])*int(mtx[2]))-int(mtx[1])-1), -1, int(mtx[2]))
#d1 = np.linspace(0,68,69) #this is correct
d1 = np.linspace(0,int(mtx[0])-1, int(mtx[0]))

#recast as integers
d0 = d0.astype(int)
d1 = d1.astype(int)

#create empty list for storing result
ubc =[]

#iterate through file in z,e,n order, starting from top, southwest corner
d = 0
while d<=int(mtx[1])-1:#60
    print ('processing row ', d)    
    for col in d1:        
        for row in d0:  
            result = a[row,col]
            ubc = np.append(ubc, result)            
    d0=d0+1
    d=d+1
    

#save file
np.savetxt(moddir + '/ubc_mod.den', ubc, '%.3f')

#NOW MAKE THE ASSOCIATED MESH FILE
mesh = pd.read_csv(moddir + "/" + matfile, nrows=9, header=None,
                   delim_whitespace=True)
mesh = mesh.T

sys.stdout = open(moddir + '/ubc_mesh.mesh', 'w')

#fo = open(moddir + '/ubc_mesh.mesh', 'w')

print (int(mesh[6]), int(mesh[7]), int(mesh[8]), sep=' ')
print (int(mesh[0]), int(mesh[2]), int(mesh[5]), sep=' ')
print (int(mesh[6]),"*",(int(mesh[1])-int(mesh[0]))/int(mesh[6]-1), sep='')
print (int(mesh[7]),"*",(int(mesh[3])-int(mesh[2]))/int(mesh[7]-1), sep='')
print (int(mesh[8]),"*",(int(mesh[5])-int(mesh[4]))/int(mesh[8]-1), sep='')
#fo.close()

#sys.stdout.close()