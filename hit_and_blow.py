import random

answer_list_int: list[int] = []
while len(answer_list_int) < 4:
    random_number: int = random.randint(0, 9)
    if random_number not in answer_list_int:
        answer_list_int.append(random_number)
answer_list: list[str] = list(map(str, answer_list_int))

print('ヒットアンドブローです')
print('4桁の数字を当てて下さい。数字は重複しません')
print('チャンスは7回までです')
print('qと入力すると途中でも終了します\n')

is_print_result: bool = True
for i in range(7):
    is_exit: bool = False
    for j in range(10):
        input_number_str: str = input(f'{i + 1}回目 4桁の数字を入力して下さい->')
        if input_number_str == 'q':
            print('q入力を受け付けました。終了します')
            is_print_result = False
            is_exit = True
            break
        if not input_number_str.isdecimal():  # onetwothreefourなど
            print('0～9の数字を入力して下さい')
            continue
        if len(input_number_str) != 4:  # 123456など
            print('4つの数字を入力して下さい')
            continue
        input_number_set: set[str] = set()
        is_overlap: bool = False
        for n in input_number_str:  # '1234'など
            if n in input_number_set:
                print('重複しないように入力して下さい')
                is_overlap = True
                break
            else:
                input_number_set.add(n)
        if is_overlap:
            continue
        # 正常な入力
        break
    else:
        print('10回以内に正しい入力が得られませんでした。終了します')
        is_print_result = False
        break
    if is_exit:
        break
    input_list: list[str] = list(input_number_str)

    hit: int = 0
    blow: int = 0
    for i in range(4):  # input:1234、answer:1357の時、1hit 1blow
        if input_list[i] == answer_list[i]:
            hit += 1
            continue
        elif input_list[i] in answer_list:
            blow += 1
        else:
            pass
    print(f'{hit}hit!{blow}blow!\n')
    if hit == 4:
        print('クリアです！おめでとうございます！')
        is_print_result = False
        break

if is_print_result:
    print(f'残念！\n当たりは{answer_list[0]}{answer_list[1]}', end='')
    print(f'{answer_list[2]}{answer_list[3]}でした！')
