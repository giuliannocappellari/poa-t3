import sys
from copy import deepcopy

solutions_set = set()


def hash_board(board):
    list_of_tuples = tuple(tuple(inner_list) for inner_list in board)
    return list_of_tuples


def create_board(n):
    return [["." for _ in range(n)] for _ in range(n)]


def is_safe(board, row, col, quadrilha):
    n = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        blocked = False
        while 0 <= r < n and 0 <= c < n:
            cell = board[r][c]
            if cell == ".":
                r += dr
                c += dc
                continue
            elif cell == quadrilha:
                if not blocked:
                    return False
                else:
                    break
            else:
                blocked = True
            r += dr
            c += dc
    return True


def sees_at_least_two_enemies(board, row, col, quadrilha):
    n = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        while 0 <= r < n and 0 <= c < n:
            cell = board[r][c]
            if cell == ".":
                r += dr
                c += dc
                continue
            elif cell != quadrilha:
                count += 1
                break
            else:
                break
            r += dr
            c += dc
    return count >= 2


def validate_board(board):
    if hash_board(board) not in solutions_set:
        n = len(board)
        for row in range(n):
            for col in range(n):
                cell = board[row][col]
                if cell != ".":
                    if not sees_at_least_two_enemies(board, row, col, cell):
                        return
        solutions_set.add(hash_board(board))
        transforms(board)


def print_board(board, solution):
    print("-" * int(len(board[0]) * 4 / 2), solution, "-" * int(len(board[0]) * 4 / 2))
    for row in board:
        print(row)
    print("-" * (len(board[0]) * 5))


def transforms(board):
    n = len(board)

    def rotate(board):
        return [[board[n - j - 1][i] for j in range(n)] for i in range(n)]
    
    def mirror_matrix(board):
        # Mirror each row of the matrix by reversing it
        mirrored_board = [row[::-1] for row in board]
        return mirrored_board

    current_board = deepcopy(board)

    for _ in range(3):
        current_board = rotate(current_board)
        solutions_set.add(hash_board(current_board))

    mirrored_board = mirror_matrix(board)
    for _ in range(3):
        current_board = rotate(mirrored_board)
        solutions_set.add(hash_board(current_board))


def backtrack(board, b_left, c_left, total_positions, index):
    if b_left == 0 and c_left == 0:
        validate_board(board)
        return

    if index >= total_positions:
        return

    n = len(board)
    row, col = divmod(index, n)

    if board[row][col] == ".":
        # Tenta colocar um 'B'
        if b_left > 0 and is_safe(board, row, col, "B"):
            board[row][col] = "B"
            backtrack(board, b_left - 1, c_left, total_positions, index + 1)
            board[row][col] = "."

        # Tenta colocar um 'C'
        if c_left > 0 and is_safe(board, row, col, "C"):
            board[row][col] = "C"
            backtrack(board, b_left, c_left - 1, total_positions, index + 1)
            board[row][col] = "."

    # Pular a posição atual
    backtrack(board, b_left, c_left, total_positions, index + 1)


def main():
    from time import time

    start = time()
    n = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    board = create_board(n)
    total_positions = n * n
    backtrack(board, b, c, total_positions, 0)
    print(len(solutions_set))
    print(time() - start)


if __name__ == "__main__":
    main()
