# ダウト
import random
import sys

# カードのスートと番号を定義(ジョーカーは無し)
suits = ('スペード', 'ハート', 'ダイヤ', 'クローバー')
numbers = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')

# テーブル上のカードリスト(伏せられている)
tablecards = []


# テーブル上のカードリストを示す(テスト時のみ使用)
def show_tablecards():
    print('テーブル上のカードリスト: ', end='')
    for card in tablecards:
        if card != tablecards[-1]:
            print(f'{card.suit}{card.number}', end=', ')
        else:
            print(f'{card.suit}{card.number}')


# カードクラス
class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number
        if self.number == 'A':
            self.value = 1
        elif self.number == 'J':
            self.value = 11
        elif self.number == 'Q':
            self.value = 12
        elif self.number == 'K':
            self.value = 13
        else:
            self.value = int(self.number)


# プレーヤークラス(スーパークラス)
class Player:
    def __init__(self, name):
        self.name = name
        self.cardlist = []

    # カードを受け取る
    def receive_card(self, card):
        self.cardlist.append(card)

    # 手札を示す(Computerクラスではテスト時のみ使用)
    def show_cardlist(self):
        self.cardlist.sort(key=lambda x: x.value)
        print(f'{self.name}の手札 ', end='')
        for i, card in enumerate(self.cardlist, 1):
            if card != self.cardlist[-1]:
                print(f'{i}:{card.suit}{card.number}', end=', ')
            else:
                print(f'{i}:{card.suit}{card.number}')

    # 以下、オーバーライド用メソッド群
    def decide_sheet(self):
        pass

    def decide_indexes(self):
        pass

    def put_cards(self):
        pass

    def call_doubt(self):
        pass


# 人間プレーヤークラス
class Human(Player):
    def __init__(self, name):
        super().__init__(name)

    # 出す枚数を決める
    def decide_sheet(self):
        # 50回以内に正しい入力がされると想定
        for i in range(50):
            sheet_input = input('何枚カードを出しますか？(1～4枚)->')
            if (sheet_input == '1'):
                break
            elif (sheet_input == '2' or sheet_input == '3' or
                  sheet_input == '4'):
                if int(sheet_input) <= len(self.cardlist):
                    break
                else:
                    print('手札の枚数以下の枚数にして下さい')
                    continue
            else:
                print('1～4までの整数を入力して下さい')
        else:
            print('50回以内に正しい入力が得られませんでした。終了します')
            sys.exit()
        return int(sheet_input)

    # テスト用
    def decide_sheet_test(self):
        sheet_test = input('何枚出しますか？')
        return int(sheet_test)

    # カードを出す位置を決める
    def decide_indexes(self, sheet):
        indexes = []
        # sheet回繰り返す
        for i in range(sheet):
            # 50回以内に
            for j in range(50):
                index_input = input('左から何番目のカードを出しますか？->')
                index = int(index_input)
                # 人間プレーヤーは1から数えるものとする
                if 1 <= index <= len(self.cardlist):
                    # ダブりがないか
                    for k in range(len(indexes)):
                        if (index - 1) == indexes[k]:
                            print('同じ位置のカードは選べません')
                            break
                    else:
                        indexes.append(index - 1)
                        break
                else:
                    print('手札の位置と対応する数字を入力して下さい')
            else:
                print('50回以内に正しい入力が得られませんでした。終了します')
                sys.exit()
        return indexes

    # カードを出す
    def put_cards(self, indexes):
        # 処理の都合で降順にソート
        sorted_indexes = sorted(indexes, reverse=True)
        putting_cards = []
        for index in sorted_indexes:
            putting_cards.append(self.cardlist[index])
            self.cardlist.pop(index)
        return putting_cards

    # ダウトと宣言
    def call_doubt(self):
        calling_input = input('ダウトの宣言をする場合はdを入力して下さい->')
        if calling_input == 'd':
            print(f'{self.name}はダウトの宣言をしました！')
            return True
        else:
            # print(f'{self.name}は宣言をしませんでした')
            return False


# コンピュータプレーヤークラス
class Computer(Player):
    def __init__(self, name):
        super().__init__(name)

    # 出す枚数を決める(当面は1枚とする)
    def decide_sheet(self):
        return 1

    # 出す位置を決める
    def decide_indexes(self, sheet, current_number):
        for index, card in enumerate(self.cardlist, 0):
            # 最初に合致したカードを出す(1枚のみ)
            if card.value == current_number:
                return index
        else:
            # 深く考えず適当に出す
            return random.randint(0, len(self.cardlist) - 1)

    # カードを出す
    def put_cards(self, indexes):
        putting_cards = []
        # とりあえず1枚しか出さない
        putting_cards.append(self.cardlist[indexes])
        self.cardlist.pop(indexes)
        return putting_cards

    # ダウトと宣言
    def call_doubt(self):
        # 1/3の確率でダウト宣言
        if random.randint(1, 3) == 3:
            print(f'{self.name}はダウトの宣言をしました！')
            return True
        else:
            return False


