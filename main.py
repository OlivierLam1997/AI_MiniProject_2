from collections import namedtuple

import csp


class Problem(csp.CSP):
    Timetable_slot = namedtuple('Timetable_slot', 'date, time')
    Weekly_class = namedtuple('Weekly_class', 'course, kind, index')
    Association = namedtuple('Association', 'student, course')
    Timetable_slot_room = namedtuple('Timetable_slot_room', 'date, time, room')

    def __init__(self, fh):

        # Place here your code to load problem from opened file object fh and
        T, W, Assoc, TR = []

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
                    Assoc.append(self.Association(elem[0], elem[1]))
            else:
                raise ValueError('Invalid file input !')

        for t in T:
            for r in R:
                TR.append(self.Timetable_slot_room(t.date, t.time, r))

        self.T = T
        self.W = W
        self.Assoc = Assoc
        self.TR = TR

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

        neighbors = {}
        for w1 in W:
            for w2 in W:
                if w1 != w2:
                    if w2 not in neighbors[w1]:
                        neighbors[w1].append(w2)
                    if w1 not in neighbors[w2]:
                        neighbors[w2].append(w1)

        self.solution = {}

        super().__init__(variables, domains, neighbors, self.constraints_function)

    def constraints_function(self, A, a, B, b):
        firstConstraint, secondConstraint, thirdConstraint = True

        if (A != B):
            if (a.date == b.date and a.time == b.time):
                firstConstraint = a.room != b.room

                for studentA, courseA in self.Assoc.items():
                    if courseA == A.course:
                        for studentB, courseB in self.Assoc.items():
                            if courseB == B.course:
                                secondConstraint = secondConstraint and (studentA != studentB)

        if (A.course == B.course) and (A.kind == B.kind) and (A.index != B.index):
            thirdConstraint = a.date != b.date

        return firstConstraint and secondConstraint and thirdConstraint

    def dump_solution(self, fh):
        for s in self.solution:
            fh.write(
                s.c + ',' + s.t + ',' + s.i + ' ' + self.solution[s].d + ',' + self.solution[s].t + ' ' + self.solution[
                    s].r + '\n')

    def cost_function(self):
        sum = 0
        for s in self.solution:
            sum += self.solution[s].time
        return sum


# def function(self,): function that calls csp.backtraking

def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)

    p.solution = csp.backtracking_search(p, csp.first_unassigned_variable,
                                         csp.unordered_domain_values,
                                         csp.no_inference)
    # p.function that calls
    p.dump_solution(output_file)


p = Problem(open("input.txt"))
print(p.variables)
