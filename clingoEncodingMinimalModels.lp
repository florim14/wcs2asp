% The preference file to specify what kind of preferences we
% want among models. In this case it is subset minimal wrt
% to the true(X) and false(X).


#heuristic false(X). [1,false]
% #heuristic false(X). [1, level]
% #heuristic false(X). [-1, sign]

#heuristic true(X). [1,false]
% #heuristic true(X). [1, level]
% #heuristic true(X). [-1, sign]



{true(X); false(X)}1:- atom(X).
:- true(X), false(X).


#show true/1.
#show false/1.
