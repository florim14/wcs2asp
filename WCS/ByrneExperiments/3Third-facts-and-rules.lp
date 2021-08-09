
true(e).
true(l) :- true(e),false(abe).
true(l) :- true(o),false(abo).
true(abe) :- false(o).
true(abo) :- false(e).

false(l) :- false(e),false(o).
false(l) :- false(e),true(abo).
false(l) :- true(abe),false(o).
false(l) :- true(abe),true(abo).
false(abe) :- true(o).
false(abo) :- true(e).

