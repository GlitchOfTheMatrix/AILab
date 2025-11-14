% max of two
max2(A, B, A) :- A >= B, !.
max2(_, B, B).

% max of three using max2
max3(A, B, C, M) :-
    max2(A, B, T),
    max2(T, C, M).
