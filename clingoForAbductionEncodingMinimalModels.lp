% The preference file to specify what kind of preferences we
% want among models. In this case it is subset minimal wrt
% to the true(X) and false(X).

{true(X); false(X)}1:- atom(X).
:- true(X), false(X).

#show true/1.
#show false/1.


#heuristic false(X). [1,false]
#heuristic true(X). [1,false]

% #preference(minimalModel,subset) {
%   true(X); false(X)
% }.

% #optimize(minimalModel).
