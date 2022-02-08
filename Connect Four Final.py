class InvalidColumnError(Exception):
    pass


class FullColError(Exception):
    pass


def print_mat(matr):
    # Function to print the matrix in the required shape.
    for r in matr:
        print(r)


def check_column_choice(col_choice, cols):
    # Check if the user input matches the parameters of the given matrix.
    if not (0 <= col_choice <= cols):
        raise InvalidColumnError


def place_player(play_num, col_choice, mat):
    # Add the player number to the matrix on the requested column and return error if that col is full.
    row_inner = len(mat)
    # Go through the column until we get zero. Start bottom-up.
    for row_ind in range(row_inner - 1, -1, -1):
        current_el = mat[row_ind][col_choice]
        if current_el == 0:
            # As soon as we get zero, we turn the zero to the player number and return current row col.
            mat[row_ind][col_choice] = play_num
            return row_ind, col_choice
    # If column full:
    raise FullColError


def horizontal_player(mat, cols, person):
    # Check each row if someone won.
    to_win = 0
    for ro in range(len(mat)):
        to_win = 0
        for co in range(cols):
            if mat[ro][co] == person:
                to_win += 1
                if to_win == 4:
                    return person
            else:
                to_win = 0
    return False


def vertical_player(mat, cols, person):
    # Check each col if someone won.
    to_win_vert = 0
    for co in range(cols):
        to_win_vert = 0
        for ro in range(len(mat)):
            if mat[ro][co] == person:
                to_win_vert += 1
                if to_win_vert == 4:
                    return person
            else:
                to_win_vert = 0
    return False


def right_down_and_left_up(row, col, mat, person):
    # Check diagonal down-right and left-up to see if someone won.
    matches = 0
    steady_row = row
    steady_col = col
    current_loc = mat[row][col]
    winner = person
    while True:
        # Try to check if a diagonal space exists or if it is out of the range of the matrix.
        try:
            next_ = mat[row + 1][col + 1]
        except IndexError:
            break
        # If it exists and is also occupied by the same player, move your current location there and repeat step above.
        if current_loc == next_:
            matches += 1
            current_loc = next_
            row += 1
            col += 1
        else:
            # If it is a zero, break but keep how many matches you have had.
            break
        # If matches were 3, then there are 4 same symbols, which means victory.
        if matches == 3:
            return winner
    current_loc = mat[steady_row][steady_col]
    row = steady_row
    col = steady_col
    while True:
        # If you did not get enough matches above, do the same for the opposite diagonal.
        try:
            if row == 0 or col == 0:
                raise IndexError
            next_ = mat[row - 1][col - 1]
        except IndexError:
            break
        if current_loc == next_:
            matches += 1
            current_loc = next_
            row -= 1
            col -= 1
        else:
            break
        if matches == 3:
            return winner
    return False


def right_up_and_left_down(row, col, mat, person):
    # Check diagonal up-right and left-down to see if someone won.
    matches = 0
    steady_row = row
    steady_col = col
    current_loc = mat[row][col]
    winner = person
    while True:
        try:
            if row == 0:
                raise IndexError
            next_ = mat[row - 1][col + 1]
        except IndexError:
            break
        if current_loc == next_:
            matches += 1
            current_loc = next_
            row -= 1
            col += 1
        else:
            break
        if matches == 3:
            return winner
    current_loc = mat[steady_row][steady_col]
    row = steady_row
    col = steady_col
    while True:
        try:
            if col == 0:
                raise IndexError
            next_ = mat[row + 1][col - 1]
        except IndexError:
            break
        if current_loc == next_:
            matches += 1
            current_loc = next_
            row += 1
            col -= 1
        else:
            break
        if matches == 3:
            return winner
    return False


def is_winner(row, col, person, mat, cols):
    # Report the winner.
    possible_winner_horizontal = horizontal_player(mat, cols, person)
    possible_winner_vertical = vertical_player(mat, cols, person)
    possible_winner_right_down_left_up = right_down_and_left_up(row, col, mat, person)
    possible_winner_right_up_left_down = right_up_and_left_down(row, col, mat, person)
    if possible_winner_horizontal:
        return possible_winner_horizontal
    elif possible_winner_vertical:
        return possible_winner_vertical
    elif possible_winner_right_down_left_up:
        return possible_winner_right_down_left_up
    elif possible_winner_right_up_left_down:
        return possible_winner_right_up_left_down
    return False


row_count = 6
col_count = 7
# Create the matrix.
matrix = [[0 for col in range(col_count)] for row in range(row_count)]
print_mat(matrix)

player = 1
while True:
    # Make sure player 1 and 2 change turns.
    player = 2 if player % 2 == 0 else 1
    try:
        column_num = int(input(f"Player {player}, which column do you want to play?\n")) - 1
        print()
        check_column_choice(column_num, col_count - 1)
        row, col = place_player(player, column_num, matrix)
        print_mat(matrix)
        if is_winner(row, col, player, matrix, col_count):
            print(f"Player {player} is the winner. Congratulations!")
            break

    except FullColError:
        print("That column is now full. Choose another.")
        continue
    except InvalidColumnError:
        print(f"The column you have listed is not valid. Please enter a number between {1} and {col_count}.")
        continue
    except ValueError:
        print(f"Please enter a valid column number between {1} and {col_count}.")
        continue

    player += 1
