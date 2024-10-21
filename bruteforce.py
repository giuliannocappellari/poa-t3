import itertools
import sys


def get_positions(n):
    return [(i, j) for i in range(n) for j in range(n)]


def create_board(n):
    return [["." for _ in range(n)] for _ in range(n)]


def place_pistoleiros(board, positions, assignment):
    for (row, col), quadrilha in zip(positions, assignment):
        board[row][col] = quadrilha


def is_valid_position(board, row, col, quadrilha):
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
                break
            r += dr
            c += dc
    return True


def pistoleiro_sees_two_enemies(board, row, col, quadrilha):
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


def is_valid_board(board, positions):
    for row, col in positions:
        quadrilha = board[row][col]
        if not is_valid_position(board, row, col, quadrilha):
            return False
        if not pistoleiro_sees_two_enemies(board, row, col, quadrilha):
            return False
    return True


def main():
    import time

    n = int(sys.argv[1])
    b = int(sys.argv[2])
    c = int(sys.argv[3])

    total_cells = n * n
    total_pistoleiros = b + c

    if total_pistoleiros > total_cells:
        print(0)
        return

    positions = get_positions(n)
    solutions = 0

    start_time = time.time()

    # Gerar todas as combinações possíveis de posições para os pistoleiros
    position_combinations = itertools.combinations(positions, total_pistoleiros)

    for pos_comb in position_combinations:
        # Gerar todas as maneiras de distribuir os pistoleiros entre as quadrilhas
        assignments = itertools.permutations(["B"] * b + ["C"] * c)

        # Usar set para evitar verificações duplicadas
        assignments_checked = set()

        for assignment in assignments:
            if assignment in assignments_checked:
                continue
            assignments_checked.add(assignment)

            board = create_board(n)
            place_pistoleiros(board, pos_comb, assignment)

            if is_valid_board(board, pos_comb):
                solutions += 1

    end_time = time.time()
    print(solutions)
    print(f"Tempo total: {end_time - start_time} segundos")


if __name__ == "__main__":
    main()
