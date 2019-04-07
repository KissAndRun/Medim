import matplotlib.pyplot as plt
import numpy as np
import cv2

Path_Working = './'
File_img = 'daheilou.jpg'
File = Path_Working + File_img
I0_origin = cv2.imread(File)
I0 = cv2.cvtColor(I0_origin, cv2.COLOR_BGR2GRAY)

plt.imshow(I0,cmap='gray'),plt.title('original image')
plt.show()

kernel_mean = np.ones((3,3), np.float32)/9
I1 = cv2.filter2D(I0, -1, kernel_mean)
kernel_mean = np.ones((21,21), np.float32)/(21*21)
I2 = cv2.filter2D(I0, -1, kernel_mean)

plt.subplot(121), plt.imshow(I1,cmap='gray'),plt.title('averaged image')
plt.subplot(122), plt.imshow(I2,cmap='gray'),plt.title('21 averaged image')
plt.show()

kernel_weighted = np.array([[1/16,2/16,1/16],
                            [2/16,4/16,2/16],
                            [1/16,2/16,1/16]], np.float32)

I3 = cv2.filter2D(I0, -1, kernel_weighted)
plt.subplot(121), plt.imshow(I3, cmap='gray'),plt.title('weighted image')
plt.subplot(122), plt.imshow(I3-I1, cmap='gray'),plt.title('weighted image')
plt.show()

I4 = cv2.medianBlur(I0, 3)
I5 = cv2.medianBlur(I0, 7)
plt.subplot(121), plt.imshow(I4, cmap='gray'),plt.title('3*3 median filter')
plt.subplot(122), plt.imshow(I5, cmap='gray'),plt.title('7*7 median filter')
plt.show()

H = np.array([[  0, -1,  0],
              [ -1,  5, -1],
              [  0, -1,  0]], np.float32)
I6 = cv2.filter2D(I0, -1, H)
plt.imshow(I6, cmap='gray'),plt.title('center sharpened filter')
plt.show()

H = np.array([[-1/3,-1/3,-1/3],
              [0,0,0],
              [1/3,1/3,1/3]], np.float32)
I7 = cv2.filter2D(I0, -1, H)
plt.subplot(121), plt.imshow(I7, cmap='gray'),plt.title('horiontal edge filter')
I8 = cv2.filter2D(I0, -1, H.T)
plt.subplot(122), plt.imshow(I8, cmap='gray'),plt.title('vertical edge filter')
plt.show()

f = np.fft.fft2(I0)
fshift = np.fft.fftshift(f)
magnitude_spectrum = np.log(np.abs(fshift)+1)
plt.imshow(magnitude_spectrum, cmap='gray'),plt.title('FFT')
plt.show()

Fstop = 10
sz = fshift.shape
o = [sz[0]/2,sz[1]/2]
Mask = np.ones(sz)
for ix in range(0,sz[0]):
    for iy in range(0,sz[1]):
        if np.sqrt(np.power((ix-o[0]),2)+np.power((iy-o[1]),2)) > np.power(Fstop,2):
            Mask[ix,iy] = 0
plt.subplot(121), plt.imshow(Mask,cmap='gray'),plt.title('Mask')
F2 = Mask*fshift
plt.subplot(122), plt.imshow(np.log(np.abs(F2)+1),cmap='gray'),plt.title('filter')
plt.show()

F3 = (1-Mask)*fshift
F2 = np.fft.ifftshift(F2)
F3 = np.fft.ifftshift(F3)
I9 = np.fft.ifft2(F2)
I10 = np.fft.ifft2(F3)
plt.subplot(121), plt.imshow(abs(I9),cmap='gray'),plt.title('inverse low pass FFT')
plt.subplot(122), plt.imshow(abs(I10),cmap='gray'),plt.title('inverse highl pass FFT')
plt.show()
