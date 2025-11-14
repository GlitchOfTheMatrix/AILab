% --- Maximum of two numbers ---
max2(X, Y, X) :- X >= Y.
max2(X, Y, Y) :- Y > X.

% --- Maximum of three numbers ---
max3(X, Y, Z, Max) :-
    (X >= Y, X >= Z -> Max = X ;
     Y >= Z -> Max = Y ;
     Max = Z).
