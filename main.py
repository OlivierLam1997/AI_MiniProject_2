from collections import namedtuple
from copy import deepcopy
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
            splited_line = l.split()
            splited_line.pop(0)
            if firstChar == 'T':
                for elem in splited_line:
                    splited_elem = elem.split(',')
                    T.append(self.Timetable_slot(splited_elem[0], splited_elem[1]))

            elif firstChar == 'R':
                R = splited_line
            elif firstChar == 'S':
                S = splited_line
            elif firstChar == 'W':
                for elem in splited_line:
                    splited_elem = elem.split(',')
                    W.append(self.Weekly_class(splited_elem[0], splited_elem[1], splited_elem[2]))
            elif firstChar == 'A':
                for elem in splited_line:
                    splited_elem = elem.split(',')
                    Assoc.append(self.Association(splited_elem[0], splited_elem[1]))
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

        for w in W:
            W1 = deepcopy(W)
            W1.remove(w)
            neighbors[w] = W1

        self.solution = {}

        super().__init__(variables, domains, neighbors, self.constraints_function)

    def constraints_function(self, A, a, B, b):
        firstConstraint = True
        secondConstraint = True
        thirdConstraint = True

        if (A != B):
            if (a.date == b.date and a.time == b.time):
                firstConstraint = a.room != b.room

                for studentA, courseA in dict(self.Assoc).items():
                    if courseA == A.course:
                        for studentB, courseB in dict(self.Assoc).items():
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


solve(open("input.txt"), open("output.txt"))