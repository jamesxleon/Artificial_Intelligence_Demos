% Initial state
initial(state(M, C, B), state(M, C, B)).

% Goal state
goal(state(M, C, B), state(M, C, B)).

% Valid state
valid(state(M, C, _)) :-
    M >= 0, C >= 0, M =< 3, C =< 3,
    (M >= C ; M = 0),
    M2 is 3 - M, C2 is 3 - C,
    (M2 >= C2 ; M2 = 0).

% Possible moves
move(state(M, C, B), state(M2, C2, B2), Move) :-
    B = 0, B2 is 1, % Move from original side to other side
    member([DM, DC], [[0, 1], [0, 2], [1, 0], [1, 1], [2, 0]]), % Possible combinations of missionaries and cannibals to move
    M2 is M - DM, C2 is C - DC, valid(state(M2, C2, B2)),
    Move = move(DM, DC, B2).

move(state(M, C, B), state(M2, C2, B2), Move) :-
    B = 1, B2 is 0, % Move from other side to original side
    member([DM, DC], [[0, 1], [0, 2], [1, 0], [1, 1], [2, 0]]), % Possible combinations of missionaries and cannibals to move
    M2 is M + DM, C2 is C + DC, valid(state(M2, C2, B2)),
    Move = move(DM, DC, B2).

% Solve the problem
solve(Node, Path, Moves, Goal) :-
    depthfirst(Node, Path, Moves, [Node], [], Goal).

depthfirst(Node, [Node], [], _, _, Goal) :-
    goal(Node, Goal).

depthfirst(Node, [Node|Path], [Move|Moves], Visited, _, Goal) :-
    move(Node, Node1, Move),
    \+ member(Node1, Visited),
    depthfirst(Node1, Path, Moves, [Node1|Visited], [Move], Goal).

% Print the solution
print_solution(Start, Goal) :-
    initial(Start, StartState),
    solve(StartState, Solution, Moves, Goal),
    writelist(Solution),
    write_moves(Moves).

% Write list
writelist([]).
writelist([H|T]) :-
    write(H), nl,
    writelist(T).

% Write moves
write_moves([]).
write_moves([move(DM, DC, B)|T]) :-
    ( B = 1 -> Side = "1" ; Side = "0" ),
    format("~d missionaries and ~d cannibals cross to ~s\n", [DM, DC, Side]),
    write_moves(T).
