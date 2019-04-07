clear all

%% average smoothing filter
Path_Working = 'E:\img_process\exp4\';
File = 'daheilou.jpg';
File = strcat(Path_Working,File);
I1 = imread(File);
I1 = double(rgb2gray(I1));
figure;imshow(I1,[]);title('original image');

H = [[1/9,1/9,1/9];...
    [1/9,1/9,1/9];...
    [1/9,1/9,1/9]];
I2 = imfilter(I1,H);
figure;imshow(I2,[]);title('average image');
figure;imshow(imfilter(I1,ones(21,21)/21.^2),[]);title('21 order average image');

%% weighted smoothing filter
H = [[1/16,2/16,1/16];...
    [2/16,4/16,2/16];...
    [1/16,2/16,1/16]];
I3 = imfilter(I1,H);
figure;imagesc(I3);colormap(gray);title('weighted average image');
figure;imagesc(I3-I2);colormap(gray);title('weighted average image - average');
%%
I4_1 = medfilt2(I1,[3,3]);
I4_2 = medfilt2(I1,[7,7]);
figure
subplot(221);imagesc(I1);colormap(gray);title('original');
subplot(222);imagesc(I2);colormap(gray);title('average filter');
subplot(223);imagesc(I4_1);colormap(gray);title('3*3 median filter');
subplot(224);imagesc(I4_2);colormap(gray);title('7*7 median filter');

%% edge filter
H = [[-1./8,-1./8,-1./8];...
    [-1./8,1./8,-1./8];...
    [-1./8,-1./8,-1./8]];
I5 = imfilter(I1,H);
figure;imagesc(I5);colormap(gray);title('center sharpened filter');

H = [[-1./3,-1./3,-1./3];...
    [0,0,0];...
    [1./3,1./3,1./3]];
I6 = imfilter(I1,H);
figure;subplot(121);imagesc(I6);colormap(gray);title('horiontal edge filter');
subplot(122);imagesc(abs(I6));colormap(gray);title('abs');

I7 = imfilter(I1,H');
figure;subplot(121);imagesc(I7);colormap(gray);title('vertical edge filter');
subplot(122);imagesc(abs(I7));colormap(gray);title('abs');
%%
I8 = 1+abs(I5);
figure;imagesc(I8,[0,255]);colormap(gray);title('sharpening filter');
%%
F1 = fft2(I1);
F1 = fftshift(F1);
absF1 = abs(F1);
figure;imshow(log(absF1+1),[]);title('logFF1');
%%
Fstop = 10;
sz = size(F1);
o = sz/2;
Mask = ones(sz);
for ix = 1:sz(1)
    for iy = 1:sz(2)
        if sqrt((ix-o(1))^2+(iy-o(2))^2)> Fstop^2
            Mask(ix,iy) = 0;
        end
    end
end
%吉布斯振荡出现残影
figure;imshow(Mask,[]);title('Mask');
F2 = F1.*Mask;
figure;imshow(log(abs(F2)+1),[]);title('filter FFT');
F2 = ifftshift(F2);
I9 = ifft2(F2);
figure;imagesc(abs(I9));colormap(gray); title('inverse low pass FFT')

%%
F3 = F1.*(1-Mask);
figure;imshow(log(abs(F3)+1),[]);title('filter FFT');
F3 = ifftshift(F3);
I10 = ifft2(F3);
figure;imagesc(abs(I10));colormap(gray); title('inverse high pass FFT')
%%
