import copy
import math

from solver import solver


# check if all constraints are filled
def check_is_finished(constraints_lengths):
    if len(constraints_lengths) == 0:
        return True
    return False


# checking uniqueness of value in the row and column of (row,col)
def is_unique(row, col, value, board, constraints):
    # check right of (row,col)
    for j in range(col + 1, len(board)):
        if board[row][j] == '#' or board[row][j] in constraints:
            break
        if board[row][j] == value:
            return False
    # check left of (row,col)
    for j in range(col - 1, -1, -1):
        if board[row][j] == '#' or board[row][j] in constraints:
            break
        if board[row][j] == value:
            return False
    # check down of (row,col)
    for i in range(row + 1, len(board)):
        if board[i][col] == '#' or board[i][col] in constraints:
            break
        if board[i][col] == value:
            return False
    # check up of (row,col)
    for i in range(row - 1, -1, -1):
        if board[i][col] == '#' or board[i][col] in constraints:
            break
        if board[i][col] == value:
            return False
    return True


# when constraint is filled remove it from constraints_lengths
def remove_constraint(constraint_name, constraint_direction, constraints_lengths):
    constraints_lengths.pop(tuple([constraint_name, constraint_direction]))


# return next constraint to be filled. for example (c1,down)
def next_constraint(constraints_lengths, constraints_domains):
    min_length = 100000000000
    min_constraint_name_and_direction = None
    for cs in constraints_lengths:
        temp = math.factorial(constraints_lengths[cs]) * len(constraints_domains[cs])
        if temp < min_length:
            min_length = temp
            min_constraint_name_and_direction = cs
    name = min_constraint_name_and_direction[0]
    direction = min_constraint_name_and_direction[1]
    return name, direction


# return list of lists which is domain of a constraint. for example [[1,2,3],[4,5,6]] for c1.right
def get_constraints_domains(name, direction, constraints_domains):
    return constraints_domains[tuple([name, direction])]


# return length of a remaining variable for a constraint. for example 3 for c1.right
def get_constraints_lengths(name, direction, constraints_lengths):
    return constraints_lengths[tuple([name, direction])]


# return constraint location. for example (0,1) for c1
def get_constraint_location(name, constraints_location):
    return constraints_location[name][0], constraints_location[name][1]


# return list of constraints effected by (i,j). for example [(c1,down),(c2,right)] for (0,1)
def get_constraints_effected(row, col, constraints_effected):
    return constraints_effected[tuple([row, col])]


# update domains of constraints effected by (i,j) and check if the domain is empty
def update_constraint_domains_and_lengths(constraints_domains, constraints_effected, constraints_lengths, row, col,
                                          number):
    # finds constraints effected by (row,col)
    # be aware that they are list of tuples like [(c1,down),(c2,right)]
    constraints = get_constraints_effected(row, col, constraints_effected)
    for constraint in constraints:
        constraints_lengths[constraint] -= 1
        if constraints_lengths[constraint] == 0:
            remove_constraint(constraint[0], constraint[1], constraints_lengths)
        domains = copy.deepcopy(constraints_domains[constraint])
        # iterate over domains of constraint
        for domain in domains:
            # if number is not in domain then remove it
            if number not in domain:
                constraints_domains[constraint].remove(domain)
                # if domain is empty then return False
        if len(constraints_domains[constraint]) == 0:
            return False
    return True


