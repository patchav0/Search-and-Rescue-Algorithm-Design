function G = weightedMaze(M) 

    % find the size of the matrix
    dims = size(M);

    % find the nodes (this is assuming the nodes are the coordinates with 
    % the highest value. this can be changed by changing nVal)
    nVal = max(dims);
    [r, c] = find(M == nVal);
    nodes = [r, c];
    nodeCount = size(nodes);
    nodeCount = nodeCount(1);

    % matrix to store pode paths
    nPaths = zeros(nodeCount);

    count = 0;
    % repeat this loop until the nPaths matix is full
    % ignores the diagonal of the nPath matrix; these will always be 0
    % while(sum(imbinarize(find(nPaths == 0))) > nodeCount)

    %repeat a certain amount of times instead
    for i = 1:1000
        for n = 1:nodeCount
        tempMaze = M;
            %current node
            cn = nodes(n,:);
            start = cn;
            %current path weight
            cpath = 0;
            %get coords of surroundings
            [U, D, L, R] = lookAround(cn, dims);

            % make current node inaccesable
           % tempMaze(cn(1), cn(2)) = 0;
            foundNode = 0;
            failsafe = 0;
            %% move until a node is found
            while(foundNode(1) == 0 && failsafe < 100)
                failsafe = failsafe + 1;
                % decide random direction
                x = randi(4);
                switch x
                    case 1
                        if(U(1) ~= 0 && tempMaze(U(1), U(2)) ~= 0)
                            cn = U;
                            %% update directions
                            [U, D, L, R] = lookAround(cn, dims);
                        end
                    case 2
                        if(D(1) ~= 0 && tempMaze(D(1), D(2)) ~= 0)
                            cn = D;
                            [U, D, L, R] = lookAround(cn, dims);
                        end
                    case 3
                        if(L(1) ~= 0 && tempMaze(L(1), L(2)) ~= 0)
                            cn = L;
                            [U, D, L, R] = lookAround(cn, dims);
                        end
                    otherwise
                        if(R(1) ~= 0 && tempMaze(R(1), R(2)) ~= 0)
                            cn = R;
                            [U, D, L, R] = lookAround(cn, dims);
                        end
                end




                %% cn has changed check for node, and change path weight
                % if you are back at the start node reset the path
                if (cn == start)
                    cpath = 0;
                else 
                val = M(cn(1),cn(2));
                    % if cn is a node other than the start node then finish
                    if(val == nVal)
                    cpath = cpath + 1;
                    foundNode = cn;
                    else
                    % if cn is not a node add its weight to the path
                    cpath = cpath + val;
                    end
                end

            end

            if(failsafe == 100) 
                break;
            end

            nRow = 0;
            for j = 1:nodeCount
                if(nodes(j,:) == foundNode)
                    nRow = j;
                end
            end

             % store the path of the found node in the nPath matrix
             if( nPaths(nRow, n) == 0 || nPaths(nRow, n) > cpath )
                nPaths(nRow, n) = cpath;
                nPaths(n, nRow) = cpath;
             end
        end   
    end

    %% Make a graph from results

    G = graph(nPaths)
    plot(G,'EdgeLabel',G.Edges.Weight)
    figure
    imagesc(M)

    %% Function that finds coordinates of surrounding
    function [U, D, L, R] = lookAround(cn, dims)
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
