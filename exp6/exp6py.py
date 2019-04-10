import cv2
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk
import morphsnakes as ms
from skfuzzy.cluster import cmeans
from visual_callback_2d import visual_callback_2d

Path_Working = './'
File_DCM = 'slice_z74.dcm'

File = Path_Working + File_DCM
I = sitk.ReadImage(File, sitk.sitkFloat32)
I_data = sitk.GetArrayFromImage(I)
I0 = I_data[0]
plt.imshow(I0,cmap='gray'),plt.title('original image')
plt.show()

img1 = I0.reshape(I0.size,1)

# K-Means
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,10,1.0)
flags = cv2.KMEANS_RANDOM_CENTERS
compactness,labels,centers = cv2.kmeans(img1,4,None,criteria,10,flags)

I1 = labels.reshape(I0.shape)
plt.imshow(I1),plt.title('kmeans')
plt.show()

# Fuzzy CMeans
center, u, u0, d, jm, p, fpc = cmeans(img1.T, m=3, c=3, error=0.005, maxiter=1000)
Labels = np.zeros(I0.size)
for ii in range(0,I0.size):
    label = np.where(u[:,ii] == max(u[:,ii]))
    Labels[ii] = label[0]
I2 = Labels.reshape(I0.shape)
plt.imshow(I2),plt.title('cmeans')
plt.show()
#
WM = np.where(I1==I1[100,94],1.0,0)
plt.imshow(WM)
plt.show()
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
erosion = cv2.erode(WM,kernel,iterations = 1)
dilation = cv2.dilate(WM,kernel,iterations = 1)
opening = cv2.morphologyEx(WM, cv2.MORPH_OPEN, kernel)
closing = cv2.morphologyEx(WM, cv2.MORPH_CLOSE, kernel)
plt.subplot(221),plt.imshow(erosion,cmap='gray'),plt.title('erosion')
plt.subplot(222),plt.imshow(dilation,cmap='gray'),plt.title('dilate')
plt.subplot(223),plt.imshow(opening,cmap='gray'),plt.title('opening')
plt.subplot(224),plt.imshow(closing,cmap='gray'),plt.title('closing')
plt.show()


# WaterShed
feature_image = sitk.GradientMagnitude(I)
I3 = sitk.MorphologicalWatershed(
    feature_image,
    markWatershedLine=True,
    fullyConnected=False,
    level=100)
I3 = sitk.GetArrayFromImage(I3)
plt.imshow(I3[0])
plt.show()

# Snake
def find_contour(img):
    img = img/255
    gimg = ms.inverse_gaussian_gradient(img, alpha=1000, sigma=5.48)
    init_ls = ms.circle_level_set(img.shape, (100, 126), 20)
    callback = visual_callback_2d(img)
    ms.morphological_geodesic_active_contour(gimg, iterations=45,
                                             init_level_set=init_ls,
                                             smoothing=1, threshold=0.31,
                                             balloon=1, iter_callback=callback)
find_contour(I0)
