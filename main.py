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
        lastestTimeSlot = 0

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

        # initialize the lastest timeslot
        for timeslot in T:
            if int(timeslot.time) >= int(lastestTimeSlot):
                lastestTimeSlot = int(timeslot.time)

        self.T = T
        self.W = W
        self.Assoc = Assoc
        self.TR = TR
        self.lastestTimeSlot = lastestTimeSlot

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

        constraint = True

        if (A != B):
            if (a.date == b.date and a.time == b.time):
                constraint = a.room != b.room and constraint

                for assocA in self.Assoc:
                    if assocA[1] == A.course:
                        for assocB in self.Assoc:
                            if assocB[1] == B.course:

                                constraint = constraint and assocA[0] != assocB[0]

        if (A.course == B.course) and (A.kind == B.kind) and (A.index != B.index):
            constraint = a.date != b.date and constraint

        constraint = constraint and int(a.time) <= self.lastestTimeSlot and int(b.time) <= self.lastestTimeSlot

#        print(A, a, B, b, constraint)
        return constraint

    def dump_solution(self, fh):
        for var, value in self.solution.items():
            fh.write(
                var.course + ',' + var.kind + ',' + var.index + ' ' + value.date + ',' + value.time + ' ' + value.room + '\n')

    def cost_function(self):
        latestTime = 0
        for var, value in self.solution.items():
            if value.time >= latestTime:
                latestTime = value.time
        return latestTime

# def function(self,): function that calls csp.backtraking

    def cspBacktrack(self, p):
        numberIteration = int(p.lastestTimeSlot)

        for i in range(numberIteration):
            p1 = deepcopy(p)
            p1.lastestTimeSlot = numberIteration - i
            p.solution = csp.backtracking_search(p1, csp.mrv, csp.lcv, csp.forward_checking)

            if p.solution == None:
                break
        return p



def solve(input_file, output_file):
    p = Problem(input_file)
    # Place here your code that calls function csp.backtracking_search(self, ...)

    p.cspBacktrack(p).dump_solution(output_file)

p = Problem(open("input.txt"))

solve(open("input.txt"), open("output.txt", "w"))