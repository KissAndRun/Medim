clear all;close all;

%%
%Path_Working = 'E:\img_process\exp1\';
Path_Working = '.\';
File_img = 'lena.jpg';
File_DCM = 'CT159.dcm';

File = strcat(Path_Working,File_img);
I1 = imread(File);
imshow(I1);

imwrite(I1,strcat(Path_Working,'Q10.jpg'),'Quality',10);
imwrite(I1,strcat(Path_Working,'Q30.jpg'),'Quality',30);

%%
% Ô½°× Ô½¶à
figure('color','white'); imshow(I1(:,:,1),[]);title('R,channel')
figure('color','white'); imshow(I1(:,:,2),[]);title('G,channel')
figure('color','white'); imshow(I1(:,:,3),[]);title('B,channel')

figure('color','white'); 
for ii = 1:3
    subplot(1,3,ii)
    imhist(I1(:,:,ii));
    title(strcat('RGB Channel',num2str(ii)))
end

%%
File_Dicom = strcat(Path_Working,File_DCM);
I2 = dicomread(File_Dicom);
figure;imshow(I2,[]);
dicominfo(File_Dicom)

%%
I1_hsv = rgb2hsv(I1);
figure('color','white'); imshow(I1_hsv(:,:,1),[]);title('H,channel')
figure('color','white'); imshow(I1_hsv(:,:,2),[]);title('S,channel')
figure('color','white'); imshow(I1_hsv(:,:,3),[]);title('V,channel')

%%
cform = makecform('srgb2cmyk');
I1_cmyk = applycform(I1,cform);
figure('color','white'); imshow(I1_cmyk(:,:,1),[]);title('C,channel')
figure('color','white'); imshow(I1_cmyk(:,:,2),[]);title('M,channel')
figure('color','white'); imshow(I1_cmyk(:,:,3),[]);title('Y,channel')
figure('color','white'); imshow(I1_cmyk(:,:,4),[]);title('K,channel')
%%