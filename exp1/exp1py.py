import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import SimpleITK as sitk

Path_Working = './'
File_img = 'lena.jpg'
File_DCM = 'CT159.dcm'

File = Path_Working + File_img
im = Image.open(File_img)
im.show()
im.save('Quality10_py.jpg','JPEG',quality=10)
im.save('Quality30_py.jpg','JPEG',quality=30)


r,g,b = im.split()
plt.figure("RGB mode")
plt.subplot(131)
plt.imshow(r,cmap="gray")
plt.subplot(132)
plt.imshow(g,cmap="gray")
plt.subplot(133)
plt.imshow(b,cmap="gray")
plt.show()


plt.figure("Histogram")
plt.hist(np.array(r).flatten(),bins=256,density=1,facecolor='red')
plt.hist(np.array(g).flatten(),bins=256,density=1,facecolor='green')
plt.hist(np.array(b).flatten(),bins=256,density=1,facecolor='blue')
plt.show()

imhsv = im.convert('HSV')
plt.figure("HSV mode")
h,s,v = imhsv.split()
plt.subplot(131)
plt.imshow(h,cmap="gray")
plt.subplot(132)
plt.imshow(s,cmap="gray")
plt.subplot(133)
plt.imshow(v,cmap="gray")
plt.show()

im_cmyk = im.convert('CMYK')
c,m,y,k = im_cmyk.split()
plt.figure("CMYK mode")
plt.subplot(141)
plt.imshow(c,cmap="gray")
plt.subplot(142)
plt.imshow(m,cmap="gray")
plt.subplot(143)
plt.imshow(y,cmap="gray")
plt.subplot(144)
plt.imshow(k,cmap="gray")
plt.show()

DicomFile = Path_Working + File_DCM
reader = sitk.ImageFileReader()
reader.SetFileName(DicomFile)
reader.ReadImageInformation()
for k in reader.GetMetaDataKeys():
    v = reader.GetMetaData(k)
    print("({0})==\"{1}\"".format(k,v))

image = reader.Execute()
sitk.Show(image)
