arco(a,b).
arco(b,c).
arco(c,d).
%arco(d,e).
%arco(e,f).

%arco(b,e).

iluminado(b). %definido por el usuario

%arco(c,a). %agregamos el ciclo

arco(X,Y) :- arco(Y,X). %hacemos que el grafo sea no dirigido

nodo(X) :- arco(X,Y).
nodo(Y) :- arco(X,Y).

iluminada(X,Y) :- arco(X,Y), iluminado(X). %Definimos que la calle esta iluminada si, al menos, uno de sus nodos esta iluminado
iluminada(X,Y) :- arco(X,Y), iluminado(Y).

no_iluminado(X,Y) :- arco(X,Y), not iluminado(X), not iluminado(Y), X != Y.

%maximo_arcos(M) :- M = #count{X,Y : arco(X,Y)}. %Se agrega un contador para la cantidad de arcos totales

%camino(X,Y,Largo) :- arco(X,Y), Largo=1, X != Y.
%camino(X,Y,Largo) :- camino(X,Z,L1), camino(Z,Y,L2), maximo_arcos(M),X != Y, Largo= L1+L2, Largo <= M. %Se agrega el limite M

contador_noiluminados(N) :- N = #count{X,Y : no_iluminado(X,Y)}. %contador de arcos no iluminados
%contador_iluminados(I) :- I = #count{X,Y : iluminada(X,Y)}. %contador de arcos iluminados

conectado_k(X,Y,K) :- no_iluminado(X,Y), K=1, X != Y.
conectado_k(X,Y,K) :- iluminada(X,Y), K=0, X != Y.
conectado_k(X,Y,K) :- conectado_k(X,Z,K1), conectado_k(Z,Y,K2), X != Y, K=K1 + K2, contador_noiluminados(N), K <= N.

camino_menor(X,Y,K) :- conectado_k(X,Y,K), conectado_k(X1,Y1,K1), K <= K1. 

% 2 nodos, 2 arcos (ida y vuelta), +7 = 11 - 3
% 3 nodos, 4 arcos (ida y vuelta), +17 = 24 - 5
% 4 nodos, 6 arcos (ida y vuelta), +41 = 51 - 5
