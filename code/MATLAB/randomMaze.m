function [M] = randomMaze(n,animate,dt,filename)
% Construct a random maze using depth-first search.
% http://rosettacode.org/wiki/Maze_generation#MATLAB_.2F_Octave

% default parameters
if nargin < 2
    animate = false;
end
if nargin < 3
    dt = 0.1;
end

% constants
PATH       = 1;
WALL       = inf;
NotVISITED = -1;
VISITED    = -2;

% dimension of matrix (including an extra outer wall)
m = 2*n+3;

% offsets of neighboring cells (in linear coordinates)
offsets = [-1, m, 1, -m];

% initialize maze matrix
M = NotVISITED(ones(m));
M([1 2:2:end end],:) = WALL;
M(:,[1 2:2:end end]) = WALL;

% start position
currentCell = sub2ind(size(M),3,3);

% mark the current cell as VISITED
M(currentCell) = VISITED;

% list of VISITED cells that have NotVISITED neighbors
S = currentCell;

ind = 1;

% loop until all cells are VISITED
while ~isempty(S)
    
    % get the neighboring cells that are NotVISITED
    moves = currentCell + 2*offsets;
    unvistedNeigbors = find(M(moves)==NotVISITED);
    
    % if there are NotVISITED neighboring cells
    if ~isempty(unvistedNeigbors)
        
        % choose a random neighbor that is NotVISITED
        next = unvistedNeigbors(randi(length(unvistedNeigbors),1));
        
        % remove the wall between the current cell and its neighbor
        M(currentCell + offsets(next)) = PATH;
        
        % if the neighbor has any NotVISITED neighbors, add it to the list
        newCell = currentCell + 2*offsets(next);
        if (any(M(newCell+2*offsets)==NotVISITED))
            S = [S newCell];
        end
        
        % set the new cell as the current cell
        currentCell = newCell;
        
        % label the current cell as VISITED
        M(currentCell) = VISITED;
        
    % if all neighboring cells are VISITED
    else
        
        % set the current cell as the first cell in the list
        currentCell = S(1);
        
        % remove the cell from the list
        S = S(2:end);
    end
    
    % update the animation
    if animate
        drawMaze(M);
        
        % save animation as a gif
        if nargin == 4
            frame = getframe(gcf);
            im = frame2im(frame);
            [A,map] = rgb2ind(im,256);
            if ind == 1
                imwrite(A,map,filename,'gif','LoopCount',Inf,'DelayTime',dt);
            else
                imwrite(A,map,filename,'gif','WriteMode','append','DelayTime',dt);
            end
        end
        ind = ind+1;
        
        pause(dt);
    end
end

% set VISITED to PATH
M(M==VISITED) = PATH;

drawMaze(M);

end