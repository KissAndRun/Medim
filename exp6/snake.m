function phi=snake(I,iter)
%  This Matlab code demonstrates an edge-based active contour model as an application of 
%  the Distance Regularized Level Set Evolution (DRLSE) formulation in the following paper:
%
%  C. Li, C. Xu, C. Gui, M. D. Fox, "Distance Regularized Level Set Evolution and Its Application to Image Segmentation", 
%     IEEE Trans. Image Processing, vol. 19 (12), pp. 3243-3254, 2010.
%
% Author: Chunming Li, all rights reserved
% E-mail: lchunming@gmail.com   
%         li_chunming@hotmail.com 
% URL:  http://www.imagecomputing.org/~cmli//


Img=double(I);
Img = 255*(Img-min(Img(:)))/(max(Img(:))-min(Img(:)));
sz = size(Img);

%% parameter setting
timestep=1;  % time step
mu=0.2/timestep;  % coefficient of the distance regularization term R(phi)
iter_inner=5;
iter_outer=iter;
lambda=5; % coefficient of the weighted length term L(phi)
alfa=-3;  % coefficient of the weighted area term A(phi)
epsilon=1.5; % papramater that specifies the width of the DiracDelta function

sigma=.8;    % scale parameter in Gaussian kernel
G=fspecial('gaussian',15,sigma); % Caussian kernel
Img_smooth=conv2(Img,G,'same');  % smooth image by Gaussiin convolution
[Ix,Iy]=gradient(Img_smooth);
f=Ix.^2+Iy.^2;
g=1./(1+f);  % edge indicator function.

% initialize LSF as binary step function
c0=2;
initialLSF = c0*ones(size(Img));

h=figure;
imagesc(Img,[0, 255]); axis off; axis equal; colormap(gray); hold on;  
[x1,y1] = ginput(1);
[x2,y2] = ginput(1);

% generate the initial region R0 as two rectangles
initialLSF(round(y1):round(y2),round(x1):round(x2))=-c0; 
phi=initialLSF;
contour(phi, [0,0], 'r');
title('snake segmentation');
pause(0.5);

potential=2;  
if potential ==1
    potentialFunction = 'single-well';  % use single well potential p1(s)=0.5*(s-1)^2, which is good for region-based model 
elseif potential == 2
    potentialFunction = 'double-well';  % use double-well potential in Eq. (16), which is good for both edge and region based models
else
    potentialFunction = 'double-well';  % default choice of potential function
end  

% start level set evolution
for n=1:iter_outer
    phi = drlse_edge(phi, g, lambda, mu, alfa, epsilon, timestep, iter_inner, potentialFunction);    
   if mod(n,2)==0
        figure(h);
        imshow(Img,[ ]); axis off; axis equal;
        hold on;  contour(phi, [0,0], 'r');
        pause(0.1);
   end
end
