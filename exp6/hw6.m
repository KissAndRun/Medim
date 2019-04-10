clc;clear;close all

Path = './';
File = strcat(Path,'slice_z74.dcm');
I = dicomread(File);
figure; imagesc(I);colormap(gray);axis off;axis equal;

%% k-means
sz = size(I);
n_pix = sz(1)*sz(2);
tic;
n_cluster = 5;
data = reshape(double(I),n_pix,1);
toc;
Labels = kmeans(data,n_cluster,'emptyaction','singleton');
toc;
KM_Seg = reshape(Labels,sz(1),sz(2));
figure;imagesc(KM_Seg);title('k-means result');axis off;axis equal;

%% FCM 
tic;
data = reshape(double(I),n_pix,1);
[centwe,U,obj_fcn] = fcm(data,n_cluster);
time = toc;
Labels = zeros(n_pix,1);
for ii = 1:n_pix
    Labels(ii) = find(U(:,ii) == max(U(:,ii)));
end
FCM_Seg = reshape(Labels,sz(1),sz(2));
figure;imagesc(FCM_Seg);title('FCM result');axis off;axis equal;
%%
WM = (KM_Seg ==KM_Seg(100,94));
se = strel('disk',3);
Seg_dilate = imdilate(WM,se);
Seg_erode = imerode(WM,se);
Seg_open = imopen(WM,se);
Seg_close = imclose(WM,se);
figure; 
subplot(2,2,1)
imagesc(Seg_dilate);colormap(gray);title('Original');axis off;axis equal;
subplot(2,2,2)
imagesc(Seg_erode);colormap(gray);title('Dilate');axis off;axis equal;
subplot(2,2,3)
imagesc(Seg_open);colormap(gray);title('Open');axis off;axis equal;
subplot(2,2,4)
imagesc(Seg_close);colormap(gray);title('Close');axis off;axis equal;

%%
WS_Seg= watershed(I);
figure;imagesc(WS_Seg);colormap(hsv);title('Watershed result');axis off;axis equal;
%%
n_iter = 300;
phi = snake(I,n_iter);
figure;imagesc(phi);colormap(gray);title('Sanke result');axis off;axis equal;
