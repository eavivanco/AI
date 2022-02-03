import sys
import os
import queue
import random

class Agent:
    def __init__(self, env):
        self.env = env
        self.x = env.init_x      # tamaño de la grilla
        self.y = env.init_y
        self.visited = set()     # celdas ya visitadas
        self.visited.add((self.x, self.y))
        self.frontier = set()    # al profesor le fue util mantener esta variable
        for n in env.neighbors(self.x, self.y):
            self.frontier.add(n)
        self.path = []
        self.path.append((self.env.init_x,self.env.init_y))            # self.path es el camino que estamos siguiendo
                                 # no es necesario que uses este atributo, pero al
                                 # profe le fue útil

        self.goalx = 1        # editar
        self.goaly = 1
        self.safe = []
        self.risky = []
        self.detected_wumpus = 0
        self.detected_pit = 0
        self.track_perceptions = []
        #self.safe.extend(self.env.neighbors(self.env.init_x, self.env.init_y))
        self.safe_area = [(0,2), (1, 2), (1,1)]



    # get_action(self, perceptions) supone que perceptions es una lista de
    # strings [s1,...,sn] donde si es sense_breeze(x,y) o sense_stench(x,y) para algúun x,y
    # debe retornar:
    #   - una tupla de la forma ('goto',x,y) para hacer que el agente se mueva a (x,y)
    #   - una tupla de la forma ('shoot',x,y) para hacer que el agente dispare a (x,y)
    #   - una tupla de la forma ('unsolvable') cuando el agente ha demostrado que el problema
    #     no tiene una solución segura
    def get_action(self, perceptions):
        def find_path(startx, starty, goalx, goaly, safe_area):
            # encuentra un camino entre (startx,starty) a (goalx,goaly)
            # pasando solo por celdas de safe_area

            if (startx, starty) == (goalx, goaly): #cuando llega a destino termina
                return True, []
            closed = set()
            fr = queue.Queue()
            fr.put((startx, starty, []))
            while not fr.empty():
                (x, y, path) = fr.get()
                closed.add((x,y))
                for (nx, ny) in self.env.neighbors(x, y):
                    if (nx, ny) in closed:
                        continue
                    newpath = path + [(nx, ny)]
                    if (nx, ny) == (goalx, goaly):
                        return True, newpath
                    else:
                        #print(f'esta es la safe rechazada {safe_area}')
                        #print(f'lo comapran con estas coord {(nx, ny)}')
                        if (nx, ny) in safe_area:
                            #print(f'pero esta entro {(nx, ny)}')
                            fr.put((nx, ny, newpath))
            return False, []


        def unsat_without(atom):
            # Consiedera completar e implementar este método
            # No es obligatorio que lo hagas, pero al profesor le fue útil.
            # Dado un cierto atom, arma un archivo extra.lp, el método retorna True
            # si y solo si el programa que resulta de considerar wumpus.lp y extra.lp
            # es tal que NO tiene modelos que no contienen a atom

            def get_models(filename):  # extrae los modelos desde filename
                f = open(filename, 'r')
                lines = f.readlines()
                lines = [l.strip() for l in lines]
                if 'SATISFIABLE' in lines:
                    answers = []
                    i = 0
                    while True:
                        while i < len(lines) - 1 and lines[i].find('Answer:', 0) == -1:
                            i += 1
                        if i == len(lines) - 1:
                            return answers
                        i += 1
                        answers.append(lines[i].split(' '))
                    return answers
                elif 'UNSATISFIABLE' in lines:
                    return []
                print(filename, 'no es un output legal de clingo')
                return []

            # COMPLETAR - aquí se eliminaron 13 líneas de la solución (incluyendo comentarios)
            fextra = open('extra.lp', 'w')
            fextra.write(extra)
            fextra.close()
            os.system('clingo -n 0 wumpus.lp extra.lp > out.txt 2> /dev/null')
            # si usas Windows, la siguiente línea debiera funcionar
            # os.system('clingo -n 0 wumpus.lp extra.lp > out.txt 2> NUL')
            models = get_models('out.txt')
            return models == []

        # COMPLETAR - aquí se eliminaron 29 líneas de la solución (incluyendo comentarios)

        ## ENCONTRAR EL GOAL

        ## TRADUCIR PELIGROS
        def clean_perceptions(perceptions):
            simple_perceptions = []
            carac_perceptions = []
            for p in perceptions:
                coo = []
                carac_coo = []
                for element in p:
                    if 'z' in element:
                        carac_coo.append('p')
                    if 'h' in element:
                        carac_coo.append('w')
                    if element.isnumeric():
                        coo.append(int(element))
                        carac_coo.append(int(element))
                simple_perceptions.append(tuple(coo))
                carac_perceptions.append(carac_coo)
            return simple_perceptions, carac_perceptions

        ## ENCONTRAR SAFE_AREA
        def check_area(past_risky,past_safe,current_x, current_y, current_neighbors, current_perceptions):
            ## se arma el area segura
            risk = 0
            if (current_x, current_y) not in past_safe:
                past_safe.append((current_x, current_y))
            simple_perceptions, carac_perceptions = clean_perceptions(current_perceptions)
            if len(simple_perceptions) == 0:
                past_safe.extend(current_neighbors) 
                #print('agregamos vecinos con lista vacia')
            else:
                for p in carac_perceptions:
                    if (p[0],p [1], p[2]) not in self.track_perceptions:
                        self.track_perceptions.append((p[0],p [1], p[2]))

                        print(f'esta es el tracker - {self.track_perceptions}')
                        if current_x == p[1] and current_y == p[2]:
                            risk +=1
                        if risk >= 1:
    
                            for nei in current_neighbors:
                                if nei not in self.path:
                                    if (p[0], nei[0], nei[1]) not in past_risky:
                                        past_risky.append((p[0], nei[0], nei[1]))
                                        print(f'agregamos vecinos peligrosos{(p[0], nei[0], nei[1])}')
                                        print(f'esta es la past risky{past_risky}')
                if risk == 0:
                    for nei in current_neighbors:
                        if (nei[0], nei[1]) not in past_safe and ('w', nei[0], nei[1]) not in past_risky and ('p', nei[0], nei[1]) not in past_risky:
                            past_safe.append((nei[0], nei[1])) 
                            print(f'agregamos vecinos sin peligro - {(nei[0], nei[1])}')
                risk = 0
            return past_risky, past_safe
        
        def double_check(riskyA, riskyB, safe):
            #print(f' largo risky {len(riskyA)} - {riskyA}')
            if len(riskyA) > 1:
                for i in riskyA:
                    for j in riskyB:
                        if i[0] != j[0] and i[1] == j[1] and i[2] == j[2]:
                            riskyA.remove(i)
                            riskyB.remove(j)
                            safe.append((i[1],i[2]))
                            print(f'se elimino un peligro ({i[1]},{i[2]})')
                            print(f'asi quedo la risk -  {riskyA}')
            
            return riskyA, safe

        def check_final(total_pits, total_wumpus, riskyA, riskyB, carac_perceptions):
            #asegura la posicion de wumpus o pits y trackea los que quedan
            #print(f'este es risky {riskyA}')
            if len(riskyA) > 1:
                for tileA in riskyA:
                    strikes = 0
                    #print(f'esta es tile {tileA}')
                    strikes = 0
                    ktileA = tileA[0]
                    xtileA = tileA[1]
                    ytileA = tileA[2]
                    if ktileA == 'w' and self.detected_wumpus < total_wumpus:
                        for n in self.env.neighbors(xtileA, ytileA):
                            xnei = n[0]
                            ynei = n[1]
                            for tileB in riskyB:
                                ktileB = tileB[0]
                                xtileB = tileB[1]
                                ytileB = tileB[2]
                                if ktileB == 'w' and xtileB == xnei and ytileB == ynei:
                                    strikes =+1
                        if strikes >= 3:
                            self.detected_wumpus +=1
                            return 'shoot', xtileA, ytileA

                    if ktileA == 'p' and self.detected_pit < total_pits:
                        for n in self.env.neighbors(xtileA, ytileA):
                            xnei = n[0]
                            ynei = n[1]
                            for tileB in riskyB:
                                ktileB = tileB[0]
                                xtileB = tileB[1]
                                ytileB = tileB[2]
                                if ktileB == 'p' and xtileB == xnei and ytileB == ynei:
                                    strikes =+1
                        if strikes >= 3:
                            self.detected_pit += 1
                            return 'avoid', xtileA, ytileA
                
            return 'chill', 0, 0

        ## los que sean neigbors de perceptions y no estan visitados son peligrosos
        ## si no hay senal, es seguro

        if self.env.is_observable():
            nwumpus = self.env.get_num_wumpus()
            npits = self.env.get_num_pits()

        ### iteraciones
        simple_perceptions, carac_perceptions = clean_perceptions(perceptions)

        current_nei = self.env.neighbors(self.x, self.y)

        self.risky, self.safe = check_area(self.risky,self.safe, self.x, self.y, current_nei, perceptions)
        self.risky, self.safe = double_check(self.risky, self.risky, self.safe)
        obs_action, xobs, yobs = check_final(npits, nwumpus, self.risky, self.risky, carac_perceptions)

        print(f'esta es la safe {self.safe}')
        
        valido = False
        while not valido:
            temporal = random.choice(self.safe)
            xoption = temporal[0]
            yoption = temporal[1]
            if xoption != self.x or yoption != self.y:
                valido = True

        print(f'esta es la temporal {temporal}')
        if xoption != self.x or yoption != self.y: #doble confirmacion porque por alguna razon fallaba
            keep_moving, newpath = find_path(self.x, self.y, xoption, yoption, self.safe) #lo vamos a iterar por cada nei
        
            if keep_moving:
                for step in newpath:
                    if step is not (self.x, self.y) and step not in self.risky:
                        #print(f'keep_moving es True y es {newpath}')
                        msg = ('goto',step[0], step[1])
                        self.x, self.y = step
                        self.path.append(step)
                        #print(f'asi va el path {self.path}')
                        return msg
            elif not keep_moving:
                msg = ('unsolvable')
                return msg

        if obs_action == 'shoot':
            msg = ('shoot', xobs, yobs)
            return msg
















