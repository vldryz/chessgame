from Chess_classes import Game


if __name__ == '__main__':
    print('A game of chess begins.')
    game = Game()
    print(game.board)

    while True:
        if game.turn == 'W':
            print(f'White to move on Move {game.move_number}')
        else:
            print(f'Black to move on Move {game.move_number}')

        move = input('Enter your move: ')

        if not game.move(move):
            continue

        game.change_turn()

        # if the move is a check
        if game.board.check_if_check(game.turn):

            if game.turn == 'W':
                game.board.state[game.board.wk_pos[0]][game.board.wk_pos[1]].is_checked = True
            else:
                game.board.state[game.board.bk_pos[0]][game.board.bk_pos[1]].is_checked = True

            # checkmate if no available moves
            if not game.board.is_there_a_move(game.turn):
                print(game.board)
                if game.turn == 'W':
                    print("White checkmated, Black won!")
                    break
                else:
                    print("Black checkmated, White won!")
                    break

            print(f"{game.turn} king is in check")

        # if the move is not a check
        else:
            if game.turn == 'W':
                game.board.state[game.board.wk_pos[0]][game.board.wk_pos[1]].is_checked = False
            else:
                game.board.state[game.board.bk_pos[0]][game.board.bk_pos[1]].is_checked = False

            # if no available moves then it is a stalemate
            if not game.board.is_there_a_move(game.turn):
                print(game.board)
                print("Stalemate, it's a draw!")
                break

        if game.turn == 'W':
            game.increment_move()

        print(game.board)
