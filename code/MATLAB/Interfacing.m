
%process maze image

Maze = rgb2gray(maze1);
Maze = imbinarize(Maze);
dims=size(Maze);dims=dims(1:2);
while(dims > 100)
    dims=round(dims/sqrt(2));
end
B=imresize(Maze,dims);



% Plot red star at start of maze

imshow(B)
hold on;
plot(13,2, 'r*', 'MarkerSize', 5);
axis on;


