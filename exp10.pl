% fib(N, F) single term
fib(0, 0) :- !.
fib(1, 1) :- !.
fib(N, F) :-
    N > 1,
    N1 is N - 1,
    N2 is N - 2,
    fib(N1, F1),
    fib(N2, F2),
    F is F1 + F2.

% fib_upto(N, List) -> [F0, F1, ..., FN]
fib_upto(N, L) :-
    N >= 0,
    fib_upto_acc(0, N, [], Rev),
    reverse(Rev, L).

fib_upto_acc(I, N, Acc, Acc) :- I > N, !.
fib_upto_acc(I, N, Acc, L) :-
    fib(I, F),
    I1 is I + 1,
    fib_upto_acc(I1, N, [F|Acc], L).
