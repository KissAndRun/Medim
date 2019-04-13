import cv2
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

Path_Working = './'
File_DCM = 'image_52'

File = Path_Working + File_DCM
I = sitk.ReadImage(File, sitk.sitkFloat32)

I_data = sitk.GetArrayFromImage(I)
plt.imshow(I_data[0],cmap='gray')
plt.show()

# Sobel
I1 = sitk.SobelEdgeDetection(I)
I1_data = sitk.GetArrayFromImage(I1)
plt.imshow(I1_data[0],cmap='gray')
plt.show()

# prewitty
kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
img_prewittx = cv2.filter2D(I_data[0], -1, kernelx)
img_prewitty = cv2.filter2D(I_data[0], -1, kernely)
plt.imshow(np.sqrt(np.power(img_prewittx,2)+np.power(img_prewitty, 2)),cmap='gray')
plt.show()

# Roberts
kernelx = np.array([[1,0],[0,-1]])
kernely = np.array([[0,1],[-1,0]])
img_robertsx = cv2.filter2D(I_data[0], -1, kernelx)
img_robertsy = cv2.filter2D(I_data[0], -1, kernely)
plt.imshow(np.sqrt(np.power(img_robertsx,2)+np.power(img_robertsy, 2)),cmap='gray')
plt.show()

# LOG
I2 = cv2.GaussianBlur(I_data[0], (5,5), 0)
I3 = cv2.Laplacian(I2,cv2.CV_32F,5)
I3 = cv2.convertScaleAbs(I3)
plt.imshow(I3,cmap='gray')
plt.show()

TH1 = 20
TH2 = 180
I4 = np.where((I2>=TH1)&(I2<=TH2),1,0)
plt.imshow(I4,cmap='gray')
plt.show()

def RegionGrow(im_arr, seedlist, iter_num=5, multiplier=2.5, initialRadius=2, replaceValue=255):

    image = sitk.GetImageFromArray(im_arr)
    image = sitk.Cast(image, sitk.sitkFloat32)
    im_new = sitk.ConfidenceConnected(image, seedlist, iter_num, multiplier, initialRadius,replaceValue)
    im_out = sitk.GetArrayFromImage(im_new)
    return im_out

plt.imshow(I2,cmap='gray')
seed = plt.ginput(2)
seed = [[int(i[0]),int(i[1])] for i in seed]
plt.show()
I5 = RegionGrow(I2,seed, 5, 2, 2, 255)
plt.imshow(I5,cmap='gray')
plt.show()
