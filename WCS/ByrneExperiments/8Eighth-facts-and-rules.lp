
true(l) :- true(e),false(abe).
true(l) :- true(t),false(abt).
false(abe).
false(abt).

false(l) :- false(e),false(t).
false(l) :- false(e),true(abt).
false(l) :- true(abe),false(t).
false(l) :- true(abe),true(abt).


:- not true(l).
atom(t).
atom(e).