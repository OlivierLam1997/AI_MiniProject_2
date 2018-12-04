from collections import namedtuple

import csp


class Problem(csp.CSP):
    Timetable_slot = namedtuple('Timetable_slot', 'date, time')
    Weekly_class = namedtuple('Weekly_class', 'course, kind, index')
    Association = namedtuple('Association', 'student, course')
    Timetable_slot_room = namedtuple('Timetable_slot_room', 'date, time, room')

    def __init__(self, fh):

        # Place here your code to load problem from opened file object fh and
        T = []
        W = []
        Assoc = []
        TR = []

        for l in fh.readlines():
            firstChar = l[0]
            list = l.split()
            list.pop(0)
            if firstChar == 'T':
                for elem in list:
                    T.append(self.Timetable_slot(elem[0], elem[1]))

            elif firstChar == 'R':
                R = list
            elif firstChar == 'S':
                S = list
            elif firstChar == 'W':
                for elem in list:
                    elem.split(',')
                    W.append(self.Weekly_class(elem[0], elem[1], elem[2]))
            elif firstChar == 'A':
                for elem in list:
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
