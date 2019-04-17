clc;clear;close all;
Path = './';
%% 1.Load the CT 
File = strcat(Path,'CT159.dcm');
I = dicomread(File);figure; imagesc(I);colormap(gray);

% %% 2.Edge filtering
% Eg_Rob = edge(I,'roberts');
% Eg_Prw = edge(I,'prewitt');
% Eg_Sob = edge(I,'sobel');
% figure;subplot(2,2,1);
% imagesc(I);colormap(gray);title('Original');
% subplot(2,2,2);imagesc(Eg_Rob);colormap(gray);title('Roberts Edge');
% subplot(2,2,3);imagesc(Eg_Prw);colormap(gray);title('Prewitt Edge');
% subplot(2,2,4);imagesc(Eg_Sob);colormap(gray);title('Sobel Edge');
% 
% %% 3.Log fitering
% Eg_LOG = edge(I,'log');
% figure;imagesc(Eg_LOG);
% colormap(gray);title('LOG');
% 
% %% 4.Thresholding
% TH1 = 20; TH2 = 180;
% Seg_TH = (I>=TH1) & (I<=TH2);
% figure;imagesc(Seg_TH);colormap(gray);title('thresholding segmentation');

%% 5.Region growing
figure;imagesc(I);colormap(gray);
[seedy,seedx] = ginput(1);
colormap(gray);
Seg_RG = regiongrowing(double(I),round(seedx),round(seedy),33.0);
figure;imagesc(Seg_RG);colormap(gray);title('region grow segmentation');