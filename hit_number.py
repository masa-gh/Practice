import random

answer = random.randint(0, 9)
print('数当てゲームです')
print('0～9のどれか1つが当たりです')
print('チャンスは3回です\n')

for i in range(3):
    input_number_str = input(f'{i + 1}回目 0～9を入力して下さい->')
    input_number = int(input_number_str)
    if input_number == answer:
        print('当たりです！')
        break
    else:
        print('違います！')

print(f'\n当たりは{answer}でした')
