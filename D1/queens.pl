% render solutions nicely.
%:- use_rendering(chess).

% use the Constraint Logic Programming over Finite Domains library
:- use_module(library(clpfd)).

% main predicate
n_queens(N, Queens) :-
    length(Queens, N),
    Queens ins 1..N,
    board(Queens, Board, 0, N, _, _),
    safe_queens(Board, 0, Queens).

% board setup
board([], [], N, N, _, _).
board([_|Queens], [Col-Vars|Board], Col0, N, [_|VR], VC) :-
    Col is Col0+1,
    functor(Vars, f, N),
    constraints(N, Vars, VR, VC),
    board(Queens, Board, Col, N, VR, [_|VC]).

% constraints setup
constraints(0, _, _, _) :- !.
constraints(N, Row, [R|Rs], [C|Cs]) :-
    arg(N, Row, R-C),
    M is N-1,
    constraints(M, Row, Rs, Cs).

% queen placement
safe_queens([], _, []).
safe_queens([C|Cs], Row0, [Col|Solution]) :-
    Row is Row0+1,
    select(Col-Vars, [C|Cs], Board),
    arg(Row, Vars, Row-Row),
    safe_queens(Board, Row, Solution).