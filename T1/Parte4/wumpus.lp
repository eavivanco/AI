%%%% Comentarios

%Hay una observabilidad parcial del mundo, lo que da paso a mundos posibles
%Queremos modelar el conocimiento del agente, no el funcionamiento del juego 
%Se considera tiempo discreto, con T0 = 0

%%%% Desarrollo

%%%set ambiente

#const timemax = 10. %definimos el tiempo maximo
time(1..timemax).

%%%set mapa
#const limitx = 3. %definimos los límites del mapa
#const limity = 3.

rangeX(0..limitx).
rangeY(0..limity).

cell(0..limitx, 0..limity). %se imprime el mapa en base a los limites definidos anteriormente
neigh(X,Y,Xp,Yp) :- cell(X,Y), cell(Xp,Yp), |Xp-X|+|Yp-Y|=1. %definimos celdas vecinas

%%%set de objetos (definidos y estaticos para la instancia)
#const qwumpus = 1. %se define la cantidad de obstaculos a tener
#const qpit = 1.
#const qgold = 1.

qwumpus{wumpus(X,Y) : cell(X,Y)}qwumpus. %se distribuyen los obstaculos en el mapa, no hay dos obstaculos en la misma casilla
qpit{pit(X,Y) : cell(X,Y), not wumpus(X,Y)}qpit.
qgold{gold(X,Y) : cell(X,Y), not wumpus(X,Y), not pit(X,Y)}qgold.

%%%set personaje
#const x0 = 0. %se definen las coordenadas iniciales del personaje
#const y0 = 0.

current(x0,y0,0). %se define posicion inicial

%%acciones posibles
action(up).
action(down).
action(left).
action(right).
action(wait).
action(shoot).

%%movimiento
1{exec(A, T) : action(A)}1 :- time(T + 1). %ejecucion movimientos

current(X,Y+1, T+1) :- exec(up,T), current(X,Y,T), cell(X,Y+1), not lose(T), not win(T).
current(X,Y-1, T+1) :- exec(down,T), current(X,Y,T), cell(X,Y-1), not lose(T), not win(T).
current(X-1,Y, T+1) :- exec(left,T), current(X,Y,T), cell(X-1,Y), not lose(T), not win(T).
current(X+1,Y, T+1) :- exec(right,T), current(X,Y,T), cell(X+1,Y), not lose(T), not win(T).
current(X,Y, T+1) :- exec(wait,T), current(X,Y,T).
dead_wumpus(Xp,Yp) :- exec(shoot, T), current(X,Y,T), wumpus(Xp,Yp), neigh(X,Y,Xp,Yp), sense_stench(Xp,Yp).

%%estados 
known(X,Y) :- current(X, Y, T). %se taggea como conocida la posicion visitada (similar a alive creo)

win(T..timemax) :- current(X,Y,T), gold(X,Y).
lose(T..timemax) :- current(X,Y,T), wumpus(X,Y), not dead_wumpus(X,Y).
lose(T..timemax) :- current(X,Y,T), pit(X,Y).

sense_breeze(Xp,Yp) :- pit(X,Y), neigh(X,Y,Xp,Yp), known(Xp,Yp). %solo se percibe si se conoce la celda
sense_stench(Xp,Yp) :- wumpus(X,Y), neigh(X,Y,Xp,Yp), known(Xp,Yp), not dead_wumpus(X,Y).

%%%% Desarrollo

%%%constraints
:- not win(timemax). %se muestran solo los modelos en que se gana
%:- not lose(timemax). %se muestran solo los modelos en que se gana

%%%% Ejecucion experiencia usuario
#show current/3.
#show win/1.
#show lose/1.
#show sense_breeze/2. 
#show sense_stench/2.

