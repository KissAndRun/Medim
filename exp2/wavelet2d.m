clear all; close all;

load woman;

% X contains the loaded image. 
% map contains the loaded colormap. 
nbcol = size(map,1);

% Perform single-level decomposition 
% of X using db1. 
[cA1,cH1,cV1,cD1] = dwt2(X,'db1');

% Images coding. 
cod_X = wcodemat(X,nbcol); 
cod_cA1 = wcodemat(cA1,nbcol); 
cod_cH1 = wcodemat(cH1,nbcol); 
cod_cV1 = wcodemat(cV1,nbcol); 
cod_cD1 = wcodemat(cD1,nbcol); 
dec2d = [... 
        cod_cA1,     cod_cH1;     ... 
        cod_cV1,     cod_cD1      ... 
        ];