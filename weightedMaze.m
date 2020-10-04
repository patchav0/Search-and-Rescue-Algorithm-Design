clear all
load('weightMaze.mat')

% Maze = rgb2gray(maze1);
% Maze = imbinarize(Maze);
% dims=size(Maze);dims=dims(1:2);
% while(dims > 10)
%     dims=round(dims/sqrt(2));
% end
% Z=imresize(Maze,dims);
% 
% weights = randperm(dims(2));
% for i = 1:dims(1) - 1
%     weights = [weights ; randperm(dims(2))];
% end
% 
% weightMaze = Z .* weights;
% M = weightMaze;
% imagesc(M)
% nodeVal = dims(1);

% assume we know the coordinates of each node
dims = size(weightMaze);

nodes = [2,6; 3,4; 5,2; 7,6; 8,3];
nodeCount = 5;

% matrix to store pode paths
nPaths = zeros(nodeCount);

count = 0;
% repeat this loop until the nPaths matix is full
% ignores the diagonal of the nPath matrix; these will always be 0
while(sum(imbinarize(find(nPaths == 0))) > nodeCount)
    for n = 1:nodeCount
    tempMaze = weightMaze;
        %current node
        cn = nodes(n,:);
        start = cn;
        %current path weight
        cpath = 0;
        %get coords of surroundings
        U = 0; D = 0; L = 0; R = 0;
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
        
        % make current node inaccesable
       % tempMaze(cn(1), cn(2)) = 0;
        foundNode = 0;
        %% move until a node is found
        while(foundNode == 0)
            % decide random direction
            x = randi(4);
            switch x
                case 1
                    if(U(1) ~= 0 && tempMaze(U(1), U(2)) ~= 0)
                        cn = U;
                        %% update directions
                        U = 0; D = 0; L = 0; R = 0;
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
                case 2
                    if(D(1) ~= 0 && tempMaze(D(1), D(2)) ~= 0)
                        cn = D;

                        U = 0; D = 0; L = 0; R = 0;
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
                case 3
                    if(L(1) ~= 0 && tempMaze(L(1), L(2)) ~= 0)
                        cn = L;

                        U = 0; D = 0; L = 0; R = 0;
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
                otherwise
                    if(R(1) ~= 0 && tempMaze(R(1), R(2)) ~= 0)
                        cn = R;

                        U = 0; D = 0; L = 0; R = 0;
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
            end
            


            
            %% cn has changed check for node, and change path weight
            % if you are back at the start node reset the path
            if (cn == start)
                cpath = 0;
            else 
            val = weightMaze(cn(1),cn(2));
                % if cn is a node other than the start node then finish
                if(val == 9)
                cpath = cpath + 1;
                foundNode = cn;
                else
                % if cn is not a node add its weight to the path
                cpath = cpath + val;
                end
            end
            
        end
        nRow = 0;
        for j = 1:nodeCount
            if(nodes(j,:) == foundNode)
                nRow = j;
            end
        end
        
         % store the path of the found node in the nPath matrix
         if(nPaths(nRow, n) == 0 || nPaths(nRow, n) > cpath)
            nPaths(nRow, n) = cpath;
            nPaths(n, nRow) = cpath;
         end
         
         nPaths
         
         
       
    end

    
end





