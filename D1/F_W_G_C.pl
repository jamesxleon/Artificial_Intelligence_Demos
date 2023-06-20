/*
 * This is the code for the Farmer, Wolf, Goat and Cabbage Problem
 * using the ADT Stack.
 *
 */

:- [adts]. /* consults (reconsults) file containing the
              various ADTs (Queue, etc.) */

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

move(state(X,X,G,C), state(Y,Y,G,C))
              :- opp(X,Y), not(unsafe(state(Y,Y,G,C))),
                 writelist(['try farmer takes wolf',Y,Y,G,C]).

move(state(X,W,X,C), state(Y,W,Y,C))
              :- opp(X,Y), not(unsafe(state(Y,W,Y,C))),
                 writelist(['try farmer takes goat',Y,W,Y,C]). 

move(state(X,W,G,X), state(Y,W,G,Y))
              :- opp(X,Y), not(unsafe(state(Y,W,G,Y))),
                 writelist(['try farmer takes cabbage',Y,W,G,Y]).

move(state(X,W,G,C), state(Y,W,G,C))
              :- opp(X,Y), not(unsafe(state(Y,W,G,C))),
                 writelist(['try farmer takes self',Y,W,G,C]).

move(state(F,W,G,C), state(F,W,G,C))
              :- writelist(['      BACKTRACK from:',F,W,G,C]), fail.

unsafe(state(X,Y,Y,C)) :- opp(X,Y).
unsafe(state(X,W,Y,Y)) :- opp(X,Y).

writelist([]) :- nl.
writelist([H|T]):- print(H), tab(1),  
                   writelist(T).

opp(e,w).
opp(w,e).

print_queue(Q) :-
        empty_queue(Q).
print_queue(Q) :-
        remove_from_queue(E, Q, Rest),
        print_queue(Rest),
        write(E), nl.