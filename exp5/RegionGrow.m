clc;clear;close all;
Path = './';
%% 1.Load the CT 
File = strcat(Path,'image_52');
I = double(dicomread(File));
figure; imagesc(I);colormap(gray);
Isizes = size(I);
J = zeros(size(I));
[y,x] = ginput(1);
threshold = 50;
x = round(x);y = round(y);
seedvalue = I(x,y);
J(x,y) = 1;

%% intial stack
stack_init = 10000; 
stack = zeros(stack_init,2); 
stack(1,:) = [x y]; stack_top = 1;

% Neighbor locations (footprint)
neigb=[-1 0; 1 0; 0 -1;0 1];
while(stack_top ~= 0)
    x = stack(stack_top,1);y = stack(stack_top,2);
    stack_top = stack_top -1;
    for j=1:4
        % Calculate the neighbour coordinate
        xn = x +neigb(j,1); yn = y +neigb(j,2);
        
        % Check if neighbour is inside or outside the image
        ins=(xn>=1)&&(yn>=1)&&(xn<=Isizes(1))&&(yn<=Isizes(2));
            
        % Add neighbor if inside and not already part of the segmented area
        if(ins&&(J(xn,yn)==0)) 
            % 是否小于门限
            isin=abs(I(xn,yn)-seedvalue)<threshold;
            if(isin)
                stack_top = stack_top+1;
                stack(stack_top,:) = [xn yn]; J(xn,yn)=1;
            end
        end
    end
end
figure;imagesc(J);colormap(gray);