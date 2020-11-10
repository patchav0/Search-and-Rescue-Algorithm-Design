function solution = createGraph(A, start, goal, labelGraph) 
%% Takes a maze matrix in the form of 1s and 0s, a starting point [a b], and ending point [c d]
% and an optional flag labelGraph. If the flag is set to one, the graph will be labeled and the solution will
% be returned in the form of a sequential list of coodinates from the start to finish.

%if user does not specify labels don't label
if nargin < 4
labelGraph = 0;
end
[row col] = find(A == 1);
dims = size(A);
nodeList = row;
nodeList = [nodeList, col];
L = size(nodeList, 1);
if(labelGraph)
    Labels = strings(1, L);  
end

for cNode = 1:L
    cnCoords = nodeList(cNode,:);
    % make a list of labels coresponding to node number
    if(labelGraph)
        Labels(cNode) = "(" + cnCoords(1) + ", " + cnCoords(2) + ")";
    end
end

s = zeros(1, dims(1)^2);
t = zeros(1, dims(1)^2);
nodeIdx = 1;

for cNode = 1:L
    cnCoords = nodeList(cNode,:);
    [U, D, L, R] = lookAround(cnCoords, dims);
    neighbors = [U; D; L; R];
    
    %for every neighbor
    for i = 1:4
        neighborCoords = neighbors(i,:);
        if(neighborCoords(1) ~= 0)
            % find the node number from the coordinates
            neighbor = find(ismember(nodeList, neighborCoords,'rows'));

            %% Check neighbor
            isNode = sum(ismember(nodeList,neighborCoords,'rows'));
            if(isNode) 
                s(nodeIdx) = cNode;
                t(nodeIdx) = neighbor; 
                nodeIdx = nodeIdx + 1;
            end

        end
    end    
end

s = s(1:nodeIdx - 1);
t = t(1:nodeIdx - 1);
G = graph(s,t);
G = simplify(G);
figure
P = plot(G)
if(labelGraph)
    labelnode(P,[1:size(Labels,2)],Labels);
end
figure
imagesc(A);

start = find(ismember(nodeList, start,'rows'));
goal = find(ismember(nodeList, goal,'rows'));

steps = [];
F = double(A);
path = shortestpath(G,start, goal);
if(labelGraph)
         steps = strings(1, size(path,2));
end
for step = 1:size(path,2)
     if(labelGraph)
         steps(step) = Labels(path(step));
     end
    coord = nodeList(path(step),:);
    F(coord(1),coord(2)) = 3;
end
figure
imagesc(F)
solution = F;
if(labelGraph)
    solution = steps;
end
end

%% Function that finds coordinates of surrounding
function [U, D, L, R] = lookAround(cn, dims)
    U = [0,0]; D = [0,0]; L = [0,0]; R = [0,0];
    %up
    if(cn(1) - 1 > 0)
        U = cn;
        U(1) = U(1) - 1;
    end
    %down 
    if(cn(1) + 1 <= dims(1))
        D = cn;
        D(1) = D(1) + 1;
    end
    %left
    if(cn(2) - 1 > 0)
        L = cn;
        L(2) = L(2) - 1;
    end
    %right
    if(cn(2) + 1 <= dims(2))
        R = cn;
        R(2) = R(2) + 1;
    end
end
