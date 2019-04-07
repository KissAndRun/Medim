clear all

%%
Path_Working = 'E:\img_process\exp2\';
File_DCM = 'CT159.dcm';

File = strcat(Path_Working,File_DCM);
I0 = dicomread(File);

figure;imagesc(I0);
colormap(gray);

[m,n]=size(I0);

I_add = zeros(m,n);
for ii = 1:10
    I_noise = rand(m,n);
    I1 = double(I0)+500 * I_noise;
    if ii <= 3
        figure; imagesc(I1);
        colormap(gray);
        title(strcat('Noisy image',num2str(ii)));
    end
    I_add = I_add + 1;
end
%figure;imagesc

%%
File = 'Tshirt1.jpeg';
File_path = strcat(Path_Working,File);
I1 = imread(File_path);
I1 = rgb2gray(I1);
figure;
subplot(121)
imshow(I1,[]);title('Image');

F1= fft2(I1);
F1 = fftshift(F1);
absF1 = abs(F1);
subplot(122)
imshow(log(absF1+1),[]);title('logFFT1');

%%
File = 'Tshirt2.jpeg';
File_path = strcat(Path_Working,File);
I2 = imread(File_path);
I2 = rgb2gray(I2);
figure;
subplot(121)
imshow(I2,[]);title('Image');

F2= fft2(I2);
F2 = fftshift(F2);
absF2 = abs(F2);
subplot(122)
imshow(log(absF2+1),[]);title('logFFT2');

%%
I3 = imrotate(I1,30);
figure;
subplot(121)
imshow(I3,[]);title('Image');

F3= fft2(I3);
F3 = fftshift(F3);
absF3 = abs(F3);
subplot(122)
imshow(log(absF3+1),[]);title('logFFT3');

%%
File = 'BBB.jpg';
File_path = strcat(Path_Working,File);
I4 = imread(File_path);
I4 = rgb2gray(I4);
figure;
imshow(I4,[]);title('Image');

[m,n]=size(I4);
I4_xiao = imresize(I4,[m/4,n/4]);
imshow(I4_xiao,[]);title('Image');

I4_1 = imresize(I4_xiao,[m,n],'nearest');
I4_2 = imresize(I4_xiao,[m,n],'bilinear');
I4_3 = imresize(I4_xiao,[m,n],'bicubic');
figure
subplot(231);imshow(I4);title('Original');
subplot(232);imshow(I4_xiao);title('down_sample');
subplot(233);imshow(I4_1);title('nearest');
subplot(234);imshow(I4_2);title('bilinear');
subplot(235);imshow(I4_3);title('bicubic');
%%
[cA1,cH1,cV1,cD1] = dwt2(I0,'db1');
dec2d = [cA1,cH1,cV1,cD1];
figure;imagesc(dec2d);colormap(gray);