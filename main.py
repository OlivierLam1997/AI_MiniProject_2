from collections import namedtuple

import csp


class Problem(csp.CSP):
    Timetable_slot = namedtuple('Timetable_slot', 'date, time')
    Weekly_class = namedtuple('Weekly_class', 'class, kind, index')
    Association = namedtuple('Association', 'student, class')
    Timetable_slot_room = namedtuple('Timetable_slot_room', 'date, time, room')

    def __init__(self, fh):

        # Place here your code to load problem from opened file object fh and
        T, W, A, TR = []
        for l in fh.readlines():
            firstChar = l[0]
            l.split().pop(0)
            if firstChar == 'T':
                for elem in l:
                    elem.split(',')
                    T.append(self.Timetable_slot(elem[0], elem[1]))

            elif firstChar == 'R':
                R = l
            elif firstChar == 'S':
                S = l
            elif firstChar == 'W':
                for elem in l:
                    elem.split(',')
                    W.append(self.Weekly_class(elem[0], elem[1], elem[2]))
            elif firstChar == 'A':
                for elem in l:
                    elem.split(',')
                    A.append(self.Association(elem[0], elem[1]))
            else:
                raise ValueError('Invalid file input !')

        for t in T:
            for r in R:
                TR.append(self.Timetable_slot_room(t.date, t.time, r))




        """position = []
        a = 0
        for i in range(len(list)):
            if len(list[i]) == 1:
                position.append(i)
                a += 1
        T = list[position[0] + 1:position[1]]
        R = list[position[1] + 1:position[2]]
        S = list[position[2] + 1:position[3]]
        W = list[position[3] + 1:position[4]]
        A = list[position[4] + 1:]

        # To compare the elements inside each tuple
        T_Aux = []
        for t in range(len(T)):
            T_Aux.append(T[t].split(','))
        T_tup = []
        for t in range(len(T_Aux)):
            T_tup.append(tuple(T_Aux[t]))

        W_Aux = []
        for w in range(len(W)):
            W_Aux.append(W[w].split(','))
        W_tup = []
        for w in range(len(W_Aux)):
            W_tup.append(tuple(W_Aux[w]))

        A_Aux = []
        for a in range(len(A)):
            A_Aux.append(A[a].split(','))
        A_tup = []
        for a in range(len(A_Aux)):
            A_tup.append(tuple(A_Aux[a]))

        variables = W
        # domains=[T,R]
        possible_values = []
        for t in range(len(T)):
            for r in range(len(R)):
                possible_values.append([T_tup[t], R[r]])

        domains = {}
        for v in range(len(variables)):
            domains[variables[v]] = possible_values

        #####################################################################
        types = {}
        classes = []
        for s in range(len(S)):
            for a in range(len(A_tup)):
                if S[s] == A_tup[a][0]:
                    classes.append(A_tup[a][1])
            types[S[s]] = classes
            classes = []

        for s in range(len(S)):
            for w in range(len(W_tup)):
                for t in range(len(types)):
                    if W_tup[w][0] == types[t]:
                        types[S[s]][t] = W_tup[w]
        """
        # set variables, domains, graph, and constraint_function accordingly

        variables = W
        domains = {}
        for var in variables:
            domains[var] = TR

        

        def constraints_function(A, a, B, b){

        }

    #       super().__init__(variables, domains, graph, constraints_function)

    def dump_solution(self, fh):


# Place here your code to write solution to opened file object fh
# solution1=[variables[1],domains[0][1],domains[1][0]]
# solution2=' '.join(solution1)


# def function(self,): function that calls csp.backtraking

def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)

    # p.function that calls
    p.dump_solution(output_file)
