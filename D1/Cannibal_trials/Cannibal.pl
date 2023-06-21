:- [adts].

go(Start, Goal) :-
    empty_queue(Empty_been_queue),
    add_to_queue(Start, Empty_been_queue, Been_queue),
    path(Start, Goal, Been_queue).

path(Goal, Goal, Been_queue) :-
    write('Solution path is: '), nl,
    print_queue(Been_queue).

path(State, Goal, Been_queue) :-
    move(State, Next_state),
    not(member_queue(Next_state, Been_queue)),
    add_to_queue(Next_state, Been_queue, New_been_queue),
    path(Next_state, Goal, New_been_queue), !.
    
move(state(X, X, Cannibals), state(Y, Y, Cannibals)) :-
    opp(X, Y), not(unsafe(state(Y, Y, Cannibals))),
    writelist(['try two missionaries cross the river', Y, Y, Cannibals]).
    
move(state(X, Missionaries, X), state(Y, Missionaries, Y)) :-
    opp(X, Y), not(unsafe(state(Y, Missionaries, Y))),
    writelist(['try two cannibals cross the river', Y, Missionaries, Y]).

move(state(X, Missionaries, Cannibals), state(Y, Missionaries, Cannibals)) :-
    opp(X,Y), not(unsafe(state(Y, Missionaries, Cannibals))),
    writelist(['try one missionary amd one cannibal cross the river', Y, Missionaries, Cannibals]).

move(state(X, Missionaries, Cannibals), state(X, Missionaries, Cannibals)) :- 
    writelist(['      BACKTRACK from:',X,Missionaries,Cannibals]), fail.

unsafe(state(X, Missionaries, Cannibals)) :-
    Missionaries > 0, Cannibals > Missionaries,
    opp(X, OtherSide), 
    OtherCannibals is 3 - Cannibals,
    OtherMissionaries is 3 - Missionaries,
    OtherMissionaries > 0, OtherCannibals > OtherMissionaries.

writelist([]) :- nl.
writelist([H|T]) :- write(H), tab(1), writelist(T).

opp(e,w).
opp(w,e).

print_queue(Q) :-
    empty_queue(Q).
print_queue(Q) :-
    remove_from_queue(E, Q, Rest),
    print_queue(Rest),
    write(E), nl.
