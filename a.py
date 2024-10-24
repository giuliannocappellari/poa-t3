n = 3

def create_board(n):
    return [[".", "C", "B"], [".",".","."], [".",".",".",]]
    # return [["." for _ in range(n)] for _ in range(n)]

def is_safe(board, row, col, quadrilha):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        blocked = False
        while (0 <= r < n) and (0 <= c < n) and (not blocked):
            print(f"r {r} c {c}")
            cell = board[r][c]
            print(f"{cell}")
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

board = create_board(3)
is_safe(board, 0, 0, "B")