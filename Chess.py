import sys, pdb, copy,webbrowser
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        # WINDOW
        self.main_widget = qtw.QWidget()
        self.setCentralWidget(self.main_widget)
        self.setFixedSize(qtc.QSize(640, 640))
        # LIST AND DICT
        self.lst_2 = [qtw.QPushButton("") for j in range(64)]
        self.lst = [[self.lst_2[j] for j in range(k, k + 8)] for k in range(0, 64, 8)]
        self.dict = {}  # Dictionary of information of every box
        self.dict_index = {}  # Dictionary of Location of button in 2D array,row and column in tuple
        self.func = {
            'pawn': self.pawn_move,
            'king': self.king_move,
            'rock': self.rock_move,
            'bishop': self.bishop_move,
            'knight': self.knight_move,
            'queen': self.queen_move
        }
        # Layout
        self.main_widget.setLayout(qtw.QGridLayout())
        self.main_widget.layout().setContentsMargins(1, 1, 1, 1)
        self.main_widget.layout().setSpacing(0)
        # Important Variable
        self.pre_sender = ""
        self.valid_moves = []
        self.changed_background = {}
        self.turn = True
        self.pieces = {1 : [j for i in [6,7] for j in self.lst[i]],0 : [j for i in [0,1] for j in self.lst[i]]}
        self.castle_dict = {}
        self.undo_var = []
        # Status Bar
        self.setStatusBar(qtw.QStatusBar())
        self.statusBar().showMessage("Turn : White")
        self.statusBar_dict = {True : "White",False : "Black"}
        # File Menu
        self.file_menu = qtw.QMenuBar()
        self.game = self.file_menu.addMenu("Game")
        self.action_reset = self.game.addAction("New Game",self.reset)
        self.game.addAction(self.action_reset)
        self.action_reset.setShortcut('Ctrl+N')
        self.action_undo = self.game.addAction("Undo",self.undo)
        self.action_undo.setShortcut("Ctrl+Z")
        self.action_redo = self.game.addAction("Redo",self.redo)
        self.action_redo.setShortcut("Ctrl+Y")
        self.setMenuBar(self.file_menu)
        self.action_redo.setDisabled(True)
        self.action_undo.setDisabled(True)

        other = self.file_menu.addMenu("Other")
        other.addAction("Help",lambda : webbrowser.open("https://www.chess.com/learn-how-to-play-chess"))
        other.addAction("About",lambda : qtw.QMessageBox.information(self,"About",f"Created By : Ajeem Ahmad \n Email : Ahmedazim7804@gmail.com \n Phone : "
                                                                                  f"9315082027"))

        # Designing Board
        self.design_board()  # Designing the board by function design_board()
        for i in self.lst_2:
            i.clicked.connect(self.choose)

    def design_board(self):

        for k, piece_lst in enumerate(self.lst, 0):
            for l, piece in enumerate(piece_lst, 0):
                self.main_widget.layout().addWidget(piece,k,l)
                piece.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
                piece.setIconSize(qtc.QSize(60, 60))
                self.dict[piece] = {"piece": "", "color": "", "icon": "", "index": (k, l)}
                self.dict_index[(k, l)] = {"piece": "", "color": "", "icon": "", "button": piece}

                if (l + k) % 2 == 0:
                    piece.setStyleSheet("background-color : #283747")
                else:
                    piece.setStyleSheet("background-color : #FFFFFF")

        # Setting Piece to thier position

        for j, i in enumerate(self.lst[1], 0):
            self.dict[i] = {'first_move': True, "piece": "pawn", "color": 0, "icon": "Icons\\pawn_black.png", 'index': (1, j)}
            self.dict_index[(1, j)] = {'first_move': True, "piece": "pawn", "color": 0, "icon": "Icons\\pawn_black.png",
                                       'button': i}

        for j, i in enumerate(self.lst[6], 0):
            self.dict[i] = {'first_move': True, "piece": "pawn", "color": 1, "icon": "Icons\\pawn_white.png", 'index': (6, j)}
            self.dict_index[(6, j)] = {'first_move': True, "piece": "pawn", "color": 1, "icon": "Icons\\pawn_white.png",
                                       'button': i}

        # Rock
        self.dict[self.lst[0][0]] = {"piece": "rock", "color": 0,'move' : 0, "icon": "Icons\\rock_black.png", 'index': (0, 0)}
        self.dict_index[(0, 0)] = {"piece": "rock", "color": 0,'move' : 0,"icon": "Icons\\rock_black.png", 'button': self.lst[0][0]}
        self.dict[self.lst[0][7]] = {"piece": "rock", "color": 0,'move' : 0, "icon": "Icons\\rock_black.png", 'index': (0, 7)}
        self.dict_index[(0, 7)] = {"piece": "rock", "color": 0,'move' : 0, "icon": "Icons\\rock_black.png", 'button': self.lst[0][7]}

        self.dict[self.lst[7][0]] = {"piece": "rock", "color": 1,'move' : 0, "icon": "Icons\\rock_white.png", 'index': (7, 0)}
        self.dict_index[(7, 0)] = {"piece": "rock", "color": 1,'move' : 0, "icon": "Icons\\rock_white.png", 'button': self.lst[7][0]}
        self.dict[self.lst[7][7]] = {"piece": "rock", "color": 1,'move' : 0, "icon": "Icons\\rock_white.png", 'index': (7, 7)}
        self.dict_index[(7, 7)] = {"piece": "rock", "color": 1,'move' : 0, "icon": "Icons\\rock_white.png", 'button': self.lst[7][7]}

        # knight
        self.dict[self.lst[0][1]] = {"piece": "knight", "color": 0, "icon": "Icons\\knight_black.png", 'index': (0, 1)}
        self.dict_index[(0, 1)] = {"piece": "knight", "color": 0, "icon": "Icons\\knight_black.png", 'button': self.lst[0][1]}
        self.dict[self.lst[0][6]] = {"piece": "knight", "color": 0, "icon": "Icons\\knight_black.png", 'index': (0, 6)}
        self.dict_index[(0, 6)] = {"piece": "knight", "color": 0, "icon": "Icons\\knight_black.png", 'button': self.lst[0][6]}

        self.dict[self.lst[7][1]] = {"piece": "knight", "color": 1, "icon": "Icons\\knight_white.png", 'index': (7, 1)}
        self.dict_index[(7, 1)] = {"piece": "knight", "color": 1, "icon": "Icons\\knight_white.png", 'button': self.lst[7][1]}
        self.dict[self.lst[7][6]] = {"piece": "knight", "color": 1, "icon": "Icons\\knight_white.png", 'index': (7, 6)}
        self.dict_index[(7, 6)] = {"piece": "knight", "color": 1, "icon": "Icons\\knight_white.png", 'button': self.lst[7][6]}

        # Bishop
        self.dict[self.lst[0][2]] = {"piece": "bishop", "color": 0, "icon": "Icons\\bishop_black.png", 'index': (0, 2)}
        self.dict_index[(0, 2)] = {"piece": "bishop", "color": 0, "icon": "Icons\\bishop_black.png", 'button': self.lst[0][2]}
        self.dict[self.lst[0][5]] = {"piece": "bishop", "color": 0, "icon": "Icons\\bishop_black.png", 'index': (0, 5)}
        self.dict_index[(0, 5)] = {"piece": "bishop", "color": 0, "icon": "Icons\\bishop_black.png", 'button': self.lst[0][5]}

        self.dict[self.lst[7][2]] = {"piece": "bishop", "color": 1, "icon": "Icons\\bishop_white.png", 'index': (7, 2)}
        self.dict_index[(7, 2)] = {"piece": "bishop", "color": 1, "icon": "Icons\\bishop_white.png", 'button': self.lst[7][2]}
        self.dict[self.lst[7][5]] = {"piece": "bishop", "color": 1, "icon": "Icons\\bishop_white.png", 'index': (7, 5)}
        self.dict_index[(7, 5)] = {"piece": "bishop", "color": 1, "icon": "Icons\\bishop_white.png", 'button': self.lst[7][5]}

        # King
        self.dict[self.lst[0][4]] = {"piece": "king", "color": 0,'move' : 0, "icon": "Icons\\king_black.png", 'index': (0, 4)}
        self.dict_index[(0, 4)] = {"piece": "king", "color": 0,'move' : 0, "icon": "Icons\\king_black.png", 'button': self.lst[0][4]}

        self.dict[self.lst[7][4]] = {"piece": "king", "color": 1,'move' : 0, "icon": "Icons\\king_white.png", 'index': (7, 4)}
        self.dict_index[(7, 4)] = {"piece": "king", "color": 1,'move' : 0, "icon": "Icons\\king_white.png", 'button': self.lst[7][4]}

        # Queen
        self.dict[self.lst[0][3]] = {"piece": "queen", "color": 0, "icon": "Icons\\queen_black.png", 'index': (0, 3)}
        self.dict_index[(0, 3)] = {"piece": "queen", "color": 0, "icon": "Icons\\queen_black.png", 'button': self.lst[0][3]}

        self.dict[self.lst[7][3]] = {"piece": "queen", "color": 1, "icon": "Icons\\queen_white.png", 'index': (7, 3)}
        self.dict_index[(7, 3)] = {"piece": "queen", "color": 1, "icon": "Icons\\queen_white.png", 'button': self.lst[7][3]}

        for i in self.dict.keys():
            i.setIcon(qtg.QIcon(self.dict[i]['icon']))

    def choose(self):
        self.background_color('reset')
        piece = self.sender()
        if self.pre_sender == piece:
            self.pre_sender = ""

        if self.pre_sender:
            if self.dict[piece]['piece']:
                if self.dict[piece]['color'] != self.dict[self.pre_sender]['color']:
                    self.process(piece, self.pre_sender)
                else:
                    self.ready(piece)
            elif not self.dict[piece]['piece']:
                self.process(piece, self.pre_sender)
        elif self.dict[piece]['piece']:
            self.ready(piece)
        elif not self.dict[piece]['piece']:
            return

    def update_icon(self):
        for i in self.dict.keys():
            i.setIcon(qtg.QIcon(self.dict[i]['icon']))

    def ready(self, piece):
        if self.turn and self.dict[self.sender()]['color']:
            pass
        elif not self.turn and not self.dict[self.sender()]['color']:
            pass
        else:
            self.statusBar().showMessage(f"{self.statusBar_dict[self.turn]}'s Turn")
            return
        self.pre_sender = self.sender()
        self.valid_moves = self.move_generator(piece)
        self.before_moves(self.pre_sender,self.valid_moves)
        # ------------For Castling---------------------
        if self.dict[self.pre_sender]['piece'] == 'king' and self.dict[self.pre_sender]['move'] == 0:
            for r in [0,7]:
                for c,d in [(3,2),(5,6)]:
                    if self.dict_index[r,c]['button'] not in self.valid_moves:
                        try:
                            self.valid_moves.remove(self.dict_index[r,d]['button'])
                        except ValueError:
                            pass
        # ---------------------------------------------
        self.background_color('change')

    def process(self, box, piece):
        self.action_undo.setDisabled(False)
        self.undo_var = []
        self.undo_var.append(piece)
        self.undo_var.append(box)

        if box not in self.valid_moves:
            return

        self.background_color('reset')

        index = self.pieces[self.dict[piece]['color']].index(piece)
        self.pieces[self.dict[piece]['color']].remove(piece)
        self.pieces[self.dict[piece]['color']].insert(index,box)

        self.change_dict(piece,box)
        # ----For Pawn,king,rock Only----
        if self.dict[box]['piece'] == 'pawn':
            self.dict[box]['first_move'] = False
            if self.dict[box]['index'][0] == 0 or self.dict[box]['index'][0] == 7:
                self.promotion(box)
        elif self.dict[box]['piece'] == 'rock':
            self.dict[box]['move'] = self.dict[box]['move'] + 1
            self.dict_index[self.dict[box]['index']]['move'] = self.dict[box]['move'] + 1
        elif self.dict[box]['piece'] == 'king':
            self.dict[box]['move'] = self.dict[box]['move'] + 1
            self.dict_index[self.dict[box]['index']]['move'] = self.dict[box]['move'] + 1

        self.update_icon()
        self.update_self_pieces(self.dict[box]['color'])
        if self.after_moves(self.dict[box]['color']) == 'checkmate':
            self.reset()
            return
        self.draw(self.dict[box]['color'])
        self.pre_sender = ""
        self.turn = not(self.turn)
        self.statusBar().showMessage(f"Turn : {self.statusBar_dict[self.turn]}")

    def update_self_pieces(self,color):
        # To update self.pieces after a opponent piece captured
        lst = []
        for i in self.pieces[not(color)]:
            if self.dict[i]['color'] == color or self.dict[i]['color'] == '':
                lst.append(i)
        for i in lst:
            self.pieces[not(color)].remove(i)

    def background_color(self, a):
        if a == 'change':
            for i in self.valid_moves:
                if self.dict[i]['piece']:
                    if self.dict[i]['color'] != self.dict[self.pre_sender]['color']:
                        self.changed_background[i] = i.styleSheet()
                        i.setStyleSheet("background-color : #EE4A4A")
                else:
                    i.setIconSize(qtc.QSize(40, 40))
                    i.setIcon(qtg.QIcon("Icons\\dot.png"))
        elif a == 'reset':
            for i in self.valid_moves:
                if not self.dict[i]['piece']:
                    i.setIconSize(qtc.QSize(60, 60))
                    i.setIcon(qtg.QIcon(""))
            for i in self.changed_background.keys():
                i.setStyleSheet(self.changed_background[i])

    def change_dict(self,piece,box):
        box_index = self.dict[box]['index']
        piece_index = self.dict[piece]['index']
        # -----------For Castling-----------------
        if self.dict[piece]['piece'] == 'king' and box in self.castle_dict and self.dict[piece]['move'] == 0:
            r = self.castle_dict[box][0]
            c = self.castle_dict[box][1]
            i = self.castle_dict[box][2]
            rock = self.dict_index[r,c]['button']
            place = self.dict_index[r,i]['button']
            if sys._getframe().f_back.f_code.co_name == 'process':
                index = self.pieces[self.dict[rock]['color']].index(rock)
                self.pieces[self.dict[rock]['color']].remove(rock)
                self.pieces[self.dict[rock]['color']].insert(index,place)
            self.castle(rock,place)
            if sys._getframe().f_back.f_code.co_name == 'process':
                self.castle_dict = {}
        # ----------------------------------------

        if self.dict[piece]['piece'] == 'pawn':
            self.dict[box]['first_move'] = self.dict[piece]['first_move']
            self.dict_index[box_index]['first_move'] = self.dict_index[piece_index]['first_move']
        elif self.dict[piece]['piece'] == 'rock':
            self.dict[box]['move'] = self.dict[piece]['move']
            self.dict_index[box_index]['move'] = self.dict_index[piece_index]['move']
        elif self.dict[piece]['piece'] == 'king':
            self.dict[box]['move'] = self.dict[piece]['move']
            self.dict_index[box_index]['move'] = self.dict_index[piece_index]['move']

        self.dict[box]['piece'] = self.dict[piece]['piece']
        self.dict[box]['color'] = self.dict[piece]['color']
        self.dict[box]['icon'] = self.dict[piece]['icon']
        self.dict_index[box_index]['piece'] = self.dict_index[piece_index]['piece']
        self.dict_index[box_index]['color'] = self.dict_index[piece_index]['color']
        self.dict_index[box_index]['icon'] = self.dict_index[piece_index]['icon']
        self.dict[piece] = {"piece": "", "color": "", "icon": "", 'index': piece_index}
        self.dict_index[piece_index] = {"piece": "", "color": "", "icon": "", 'button': piece}

    def move_generator(self,piece):
        piece_name = self.dict[piece]['piece']
        r = self.dict[piece]['index'][0];
        c = self.dict[piece]['index'][1]
        return self.func[piece_name](piece,r,c)

    def pawn_move(self, piece, r, c):
        moves = []
        if r == 0 or r == 7:
            return moves
        if self.dict[piece]['color']:
            sign = -1
        else:
            sign = 1
        max = 2
        if self.dict[piece]['first_move']:
            max = 3
        for i in range(1, max):
            if self.dict_index[(r + i * sign, c)]['piece']:
                break
            else:
                moves.append(self.dict_index[(r + i * sign, c)]['button'])
        try:
            if self.dict_index[(r + 1 * sign, c + 1)]['piece'] and self.dict_index[r + 1 * sign, c + 1]['color'] != \
                    self.dict_index[r, c]['color']:
                moves.append(self.dict_index[(r + 1 * sign, c + 1)]['button'])
        except KeyError:
            pass
        try:
            if self.dict_index[(r + 1 * sign, c - 1)]['piece'] and self.dict_index[r + 1 * sign, c - 1]['color'] != \
                    self.dict_index[r, c]['color']:
                moves.append(self.dict_index[(r + 1 * sign, c - 1)]['button'])
        except KeyError:
            pass

        return moves

    def rock_move(self, piece, r, c):
        moves = []
        i = 0
        for s in [-1, 1]:
            for k in ['(r+i*s,c)', '(r,c+i*s)']:
                try:
                    for i in range(1, 8):
                        index = eval(k)
                        if self.dict_index[index]['piece']:
                            if self.dict_index[index]['color'] != self.dict_index[(r, c)]['color']:
                                moves.append(self.dict_index[index]['button'])
                                break
                            else:
                                break
                        else:
                            moves.append(self.dict_index[index]['button'])
                except KeyError:
                    continue
        return moves

    def bishop_move(self, piece, r, c):
        moves = []
        for r_sign in [1, -1]:
            for c_sign in [1, -1]:
                try:
                    for i in range(1, 8):
                        if self.dict_index[r + i * r_sign, c + i * c_sign]['piece']:
                            if self.dict_index[r, c]['color'] != self.dict_index[r + i * r_sign, c + i * c_sign][
                                'color']:
                                moves.append(self.dict_index[r + i * r_sign, c + i * c_sign]['button'])
                                break
                            else:
                                break
                        else:
                            moves.append(self.dict_index[r + i * r_sign, c + i * c_sign]['button'])
                except KeyError:
                    continue
        return moves

    def knight_move(self, piece, r, c):
        moves = []
        for r_sign in [-1, 1]:
            for c_sign in [1, -1]:
                for i, j in [(1, 2), (2, 1)]:
                    try:
                        if self.dict_index[r + i * r_sign, c + j * c_sign]['piece']:
                            if self.dict_index[r, c]['color'] != self.dict_index[r + i * r_sign, c + j * c_sign][
                                'color']:
                                moves.append(self.dict_index[r + i * r_sign, c + j * c_sign]['button'])
                        else:
                            moves.append(self.dict_index[r + i * r_sign, c + j * c_sign]['button'])
                    except KeyError:
                        continue
        return moves

    def queen_move(self, piece, r, c):
        moves = self.rock_move(piece, r, c)
        moves.extend(self.bishop_move(piece,r,c))
        return moves

    def king_move(self, piece, r, c):
        moves = []
        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                if i == 0 and j == 0: continue
                try:
                    if self.dict_index[r + i, c + j]['piece']:
                        if self.dict_index[r + i, c + j]['color'] != self.dict_index[r, c]['color']:
                            moves.append(self.dict_index[r + i, c + j]['button'])
                    else:
                        moves.append(self.dict_index[r + i, c + j]['button'])
                except KeyError:
                    continue
        # ---------------------For Castling------------------------
        if self.dict[piece]['move'] == 0:
            if self.dict[piece]['color']:
                r = 7
            for c,i,d in [(0,3,2),(7,5,6)]:
                if self.dict_index[r,c]['piece'] == 'rock':
                    if self.dict_index[r,c]['move'] == 0:
                        lst = self.move_generator(self.dict_index[r,c]['button'])
                        if self.dict_index[r,i]['button'] in lst:
                            self.castle_dict[self.dict_index[r,d]['button']] = (r,c,i)
                            moves.append(self.dict_index[r,d]['button'])
        return moves

    def castle(self,rock,box):
        self.change_dict(rock,box)

    def before_moves(self,piece,valid_moves):
        all_moves = {}
        color = self.dict[piece]['color']
        king_only = []
        name = self.dict[piece]['piece']

        for i in valid_moves:
            dict = copy.copy(self.dict[i])
            dict_index = copy.copy(self.dict_index[dict['index']])
            # ---------------For Castling-----------------
            if name == 'king' and i in self.castle_dict:
                index = self.castle_dict[i]
                r = index[0]
                c = index[1]
                z = index[2]
                rock_index = copy.copy(self.dict_index[r,c])
                rock_dict = copy.copy(self.dict[rock_index['button']])
                empty_index = copy.copy(self.dict_index[r,z])
                empty_dict = copy.copy(self.dict[empty_index['button']])
            # --------------------------------------------

            self.change_dict(piece,i)

            a = self.all_moves(color)
            all_moves[i] = a
            # --------For King------------
            if name == 'king':
                for j in a:
                    if self.dict[j]['piece'] == 'king' and self.dict[j]['color'] == color:
                        king_only.append(i)
            # ----------------------------
            self.change_dict(i,piece)

            self.dict[i] = dict
            self.dict_index[dict['index']] = dict_index

            # ------------For Castling--------------------
            if name == 'king' and i in self.castle_dict:
                self.dict_index[r,c] = rock_index
                self.dict[rock_index['button']] = rock_dict

                self.dict_index[r,z] = empty_index
                self.dict[empty_index['button']] = empty_dict
            # --------------------------------------------
        # -------For King-------------
        if name == 'king':
            king_only = set(king_only)
            for i in king_only:
                valid_moves.remove(i)
            return
        # ----------------------------

        for k in all_moves.keys():
            for j in all_moves[k]:
                if self.dict[j]['piece'] == 'king' and self.dict[j]['color'] == color:
                    valid_moves.remove(k)
                    break

    def after_moves(self,color):
        all_moves = self.all_moves(not(color))
        for i in all_moves:
            if self.dict[i]['piece'] == 'king' and self.dict[i]['color'] != color:
                qtw.QMessageBox.about(self,'',f'Check To {self.statusBar_dict[not(color)]}')
                if self.checkmate(color,'checkmate') == 'checkmate':
                    return 'checkmate'

    def all_moves(self,color):
        all_moves = []
        for i in self.lst_2:
            if self.dict[i]['color'] != color and self.dict[i]['color'] != '':
                moves = self.move_generator(i)
                all_moves.extend(moves)
        return all_moves

    def checkmate(self,color,arg):
        color = not(color)
        all_moves = []
        for i in self.lst_2:
            if self.dict[i]['color'] == color:
                moves = self.move_generator(i)
                self.before_moves(i,moves)
                all_moves.extend(moves)
        if len(all_moves) == 0:
            if arg == 'checkmate':
                qtw.QMessageBox.about(self,'',f'Checkmate To {self.statusBar_dict[color]}')
                return 'checkmate'
            else:
                qtw.QMessageBox.about(self,'','Game Draw')
                return 'draw'

    def draw(self,color):
        if self.checkmate(color,'draw') == 'draw':
            qtw.QMessageBox.about(self,'','Game Draw')
            self.reset()
            return

        draw_1 = False
        draw_2 = False

        if len(self.pieces[not(color)]) == 1:
            draw_1 = True
        elif len(self.pieces[not(color)]) == 2:
            a = [self.dict[i]['piece'] for i in self.pieces[not(color)]]
            if 'king' in a:
                if 'knight' in a or 'bishop' in a:
                    draw_1 = True
        elif len(self.pieces[not(color)]) == 3:
            a = [self.dict[i]['piece'] for i in self.pieces[not(color)]]
            if 'king' in a:
                if a.count('knight') == 2:
                    draw_1 = True

        if len(self.pieces[color]) == 1:
            draw_2 = True
        elif len(self.pieces[color]) == 2:
            a = [self.dict[i]['piece'] for i in self.pieces[color]]
            if 'king' in a:
                if 'knight' in a or 'bishop' in a:
                    draw_2 = True
        elif len(self.pieces[color]) == 3:
            a = [self.dict[i]['piece'] for i in self.pieces[color]]
            if 'king' in a:
                if a.count('knight') == 2:
                    draw_2 = True

        if draw_1 == draw_2 == True:
            qtw.QMessageBox.about(self,'',"Game Draw")
            self.reset()
            return

    def promotion(self,piece):
        dialog = qtw.QMessageBox()
        dialog.setText("\t\tConvert Pawn To")
        queen = qtw.QPushButton("Queen");queen.clicked.connect(lambda : self.promotion_2(piece,'queen'))
        rock = qtw.QPushButton("Rock");rock.clicked.connect(lambda : self.promotion_2(piece,'rock'))
        knight = qtw.QPushButton("Knight");knight.clicked.connect(lambda : self.promotion_2(piece,'knight'))
        bishop = qtw.QPushButton("Bishop");bishop.clicked.connect(lambda : self.promotion_2(piece,'bishop'))
        dialog.addButton(queen,qtw.QMessageBox.YesRole)
        dialog.addButton(rock,qtw.QMessageBox.NoRole)
        dialog.addButton(knight,qtw.QMessageBox.RejectRole)
        dialog.addButton(bishop,qtw.QMessageBox.ApplyRole)
        dialog.exec()

    def promotion_2(self,piece,name):
        color = self.dict[piece]['color']
        index = self.dict[piece]['index']
        self.dict[piece]['piece'] = name
        if name == 'queen':
            if color:
                self.dict[piece]['icon'] = 'Icons\\queen_white.png'
                self.dict_index[index]['icon'] = 'Icons\\queen_white.png'
            elif not color:
                self.dict[piece]['icon'] = 'Icons\\queen_black.png'
                self.dict_index[index]['icon'] = 'Icons\\queen_black.png'
        elif name == 'rock':
            if color:
                self.dict[piece]['icon'] = 'Icons\\rock_white.png'
                self.dict_index[index]['icon'] = 'Icons\\rock_white.png'
            elif not color:
                self.dict[piece]['icon'] = 'Icons\\rock_black.png'
                self.dict_index[index]['icon'] = 'Icons\\rock_black.png'
        elif name == 'knight':
            if color:
                self.dict[piece]['icon'] = 'Icons\\knight_white.png'
                self.dict_index[index]['icon'] = 'Icons\\knight_white.png'
            elif not color:
                self.dict[piece]['icon'] = 'Icons\\knight_black.png'
                self.dict_index[index]['icon'] = 'Icons\\knight_black.png'
        elif name == 'bishop':
            if color:
                self.dict[piece]['icon'] = 'Icons\\bishop_white.png'
                self.dict_index[index]['icon'] = 'Icons\\bishop_white.png'
            elif not color:
                self.dict[piece]['icon'] = 'Icons\\bishop_black.png'
                self.dict_index[index]['icon'] = 'Icons\\bishop_black.png'
        self.dict[piece].pop('first_move')
        self.dict_index[index].pop('first_move')

    def reset(self):
        self.dict = {}
        self.dict_index = {}
        self.pre_sender = ""
        self.valid_moves = []
        self.changed_background = {}
        self.turn = True
        self.pieces = {1 : [j for i in [6,7] for j in self.lst[i]],0 : [j for i in [0,1] for j in self.lst[i]]}
        self.castle_dict = {}
        self.undo_var = []
        self.design_board()

    def undo(self):
        piece = self.undo_var[1]
        box = self.undo_var[0]
        self.valid_moves = [box]
        self.process(box,piece)
        self.action_undo.setDisabled(True)
        self.action_redo.setDisabled(False)

    def redo(self):
        piece = self.undo_var[1]
        box = self.undo_var[0]
        self.valid_moves = [box]
        self.process(box,piece)
        self.action_redo.setDisabled(True)
        self.action_undo.setDisabled(False)

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())