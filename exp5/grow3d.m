clc;clear;close all;
Path = './';
%% 1.Load the CT 
File = strcat(Path,'YUCHANGHUA_Thrx_CT.mhd');
I = read_mhd(File);

I = I.data;
Isizes = size(I);
J = zeros(size(I));
x = 107;y = 112;z = 52;
threshold = 45;
seedvalue = I(x,y,z);
J(x,y,z) = 1;
%% intial stack
stack_init = 10000; 
stack = zeros(stack_init,3); 
stack(1,:) = [x y z]; stack_top = 1;
k = 0;

% Neighbor locations (footprint)
neigb=[-1 0 0; 1 0 0; 0 -1 0;0 1 0;0 0 1;0 0 -1];
tic
while(stack_top ~= 0)
    x = stack(stack_top,1);y = stack(stack_top,2);
    z = stack(stack_top,3);
    stack_top = stack_top -1;
    for j=1:6
        % Calculate the neighbour coordinate
        xn = x +neigb(j,1); yn = y +neigb(j,2);zn = z +neigb(j,3);
        
        % Check if neighbour is inside or outside the image
        ins=(xn>=1)&&(yn>=1)&&(zn>=1)&&(xn<=Isizes(1))&&(yn<=Isizes(2))&&(zn<=Isizes(3));
            
        % Add neighbor if inside and not already part of the segmented area
        if(ins&&(J(xn,yn,zn)==0)) 
            % 是否小于门限
            isin=abs(I(xn,yn,zn)-seedvalue)<threshold;
            if(isin)
                stack_top = stack_top+1;
                stack(stack_top,:) = [xn yn zn]; J(xn, yn, zn)=1;
            end
        end
    end
end
toc
SliceBrowser(J);
