clc;close all

%%
Path_Working = 'E:\img_process\exp3\';
File = 'SnowWhite.jpg';
File = strcat(Path_Working,File);
I1 = imread(File);
figure('color','white','OuterPosition',[50,100,1200,600]);
subplot(121);imshow(I1,[]);title('original image');
subplot(122);imhist(I1);title('original histagram');

%%
x0 = 30; x1 = 120;
y0 = 50; y1 = 180;
figure; plot([0,x0,x1,255],[0,y0,y1,255]);
hold on;plot([x0,x1],[y0,y1],'o');

I1 = double(I1);
I2 = I1;

ind = find(I1 < x0);
I2(ind) = I1(ind)*y0/x0;

ind = find(I1 >= x0 & I1<x1);
I2(ind) = y0 +(I1(ind)-x0)*(y1-y0)/(x1-x0);

ind = find(I1>x1);
I2(ind) = y1 +(I1(ind)-x1)*(255-y1)/(255-x1);
figure('color','white','OuterPosition',[50,100,1200,600]);
subplot(121);imshow(I2,[]);title('mapped image');
subplot(122);imhist(uint8(I2));title('mapped histagram');

%%
I3 = histeq(uint8(I1));
figure('color','white','OuterPosition',[50,100,1200,600]);
subplot(121);imshow(I3,[]);title('equalized image');
subplot(122);imhist(I3);title('equalized histagram');

%%
File = strcat(Path_Working,'StarNight.jpg');
I_ref = imread(File);
figure('color','white','OuterPosition',[50,100,1200,600]);
subplot(121);imshow(I_ref);title('reference image');
subplot(122);imhist(I_ref);title('reference histagram');
%%
I4 = imhistmatch(uint8(I1),I_ref);
figure('color','white','OuterPosition',[50,100,1200,600]);
subplot(121);imshow(I4,[]);title('immatched image');
subplot(122);imhist(I4);title('immatched histagram');
%%
