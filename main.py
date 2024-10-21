import sys


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
    n = len(board)
    for row in range(n):
        for col in range(n):
            cell = board[row][col]
            if cell != ".":
                if not sees_at_least_two_enemies(board, row, col, cell):
                    return False
    return True


def print_board(board, solution):
    print("-"*int(len(board[0])*4/2), solution, "-"*int(len(board[0])*4/2))
    for row in board:
        print(row)
    print("-"*(len(board[0])*5))


def backtrack(board, b_left, c_left, total_positions, index, solutions):
    if b_left == 0 and c_left == 0:
        if validate_board(board):
            solutions[0] += 1
            print_board(board, solutions[0])
        return

    if index >= total_positions:
        return

    n = len(board)
    row, col = divmod(index, n)

    if board[row][col] == ".":
        # Tentar colocar um 'B'
        if b_left > 0 and is_safe(board, row, col, "B"):
            board[row][col] = "B"
            backtrack(board, b_left - 1, c_left, total_positions, index + 1, solutions)
            board[row][col] = "."

        # Tentar colocar um 'C'
        if c_left > 0 and is_safe(board, row, col, "C"):
            board[row][col] = "C"
            backtrack(board, b_left, c_left - 1, total_positions, index + 1, solutions)
            board[row][col] = "."

    # Pular a posição atual
    backtrack(board, b_left, c_left, total_positions, index + 1, solutions)


def main():
    n = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    board = create_board(n)
    total_positions = n * n
    solutions = [0]
    backtrack(board, b, c, total_positions, 0, solutions)
    print(solutions[0])


if __name__ == "__main__":
    main()
