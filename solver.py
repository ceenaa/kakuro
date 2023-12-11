from domains import extract_domains


class solver:

    def __init__(self, board, constraints):
        self.board = board
        self.constraints = constraints
        self.constraints_location = self.generate_constraint_location()
        self.constraint_domains, self.constraints_lengths = self.generate_constraint_domains()
        self.constraints_effected = self.generate_constraints_effected()

    # generate location of constraints
    def generate_constraint_location(self):
        constraints_location = {
        }
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] in self.constraints:
                    constraints_location[self.board[i][j]] = (i, j)

        return constraints_location

    # generate length of constraints for ordering
    # and also generate domains for each constraint for backtracking
    def generate_constraint_domains(self):
        constraint_lengths = {}
        constraint_domains = {}
        for cs_name in self.constraints:
            row = self.constraints_location[cs_name][0]
            col = self.constraints_location[cs_name][1]
            if 'down' in self.constraints[cs_name]:
                length = 0
                for i in range(row+1, len(self.board)):
                    if self.board[i][self.constraints_location[cs_name][1]] == 0:
                        length += 1
                    else:
                        break
                constraint_lengths[tuple([cs_name, 'down'])] = length
                value = self.constraints[cs_name]['down']
                constraint_domains[tuple([cs_name, 'down'])] = extract_domains(value=value, length=length)

            if 'right' in self.constraints[cs_name]:
                length = 0
                for j in range(col+1, len(self.board)):
                    if self.board[self.constraints_location[cs_name][0]][j] == 0:
                        length += 1
                    else:
                        break
                constraint_lengths[tuple([cs_name, 'right'])] = length
                value = self.constraints[cs_name]['right']
                constraint_domains[tuple([cs_name, 'right'])] = extract_domains(value=value, length=length)

        return constraint_domains, constraint_lengths

    # for finding with constraints are effected on (i,j)
    # to change its domain of the constraints
    def generate_constraints_effected(self):
        constraints_effected = {}
        for cs_name in self.constraints:
            constraints_effected[cs_name] = []
            row = self.constraints_location[cs_name][0]
            col = self.constraints_location[cs_name][1]
            if 'down' in self.constraints[cs_name]:
                for i in range(row+1, len(self.board)):
                    if self.board[i][col] == '#' or self.board[i][col] in self.constraints:
                        break
                    if self.board[i][col] == 0:
                        if tuple([i, col]) not in constraints_effected:
                            constraints_effected[tuple([i, col])] = []
                        constraints_effected[tuple([i, col])].append(tuple([cs_name, 'down']))

            if 'right' in self.constraints[cs_name]:
                for j in range(col+1, len(self.board)):
                    if self.board[row][j] == '#' or self.board[row][j] in self.constraints:
                        break

                    if self.board[row][j] == 0:
                        if tuple([row, j]) not in constraints_effected:
                            constraints_effected[tuple([row, j])] = []
                        constraints_effected[tuple([row, j])].append(tuple([cs_name, 'right']))

        return constraints_effected



