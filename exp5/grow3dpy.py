import SimpleITK as sitk
import numpy as np

Path_Working = './'
File_img = 'YUCHANGHUA_Thrx_CT.mhd'
File = Path_Working + File_img
I = sitk.ReadImage(File)
I = sitk.DiscreteGaussian(I)
I = sitk.GetArrayFromImage(I)
Isizes = I.shape
J = np.zeros(Isizes)
x1 = 51
y1 = 111
z1 = 106
x2 = 34
y2 = 127
z2 = 243
threshold = 70
seedvalue = (I[x1, y1, z1]+I[x2, y2, z2])/2.
J[x1, y1, z1] = 1
J[x2, y2, z2] = 1

stack_init = 500000
stack = np.zeros((stack_init, 3))
stack[0, :] = [x1, y1, z1]
stack[1, :] = [x2, y2, z2]
stack_top = 1
numofpixel = 2

neigb = np.array([[-1, 0, 0], [1, 0, 0], [0, -1, 0],
                  [0, 1, 0], [0, 0, 1], [0, 0, -1]])

while stack_top != -1:
    x = stack[stack_top, 0]
    y = stack[stack_top, 1]
    z = stack[stack_top, 2]
    stack_top = stack_top - 1
    for j in range(6):
        xn = int(x + neigb[j, 0])
        yn = int(y + neigb[j, 1])
        zn = int(z + neigb[j, 2])

        ins = (xn >= 0 and yn >= 0 and zn >=
               0) and xn < Isizes[0] and yn < Isizes[1] and zn < Isizes[2]
        if (ins and int(J[xn, yn, zn]) == 0):
            isin = np.abs(I[xn, yn, zn]-seedvalue) < threshold
            if isin:
                stack_top = stack_top + 1
                stack[stack_top, :] = [xn, yn, zn]
                J[xn, yn, zn] = 1
                numofpixel = numofpixel + 1

print(numofpixel)
#out = sitk.GetImageFromArray(J)
# sitk.Show(out)
#sitk.WriteImage(out, "./Result.mhd")
mri = "./result.0.mhd"
mr = sitk.ReadImage(mri)
mr = sitk.GetArrayFromImage(mr)
mr_part = np.where(J == 1, mr, 0)
mean_of_mr = mr_part.sum()/numofpixel
print(mean_of_mr)
