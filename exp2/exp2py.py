import cv2
import pywt
import numpy as np
import matplotlib.pyplot as plt
import SimpleITK as sitk

Path_Working = './'
File_DCM = 'CT159.dcm'

File = Path_Working + File_DCM
I0 = sitk.ReadImage(File)

I0_data = sitk.GetArrayFromImage(I0)

I_shape = I0_data.shape
I_add = np.zeros(I_shape)
for ii in range(1,11):
    I_noise = np.random.rand(I_shape[1],I_shape[2])
    I1 = I0_data + 500*I_noise
    if ii <=3 :
        I1_image = sitk.GetImageFromArray(I1)
        sitk.Show(I1_image)
    I_add = I_add + I1
I1 = sitk.GetImageFromArray(I_add/10)
sitk.Show(I1)

def show_fft(im, angle):
    File = Path_Working + im
    img = cv2.imread(File)
    I2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (h, w) = I2.shape[:2]
    center = (w/2, h/2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    I2_rotated = cv2.warpAffine(I2, M, (w, h))
    f = np.fft.fft2(I2_rotated)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = np.log(np.abs(fshift)+1)
    plt.subplot(1,2,1),plt.imshow(I2_rotated,cmap="gray")
    plt.title('input image by numpy'),plt.xticks([]),plt.yticks([])
    plt.subplot(1,2,2),plt.imshow(magnitude_spectrum,cmap="gray")
    plt.title('magnitude spectrum by numpy'),plt.xticks([]),plt.yticks([])
    plt.show()

show_fft('Tshirt1.jpeg',0)
show_fft('Tshirt2.jpeg',0)
show_fft('Tshirt2.jpeg',30.0)

File = 'BBB.jpg';
File = Path_Working + File
img = cv2.imread(File)
print(type(img))
I3 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(h, w) = I3.shape[:2]
I4 = cv2.resize(I3, (int(w / 4), int(h / 4)))
I5 = cv2.resize(I4, (w, h), interpolation=cv2.INTER_NEAREST)
I6 = cv2.resize(I4, (w, h), interpolation=cv2.INTER_LINEAR)
I7 = cv2.resize(I4, (w, h), interpolation=cv2.INTER_CUBIC)
plt.subplot(231),plt.imshow(I3,cmap="gray"),plt.title("Original")
plt.subplot(232),plt.imshow(I4,cmap="gray"),plt.title("Down Sample")
plt.subplot(233),plt.imshow(I5,cmap="gray"),plt.title("Nearest")
plt.subplot(234),plt.imshow(I6,cmap="gray"),plt.title("Linear")
plt.subplot(235),plt.imshow(I7,cmap="gray"),plt.title("Cubic")
plt.show()

coeffs = pywt.dwt2(I0_data[0], 'haar')
cA, (cH, cV, cD) = coeffs

AH = np.concatenate([cA, cH], axis=1)
VD = np.concatenate([cV, cD], axis=1)
img = np.concatenate([AH, VD], axis=0)

plt.imshow(img,cmap='gray')
plt.show()
