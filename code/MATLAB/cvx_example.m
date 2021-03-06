%% Least-squares problem
% minimize ||A*x-b||_2

% randomly generate problem data
m = 16;
n = 8;
A = randn(m,n);
b = randn(m,1);

% solution
x_ls = A \ b;

% solution using cvx
cvx_begin quiet
    variable x(n)
    minimize( norm(A*x-b) );
cvx_end

% show that the two solutions are the same
disp(norm(x-x_ls))




%% Multiagent path planning problem
%
% assumptions:
%   - same number of agents as targets (n = m)
%   - each agent moves to a single target

% weighted adjacency matrix
A = [0 3 1 0 0; 3 0 7 5 1; 1 7 0 2 0; 0 5 2 0 7; 0 1 0 7 0];

% node names
nodenames = {'A','B','C','D','E'};

% graph
G = graph(A,nodenames);

% agents
agents = [1 2];

% targets
targets = [4 5];

% number of agents
n = length(agents);

% number of targets
m = length(targets);

% cost(i,j) = optimal cost for agent i to go to target j (from Dijkstra's algorithm)
cost = distances(G,agents,targets);

cvx_begin quiet

    % binary indicator variable for whether agent i should go to target j
    variable z(n,m)
    0 <= z <= 1;
    
    % each target is obtained by an agent
    1 == sum(z,1);
    
    % each agent moves to a target
    1 == sum(z,2);
    
    % total cost over all agents
    total_cost = sum(sum(z.*cost));
    
    % optimize the total cost
    minimize(total_cost);
    
cvx_end

% display results
disp('cost matrix')
disp(cost)
disp('indicator matrix')
disp(z)
disp('total cost')
disp(total_cost)


%% Create graph from image

% maze dimensions
rows = 100;
cols = 100;

% load image
img = imread('../images/maze1.jpg');

% convert to grayscale
img = rgb2gray(img);

% resize to desired dimensions
img = imresize(img,[rows cols]);

% convert to binary
maze = imbinarize(img);

% show the maze
imshow(maze);
