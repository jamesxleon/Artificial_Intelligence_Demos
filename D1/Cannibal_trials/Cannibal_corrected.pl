:- [adts].

% Initial state
initial(state(3, 3, w)).

% Goal state
goal(state(0, 0, e)).

% Valid state
valid(state(M, C, _)) :-
    M >= 0, C >= 0, M =< 3, C =< 3,
    (M >= C ; M = 0),
    M2 is 3 - M, C2 is 3 - C,
    (M2 >= C2 ; M2 = 0).

% Possible moves
move(state(M, C, w), state(M2, C2, e)) :-
    member([DM, DC], [[0, 1], [0, 2], [1, 0], [1, 1], [2, 0]]), % Possible combinations of missionaries and cannibals to move
    M2 is M - DM, C2 is C - DC, valid(state(M2, C2, e)),
    writelist(['try moving', DM, 'missionaries and', DC, 'cannibals from west to east']).

move(state(M, C, e), state(M2, C2, w)) :-
    member([DM, DC], [[0, 1], [0, 2], [1, 0], [1, 1], [2, 0]]), % Possible combinations of missionaries and cannibals to move
    M2 is M + DM, C2 is C + DC, valid(state(M2, C2, w)),
    writelist(['try moving', DM, 'missionaries and', DC, 'cannibals from east to west']).

move(state(F, M, C), state(F, M, C)) :-
    writelist(['      BACKTRACK from:', F, M, C]), fail.

% Solve the problem
go(Start,Goal) :-
    empty_queue(Empty_been_queue),
    add_to_queue(Start, Empty_been_queue, Been_queue),
    path(Start,Goal,Been_queue).

path(Goal,Goal,Been_queue) :-
    write('Solution Path Is:' ), nl,
    print_queue(Been_queue).

path(State,Goal,Been_queue) :-
    move(State,Next_state),
    not(member_queue(Next_state,Been_queue)),
    add_to_queue(Next_state, Been_queue, New_been_queue),
    path(Next_state,Goal,New_been_queue),!.

% Write list
writelist([]) :- nl.
writelist([H|T]) :-
    print(H), tab(1),
    writelist(T).

print_queue(Q) :-
        empty_queue(Q).
print_queue(Q) :-
        remove_from_queue(E, Q, Rest),
        print_queue(Rest),
        write(E), nl.
