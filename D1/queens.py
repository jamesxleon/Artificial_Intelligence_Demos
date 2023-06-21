def n_queens(N):
    def solve(queens, xy_dif, xy_sum):
        p = len(queens)
        if p == N:
            result.append(queens)
            return None
        for q in range(N):
            #print("q: {q}, p: {p}, queens: {queens}, xy_dif: {xy_dif}, xy_sum: {xy_sum}".format(q=q, p=p, queens=queens, xy_dif=xy_dif, xy_sum=xy_sum))
            if q not in queens and p-q not in xy_dif and p+q not in xy_sum:
                solve(queens+[q], xy_dif+[p-q], xy_sum+[p+q])

    result = []
    solve([],[],[])
    return result

def draw_board(queen_positions):
    board = []
    for i in range(len(queen_positions)):
        row = []
        for j in range(len(queen_positions)):
            if j == queen_positions[i]:
                row.append('Q')
            else:
                row.append('.')
        board.append(row)
    return board

def draw_boards(queen_positions):
    boards = []
    for queen_position in queen_positions:
        boards.append(draw_board(queen_position))
    return boards

solutions = n_queens(8)

for solution in solutions:
    print(solution)
    print()
    board = draw_board(solution)
    for row in board:
        print(' '.join(row))
    print()

#puedo encontrar las siguientes soluciones posibles