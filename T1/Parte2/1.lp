arco(a,b).
arco(b,c).
arco(b,e).
arco(e,f).

arco(c,a). %agregamos el ciclo

nodo(X) :- arco(X,Y).
nodo(Y) :- arco(X,Y).

maximo_arcos(M) :- M = #count{X,Y : arco(X,Y)}. %Se agrega un contador para la cantidad de arcos totales

camino(X,Y,Largo) :- arco(X,Y), Largo=1.
camino(X,Y,Largo) :- camino(X,Z,L1), camino(Z,Y,L2), maximo_arcos(M), Largo= L1+L2, Largo <= M. %Se agrega el limite M
