[row col] = find(A == 1);
dims = size(A);
nodeList = row;
nodeList = [nodeList, col];
[L, W]  = size(nodeList);

% make a list of labels coresponding to node number
for cNode = 1:L
    cnCoords = nodeList(cNode,:);
    Labels(cNode) = "(" + cnCoords(1) + ", " + cnCoords(2) + ")";
end

s = [];
t = [];

for cNode = 1:L
    cnCoords = nodeList(cNode,:);
    [U, D, L, R] = lookAround(cnCoords, dims);
    neighbors = [U; D; L; R];
    
    %for every neighbor
    for i = 1:4
        neighborCoords = neighbors(i,:);
        if(neighborCoords(1) ~= 0)
            % find the node number from the coordinates
            key = "(" + neighborCoords(1) + ", " + neighborCoords(2) + ")";
            neighbor = find(strcmp(Labels,key));

            %% Check neighbor
            isNode = sum(ismember(nodeList,neighborCoords,'rows'));

            if(isNode) 
                s = [s, cNode];
                t = [t, neighbor]; 
            end

        end
    end    
end

G = graph(s,t);
G = simplify(G);
P = plot(G)
labelnode(P,[1:196],Labels);
figure
imagesc(A);


start = [1 3];
key = "(" + start(1) + ", " + start(2) + ")";
start = find(strcmp(Labels,key));

goal = [19 17];
key = "(" + goal(1) + ", " + goal(2) + ")";
goal = find(strcmp(Labels,key));

steps = [];

path = shortestpath(G,start, goal);
for step = 1:size(path,2)
   steps = [steps;Labels(path(step))];
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

% %% Function that gets the label of the node
% function label = getLabel(nodeNum, Labels)
%     
%     key = "(" + start(1) + ", " + start(2) + ")";
%     start = find(strcmp(Labels,key));
% 
% end

