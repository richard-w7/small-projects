import random

def monty(num_games=1000):
    win_count_s, win_count_n = 0, 0
    doors = [1, 2, 3]

    for i in range(0,2):
        for _ in range(num_games):
            target = random.choice(doors)
            pick = random.choice(doors)

            host_opens = random.choice(list(set(doors) - {target, pick}))

            if i == 1:
                pick = (set(doors) - set([pick, host_opens])).pop()

            if pick == target:
                if i == 1:
                    win_count_s += 1
                else:
                    win_count_n += 1

    print(f'Simulated {num_games} times')
    print(f'Win percentage from always switching: {win_count_s / num_games:.3%}')
    print(f'Win percentage from never switching: {win_count_n / num_games:.3%}')

monty(10000)