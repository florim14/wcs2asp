
true(l) :- true(e),false(abe).
false(abe).

false(l) :- false(e).
false(l) :- true(abe).


:- not true(l).
atom(e).