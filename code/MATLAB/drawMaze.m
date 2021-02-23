function drawMaze(M)
% Draw the maze.

% set colormap
c = flipud(gray(256));
c = [c; [0 0 1]; [1 0 0]; [0 1 0]; [0 0 0]];
colormap(c);

% set axis background white
set(gcf,'color','w');

image(M);
axis equal off;
drawnow;

end