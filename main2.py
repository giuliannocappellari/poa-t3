import sys
import threading

def main():
    import sys

    sys.setrecursionlimit(1 << 25)
    threading.stack_size(1 << 27)

    def solve():
        n = int(sys.argv[1])
        b = int(sys.argv[2])
        c = int(sys.argv[3])

        total_positions = n * n
        solutions = [0]

        board = [["." for _ in range(n)] for _ in range(n)]

        # Directions: N, NE, E, SE, S, SW, W, NW
        DIRECTIONS = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                      (1, 0), (1, -1), (0, -1), (-1, -1)]

        gang_positions = {"B": [], "C": []}

        def is_safe(row, col, gang):
            enemy_gang = "B" if gang == "C" else "C"
            n = len(board)

            for dr, dc in DIRECTIONS:
                r, c = row + dr, col + dc
                blocked = False
                while 0 <= r < n and 0 <= c < n:
                    cell = board[r][c]
                    if cell == ".":
                        pass
                    elif cell == gang:
                        if not blocked:
                            return False
                        else:
                            break
                    else:  # Enemy gang member
                        blocked = True
                    r += dr
                    c += dc
            return True

        def sees_at_least_two_enemies(row, col, gang):
            enemy_gang = "B" if gang == "C" else "C"
            n = len(board)
            count = 0

            for dr, dc in DIRECTIONS:
                r, c = row + dr, col + dc
                while 0 <= r < n and 0 <= c < n:
                    cell = board[r][c]
                    if cell == ".":
                        pass
                    elif cell == enemy_gang:
                        count += 1
                        break
                    else:  # Same gang
                        break
                    r += dr
                    c += dc
                if count >= 2:
                    return True  # Early exit
            return count >= 2

        def validate_board():
            for gang in ["B", "C"]:
                for row, col in gang_positions[gang]:
                    if not sees_at_least_two_enemies(row, col, gang):
                        return False
            return True

        def backtrack(index, b_left, c_left):
            if b_left == 0 and c_left == 0:
                if validate_board():
                    solutions[0] += 1
                return

            if index >= total_positions:
                return

            row, col = divmod(index, n)

            # Prune branches where remaining positions are insufficient
            remaining_positions = total_positions - index
            if b_left + c_left > remaining_positions:
                return

            # Prune branches where it's impossible to meet the enemy visibility constraint
            min_possible_enemies_seen = min(len(gang_positions["B"]), c_left) + min(len(gang_positions["C"]), b_left)
            if min_possible_enemies_seen < 2 * (b_left + c_left):
                return

            if board[row][col] == ".":
                # Try placing 'B'
                if b_left > 0 and is_safe(row, col, "B"):
                    board[row][col] = "B"
                    gang_positions["B"].append((row, col))
                    backtrack(index + 1, b_left - 1, c_left)
                    gang_positions["B"].pop()
                    board[row][col] = "."

                # Try placing 'C'
                if c_left > 0 and is_safe(row, col, "C"):
                    board[row][col] = "C"
                    gang_positions["C"].append((row, col))
                    backtrack(index + 1, b_left, c_left - 1)
                    gang_positions["C"].pop()
                    board[row][col] = "."

            # Skip current position
            backtrack(index + 1, b_left, c_left)

        backtrack(0, b, c)
        print(solutions[0])

    threading.Thread(target=solve).start()



if __name__ == "__main__":
    from time import time
    start = time()
    main()
    print(time() - start)
