clear all;
% Create a graph

s = [1 1 2 2 2 3 4];
t = [2 4 3 4 5 5 5];
edges = [s;t]';
dim = size(s);
dim = dim(2);
weights = randperm(dim);
%node_names = {'A','B','C','D','E'};
G1 = graph(s, t, weights)
plot(G1,'EdgeLabel',G1.Edges.Weight)

    
%% Find neighbors of current node
Nc = 1;
Ng = 3;

totalCost = 0;
while (Nc ~= Ng)
    %visited nodes
    visited = [];
    % coordinants of neighbor nodes
    ucoords = [];
    % neighbor nodes
    u = [];
    cost = weights;
    [row, column] = find(edges == Nc);
    for i = 1:length(row)
        % we want the same row, the other column
        c = 1;
        if( column(i) == 1 )
            c = 2;
        end
        ucoords = [ucoords; [row(i), c]];
        u = [u ; edges(row(i), c)];
    end

    %%



    %for each neighbor
    small = Nc;
    distc = 0;
    distu = 100000;
    for i = 1:length(u)
        %if node has not been visited)
        if( sum(find(visited == u(i))) == 0 ) 
            %find cost(Nc, u)
            temp = ucoords(i);
            temp = temp(1);
            cost = weights (temp);


            if (distc + cost < distu) 
                distu = distc + cost;
                small = u(i);
            end
        end

    end
    visited = [visited; Nc];
    Nc = small;
    totalCost = totalCost + distu;
    
end

