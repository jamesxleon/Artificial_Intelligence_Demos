:- [adts]

go(Start, Goal) :-
    empty_queue(Empty_open),
    state_record(Start, nil, 0, 0, Start, Start_state),
    add_to_queue(Start_state, Empty_open, Open),
    empty_set(Closed),
    path(Open, Closed, Goal).

path(Goal, Goal, Been, Queue) :- 
    write('Solution path is: '), nl,
    printsolution(Goal, Been, Queue).