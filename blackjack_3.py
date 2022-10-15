# ブラックジャック(Aは1or11)
import random


def blackjack():
    # スートと英数字を定義(ジョーカーは無し)
    suits: tuple[str, ...] = ('スペード', 'ハート', 'ダイヤ', 'クローバー')
    numbers: tuple[str, ...] = ('A', '2', '3', '4', '5', '6', '7', '8', '9',
                                '10', 'J', 'Q', 'K')

    # Aの値を決める
    def decide_Avalue(A_number: int, other_value: int) -> int:
        if other_value <= 11 - A_number:
            return 10 + A_number
        else:  # other_value >= 11
            return A_number

    class Card:
        def __init__(self, suit: str, number: str) -> None:
            self.suit: str = suit
            self.number: str = number
            if self.number == 'J' or self.number == 'Q' or self.number == 'K':
                self.value: int = 10
            elif self.number == 'A':
                pass
            else:
                self.value: int = int(self.number)

    class Player:
        def __init__(self, name: str) -> None:
            self.name: str = name
            self.cardlist: list[Card] = []
            # 入力連続失敗時の脱出用フラグ
            self.is_exit: bool = False
            # standの際の脱出用フラグ
            self.is_stand: bool = False
            # bustの際の脱出用フラグ
            self.is_bust: bool = False
            # naturalblackjackの際の脱出用フラグ
            self.is_naturalblackjack: bool = False
            # blackjackの際の脱出用フラグ
            self.is_blackjack: bool = False
            # 1回目であるかどうかのフラグ
            self.is_first: bool = True

        # カードを受け取る
        def receive_card(self, shuffle_card: Card) -> None:
            self.cardlist.append(shuffle_card)

        # scoreを計算する
        def calc_score(self) -> int:
            score: int = 0
            A_count: int = 0
            for cl in self.cardlist:
                if cl.number != 'A':
                    score += cl.value
                else:  # cl.number == 'A'
                    A_count += 1
            if A_count >= 1:
                score += decide_Avalue(A_count, score)
            return score

        # 21を超えているか
        def is_over21(self) -> bool:
            if self.calc_score() > 21:
                return True
            else:
                return False

        # 21と等しいか
        def is_equal21(self) -> bool:
            if self.calc_score() == 21:
                return True
            else:
                return False

    class Human(Player):
        def __init__(self, name: str) -> None:
            super().__init__(name)
            # 入力連続失敗時の脱出用フラグ
            self.is_exit: bool = False

        # 手札とscoreを示す
        def show_card(self) -> None:
            print(f'{self.name}\'s cards: ', end='')
            for cl in self.cardlist:
                if cl != self.cardlist[-1]:
                    print(f'{cl.suit}{cl.number}', end=', ')
                else:
                    print(f'{cl.suit}{cl.number}', end='  ')
            print(f'score:{self.calc_score()}')
            if self.is_first and self.is_equal21():
                print(f'{self.name} naturalblackjack!!')
                self.is_naturalblackjack = True
            if self.is_first:
                self.is_first = False

        # hitとstandの選択
        def select_hand(self, shuffle_cards: list[Card]) -> None:
            for i in range(10):  # 10回入力失敗すると終了
                hand: str = input('hit or stand？ hit:h stand:s ->')
                if hand == 'h':
                    self.receive_card(shuffle_cards.pop(0))
                    self.show_card()
                    if self.is_over21():
                        print(f'{self.name} bust!!')
                        self.is_bust = True
                    if self.is_equal21():  # and not self.is_naturalblackjack
                        print(f'{self.name} blackjack!\n')
                        self.is_blackjack = True
                    break
                elif hand == 's':
                    self.is_stand = True
                    break
                else:
                    print('input h or s')
            # 10回以内に正しい入力が得られない場合
            else:
                print('end(because 10times input error)')
                self.is_exit = True
                return

    class Computer(Player):
        # 手札を全て示す(scoreも)
        def show_card_full(self) -> None:
            print(f'{self.name}\'s cards: ', end='')
            for cl in self.cardlist:
                if cl != self.cardlist[-1]:
                    print(f'{cl.suit}{cl.number}', end=', ')
                else:
                    print(f'{cl.suit}{cl.number}', end='  ')
            print(f'score:{self.calc_score()}')
            if self.is_naturalblackjack:
                print(f'{self.name} naturalblackjack!!')
            # if self.is_first and self.is_naturalblackjack:
            #     print(f'{self.name} naturalblackjack!!')
            # if self.is_first:
            #     self.is_first = False

        # 1回目用(1枚目のみ示し、scoreは伏せる)
        def show_card_first(self) -> None:
            print(f'{self.name}\'s cards: ', end='')
            print(f'{self.cardlist[0].suit}{self.cardlist[0].number},', end='')
            print(' ********  score:**')  # 長いので2行で表示
            if self.is_equal21():
                self.is_naturalblackjack = True
            self.is_first = False

        # scoreが17以上になるまではhit、なったらstand
        def select_hand(self, shuffle_cards: list[Card]) -> None:
            if self.calc_score() < 17:
                print(f'{self.name} hit')
                self.cardlist.append(shuffle_cards.pop(0))
                self.show_card_full()
                if self.is_over21():
                    print(f'{self.name} bust!!')
                    self.is_bust = True
                if self.is_equal21():
                    print(f'{self.name} blackjack!')
                    self.is_blackjack = True
            else:  # self.calc_score() >= 17
                print(f'{self.name} stand')
                self.is_stand = True
                self.show_card_full()
                if self.is_over21():
                    print(f'{self.name} bust!!')
                    self.is_bust = True
                if self.is_equal21():
                    print(f'{self.name} blackjack!')
                    self.is_blackjack = True

    # ここからメインの処理
    print('blackjack start\n')

    # 52枚のトランプをインスタンス化
    cards: list[Card] = []
    for s in suits:
        for n in numbers:
            cards.append(Card(s, n))

    # テスト用カード
    # cards_test: list[Card] = []
    # cards_test.append(Card('スペード', 'A'))
    # cards_test.append(Card('ハート', '5'))
    # cards_test.append(Card('ダイヤ', 'A'))
    # cards_test.append(Card('ハート', '9'))
    # cards_test.append(Card('クローバー', 'K'))
    # cards_test.append(Card('ハート', '6'))

    # プレーヤー・コンピュータのインスタンス化
    human = Human('HUMAN')
    cpu = Computer('CPU')

    # カードのシャッフル
    shuffle_cards: list[Card] = random.sample(cards, len(cards))

    # 表示テスト
    # for sc in shuffle_cards:
    #     print(f'{sc.suit}{sc.number}', end=', ')
    # print()

    # カードの配布
    for i in range(2):
        human.receive_card(shuffle_cards.pop(0))
        cpu.receive_card(shuffle_cards.pop(0))

    # テスト用カードの配布
    # for i in range(2):
    #     human.receive_card(cards_test.pop(0))
    #     cpu.receive_card(cards_test.pop(0))

    # カードの表示
    human.show_card()

    # テスト表示
    # cpu.show_card_full()
    # 本番表示
    cpu.show_card_first()

    print()

    # プレーヤーによる手の選択
    if not human.is_naturalblackjack:  # 既に21の時は実行しない
        for i in range(12):  # A×4+2×4+3×4=24
            human.select_hand(shuffle_cards)
            # human.select_hand(cards_test)
            if human.is_exit:  # 入力連続失敗により終了
                return
            if human.is_stand or human.is_bust or human.is_blackjack:
                break
        print()

    # コンピュータによる手の選択
    if not cpu.is_naturalblackjack:
        for i in range(12):
            cpu.select_hand(shuffle_cards)
            # cpu.select_hand(cards_test)
            if cpu.is_stand or cpu.is_bust or cpu.is_blackjack:
                break
    else:
        cpu.show_card_full()
    print()

    # 勝敗判定
    if human.is_naturalblackjack and cpu.is_naturalblackjack:
        print('draw')
    elif human.is_naturalblackjack:
        print(f'{human.name} win!!')
    elif cpu.is_naturalblackjack:
        print(f'{human.name} lose...')
    elif human.is_bust:
        print(f'{human.name} lose...')
    elif cpu.is_bust:  # not human.is_bustの上で
        print(f'{human.name} win!!')
    elif human.calc_score() > cpu.calc_score():  # 共にbustでない、その上で
        print(f'{human.name} win!!')
    elif human.calc_score() < cpu.calc_score():
        print(f'{human.name} lose...')
    else:  # human.calc_score() == cpu.calc_score()
        print('draw')


# ゲーム開始
blackjack()