# メインロジック
def doubt():
    print('ダウトを始めます\n')

    # 52枚のカードをインスタンス化
    original_cards = []
    for suit in suits:
        for number in numbers:
            original_cards.append(Card(suit, number))

    # 人間プレーヤー・コンピュータプレーヤー(3人)のインスタンス化
    human = Human('HUMAN')
    cpu1 = Computer('CPU1')
    cpu2 = Computer('CPU2')
    cpu3 = Computer('CPU3')

    # カードのシャッフル
    cards = random.sample(original_cards, len(original_cards))

    # 順番を決める
    original_players = [human, cpu1, cpu2, cpu3]
    players = random.sample(original_players, len(original_players))

    # 順番を表示
    print('プレーする順番は ', end='')
    for player in players:
        if player != players[-1]:
            print(player.name, end='→')
        else:
            print(player.name, end='')
    print('です\n')

    # カードを配る
    for i, card in enumerate(cards, 0):
        if i % len(players) == 0:
            players[0].receive_card(card)
        elif i % len(players) == 1:
            players[1].receive_card(card)
        elif i % len(players) == 2:
            players[2].receive_card(card)
        elif i % len(players) == 3:
            players[3].receive_card(card)

    # 途中の処理をまとめておく
    def sub_logic(current_player, current_number):
        # 人間プレーヤーの場合のみ、手札のカードを表示
        if current_player == human:
            current_player.show_cardlist()
        sheet = current_player.decide_sheet()
        if current_player == human:
            indexes = current_player.decide_indexes(sheet)
        # コンピュータプレーヤーの場合、引数にcurrent_numberを与える
        else:
            indexes = current_player.decide_indexes(sheet, current_number)
        putting_cards = current_player.put_cards(indexes)
        # 出したカードは一旦テーブルへ
        for card in putting_cards:
            tablecards.append(card)
        # ダウト宣言はあるか？(公平性のため宣言の順番はランダム)
        # (最初に宣言したプレーヤーのダウトのみ有効)
        shuffle_players = random.sample(players, len(players))
        shuffle_players.remove(current_player)
        is_doubt = False
        is_called_doubt = False
        for player in shuffle_players:
            # ダウト宣言があった時
            if player.call_doubt():
                is_called_doubt = True
                for card in putting_cards:
                    # current_numberが13の倍数の時は2つ目の判定をする
                    if (card.value != current_number % 13) and\
                       (card.value != 13):
                        print(f'比較 {card.value}:{current_number % 13}')
                        print(f'{card.suit}{card.number}は', end='')
                        print('ダウトです！')
                        is_doubt = True
                        break
                else:
                    print('ダウトではありませんでした！')
                print('テーブル上のカードは全て', end='')
                if is_doubt:
                    print(f'{current_player.name}が引き取ることになります！\n')
                    for card in tablecards:
                        current_player.cardlist.append(card)
                else:
                    print(f'{player.name}が引き取ることになります！\n')
                    for card in tablecards:
                        player.cardlist.append(card)
                tablecards.clear()
                # 最初に宣言したプレーヤーのみイベントが起こる
                break
        # ダウト宣言が無かった時
        if not is_called_doubt:
            print('ダウトの宣言はありません\n')

    # カードが無くなったプレーヤーが出るまで繰り返す
    current_number = 1
    while True:
        # 出すべきカード番号の周知
        print(f'現在出すべき番号は{numbers[(current_number - 1) % 13]}です')

        # 順番のプレーヤーの周知
        print(f'出すプレーヤーは{players[(current_number - 1) % 4].name}です')

        # 人間プレーヤーの時
        if players[(current_number - 1) % 4] == human:
            sub_logic(human, current_number)
        # コンピュータプレーヤーの時
        elif players[(current_number - 1) % 4] == cpu1:
            sub_logic(cpu1, current_number)
        elif players[(current_number - 1) % 4] == cpu2:
            sub_logic(cpu2, current_number)
        elif players[(current_number - 1) % 4] == cpu3:
            sub_logic(cpu3, current_number)

        # テーブル上のカードの枚数を表示
        print(f'テーブル上のカードの枚数は{len(tablecards)}です')

        # 各プレーヤーの手札の枚数を表示
        is_existing_winner = False
        for player in players:
            print(f'{player.name}の手札は{len(player.cardlist)}枚です')
            # テスト
            # human.cardlist.clear()
            if len(player.cardlist) == 0:
                is_existing_winner = True
                winner = player
        print()

        # 勝敗が決した場合
        if is_existing_winner:
            print(f'{winner.name}の勝利です！')
            # 勝ったプレーヤーを取り除く
            players.remove(winner)
            players.sort(key=lambda x: len(x.cardlist))
            for i, player in enumerate(players, 2):
                print(f'{i}位は{player.name}です')
            print('ダウトを終了します')
            return

        # 番号を1増やす
        current_number += 1

    # テスト
    # for player in players:
    #     print(player.name)
    #     for card in player.cardlist:
    #         print(card.suit, card.number, end=', ')
    #     print()


# 実行
doubt()
