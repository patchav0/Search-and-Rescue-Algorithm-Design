%process maze image
Maze = rgb2gray(maze1);
Maze = imbinarize(Maze);
dims=size(Maze);dims=dims(1:2);
while(dims > 11)
    dims=round(dims/sqrt(2));
end
Z=imresize(Maze,dims);

imshow(Z)
hold on;
plot(2, 3, 'r*', 'MarkerSize', 5);
pause(.1)
axis on;
r = move(2,3, 2,2, Z)
function r = move(p1, p2, p1o, p2o, map)

    %move right
    if( map(p2, p1 + 1) == 1 && p1 < 10 && p1o ~= p1 + 1)
        p1o = p1;
        p2o = p2;
        p1 = p1 + 1;
        plot(p1, p2, 'r*', 'MarkerSize', 5);
        pause(.1)
        r = move(p1, p2, p1o, p2o, map)
    %move down
    elseif( map(p2 + 1, p1) == 1 && p2 < 10 && p2o ~= p2 + 1)
        p1o = p1;
        p2o = p2;
        p2 = p2 + 1;
        plot(p1, p2, 'r*', 'MarkerSize', 5);
        pause(.1)
        r = move(p1, p2, p1o, p2o, map)
  
    %move left    
    elseif( map(p2, p1 - 1) == 1 && p1 > 0 && p1o ~= p1 - 1)
        p1o = p1;
        p2o = p2;
        p1 = p1 - 1;
        plot(p1, p2, 'r*', 'MarkerSize', 5);
        pause(.1)
        r = move(p1, p2, p1o, p2o, map)    
    %move up
    elseif( map(p2 - 1, p1) == 1 && p2 > 0 && p2o ~= p2 - 1 )
        p1o = p1;
        p2o = p2;
        p2 = p2 - 1;
        plot(p1, p2, 'r*', 'MarkerSize', 5);
        pause(.1)
        r = move(p1, p2, p1o, p2o, map)   
    %move back
    elseif(map(p2,p1) ~= 2)
        temp = p1o;
        p1o = p1;
        p1 = temp;
        temp = p2o;
        p2o = p2;
        p2 = temp;
        plot(p1, p2, 'r*', 'MarkerSize', 5);
        pause(.1)
        r = move(p1, p2, p1o, p2o, map) 
    else
        r = 1;
    end
end
