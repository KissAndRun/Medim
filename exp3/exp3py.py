import matplotlib.pyplot as plt
import numpy as np
import cv2
from histmatch import hist_match

Path_Working = './'
File_img = 'SnowWhite.jpg'
File = Path_Working + File_img
I0_origin = cv2.imread(File)
I0 = cv2.cvtColor(I0_origin, cv2.COLOR_BGR2GRAY)

plt.figure("Histogram")
plt.subplot(121),plt.imshow(I0,cmap='gray')
plt.subplot(122),plt.hist(np.array(I0).flatten(),bins=256)
plt.show()

x0 = 30.0
x1 = 120.0
y0 = 50.0
y1 = 180.0
x = [0, x0, x1, 255]
y = [0, y0, y1, 255]
plt.plot(x,y)
plt.plot([x0,x1],[y0,y1],'o')
plt.show()

I1_0 = np.where(I0<x0, I0*y0/x0 ,0)
I1_1 = np.where((I0>=x0)&(I0<x1),y0+(I0-x0)*(y1-y0)/(x1-x0), 0)
I1_2 = np.where(I0>x1, y1+(I0-x1)*(255-y1)/(255-x1), 0)
I1 = I1_0+I1_1+I1_2
print(I1)

plt.subplot(121),plt.imshow(I1, cmap='gray'),plt.title("after")
plt.subplot(122),plt.hist(np.array(I1).flatten(),bins=256)
plt.show()

I2 = cv2.equalizeHist(I0)
plt.subplot(121),plt.imshow(I2, cmap='gray'),plt.title("after")
plt.subplot(122),plt.hist(np.array(I2).flatten(),bins=256)
plt.show()


File_img = 'StarNight.jpg'
File = Path_Working + File_img
I_ref = cv2.imread(File)
I_ref = cv2.cvtColor(I_ref, cv2.COLOR_BGR2GRAY)
plt.subplot(121),plt.imshow(I_ref,cmap='gray')
plt.subplot(122),plt.hist(np.array(I_ref).flatten(),bins=256)
plt.show()

I3 = hist_match(I0,I_ref)
plt.subplot(121),plt.imshow(I3,cmap='gray')
plt.subplot(122),plt.hist(np.array(I3).flatten(),bins=256)
plt.show()
