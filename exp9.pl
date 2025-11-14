% sum_n(N, S) computes 1 + 2 + ... + N (with sum_n(0,0))
sum_n(0, 0) :- !.
sum_n(N, S) :-
    N > 0,
    N1 is N - 1,
    sum_n(N1, S1),
    S is S1 + N.