class forward_checking(solver):

    def solve(self, row, col, board, constraints_domains, constraints_lengths, constraint_name=None, direction=None,
              numbers=None):

        # end case
        if check_is_finished(constraints_lengths):
            self.board = board
            return True

        # case to find next constraint to be filled
        if row == -1 and col == -1:
            constraint_name, direction = next_constraint(constraints_lengths, constraints_domains)
            if direction == 'down':
                row, col = get_constraint_location(constraint_name, self.constraints_location)
                domains = get_constraints_domains(constraint_name, direction, constraints_domains)
                # iterate over domains of constraint
                for domain in domains:
                    copy_board = copy.deepcopy(board)
                    copy_constraints_domains = copy.deepcopy(constraints_domains)
                    # fix domain of constraint
                    copy_constraints_domains[tuple([constraint_name, direction])] = [domain]
                    copy_constraints_lengths = copy.deepcopy(constraints_lengths)
                    # send to fill constraint
                    if self.solve(row + 1, col, copy_board, copy_constraints_domains,
                                  copy_constraints_lengths, constraint_name, direction, numbers=domain):
                        return True
                return False

            if direction == 'right':
                row, col = get_constraint_location(constraint_name, self.constraints_location)
                domains = get_constraints_domains(constraint_name, direction, constraints_domains)
                # iterate over domains of constraint
                for domain in domains:
                    copy_board = copy.deepcopy(board)
                    copy_constraints_domains = copy.deepcopy(constraints_domains)
                    # fix domain of constraint
                    copy_constraints_domains[tuple([constraint_name, direction])] = [domain]
                    copy_constraints_lengths = copy.deepcopy(constraints_lengths)
                    # send to fill constraint
                    if self.solve(row, col + 1, copy_board, copy_constraints_domains,
                                  copy_constraints_lengths, constraint_name, direction, numbers=domain):
                        return True
                return False

        if direction == 'down':
            if row == len(board) or board[row][col] == '#' or board[row][col] in self.constraints:
                # send to next constraint
                return self.solve(-1, -1, board, constraints_domains, constraints_lengths)

            if board[row][col] != 0:
                # it has been filled before
                return self.solve(row + 1, col, board, constraints_domains, constraints_lengths, constraint_name,
                                  direction, numbers)

            elif board[row][col] == 0:
                # iterate over numbers in domain to fill the constraint
                for number in numbers:
                    if is_unique(row, col, number, board, self.constraints):
                        copy_board = copy.deepcopy(board)
                        copy_constraints_domains = copy.deepcopy(constraints_domains)
                        copy_constraints_lengths = copy.deepcopy(constraints_lengths)
                        # fill the constraint
                        copy_board[row][col] = number
                        # update domains of constraints effected by (row,col)
                        if update_constraint_domains_and_lengths(copy_constraints_domains, self.constraints_effected,
                                                                 copy_constraints_lengths, row, col, number):
                            # send to next constraint
                            if self.solve(row + 1, col, copy_board, copy_constraints_domains,
                                          copy_constraints_lengths, constraint_name, direction, numbers):
                                return True

                # if no number in domain can be filled then return False
                return False

        if direction == 'right':
            if col == len(board) or board[row][col] == '#' or board[row][col] in self.constraints:
                # send to next constraint
                return self.solve(-1, -1, board, constraints_domains, constraints_lengths)

            if board[row][col] != 0:
                # it has been filled before
                return self.solve(row, col + 1, board, constraints_domains, constraints_lengths, constraint_name,
                                  direction, numbers)

            elif board[row][col] == 0:
                # iterate over numbers in domain to fill the constraint
                for number in numbers:
                    if is_unique(row, col, number, board, self.constraints):
                        copy_board = copy.deepcopy(board)
                        copy_constraints_domains = copy.deepcopy(constraints_domains)
                        copy_constraints_lengths = copy.deepcopy(constraints_lengths)
                        # fill the constraint
                        copy_board[row][col] = number
                        # update domains of constraints effected by (row,col)
                        if update_constraint_domains_and_lengths(copy_constraints_domains, self.constraints_effected,
                                                                 copy_constraints_lengths, row, col, number):
                            # send to next constraint
                            if self.solve(row, col + 1, copy_board, copy_constraints_domains,
                                          copy_constraints_lengths, constraint_name, direction, numbers):
                                return True

                # if no number in domain can be filled then return False
                return False
