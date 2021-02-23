% read image
map = imread('maze1.jpg');

% if the image is in color turn it black and white. (check if its a 
% three dimensional matrix)
x = size(map);
x = size(x);
x = x(2);
if(x == 3)
    map = rgb2gray(map);
end

%make sure the image is square


Z = imbinarize(map);
dims=size(Z);
Z = imresize(Z,[max(dims) max(dims)]);
imagesc(Z);

windowSize = 20;
X = Z;

%iterate through windows to make each node perfectly square
for r = 1:windowSize:(dims(1) - windowSize)
    for c = 1:windowSize:(dims(1) - windowSize)
        %window r, c
        W = X(r:r+(windowSize-1),c:c+(windowSize-1));
        X(r:r+(windowSize-1),c:c+(windowSize-1)) = round(mean(mean(W)));
    end
end
figure
imagesc(X)
A = imresize(X, 1/windowSize);
figure
imagesc(A);





