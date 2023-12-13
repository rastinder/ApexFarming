import random
import time
def generate_username1():
    first_names = ['Avery', 'Bailey', 'Cameron', 'Dakota', 'Elliott', 'Frankie', 'Gray', 'Harley', 'Jordan', 'Kendall',
                   'Logan', 'Morgan', 'Parker', 'Quinn', 'Reese', 'Rowan', 'Sage', 'Spencer', 'Taylor', 'Valentine', 'Winter', 'Zephyr']
    second_names = ['Ace', 'Alpha', 'Apex', 'Berserk', 'Blaze', 'Champion', 'Cobra', 'Dragon', 'Eagle', 'Falcon', 'Glitch', 'Hawk', 'Hunter', 'Jaguar',
                    'Knight', 'Legend', 'Maverick', 'Ninja', 'Omega', 'Phoenix', 'Pirate', 'Raptor', 'Rebel', 'Samurai', 'Shadow', 'Sniper', 'Warrior', 'Wolf', 'Zombie']
    last_names = ['Black', 'Blade', 'Blaze', 'Dark', 'Death', 'Dragon', 'Fire', 'Fury', 'Ghost', 'Hunter',
                  'Knight', 'Legend', 'Ninja', 'Phoenix', 'Rebel', 'Shadow', 'Slayer', 'Storm', 'Thunder', 'Warrior']
    suffixes = ['Gaming', 'Player', 'Warrior', 'Master',
                'Legend', 'Hunter', 'Assassin', 'Champion', 'Ninja', 'Sniper']

    separator = random.choice(['_', '.', '-', ''])
    separator = ''

    # Randomly decide whether to use a middle name
    use_middle_name = random.choice([True, False])
    if use_middle_name:
        middle_name = random.choice(second_names)
        word_choices = [random.choice(
            first_names), middle_name, random.choice(last_names)]
    else:
        word_choices = [random.choice(first_names), random.choice(last_names)]

    random.shuffle(word_choices)

    # Randomly decide whether to add a number to the username
    add_number = random.choice([True, False])
    if add_number:
        random_number = random.randint(100, 999)
        word_choices.append(str(random_number))

    # Randomly decide whether to add a suffix to the username
    add_suffix = random.choice([True, False])
    if add_suffix:
        suffix = random.choice(suffixes)
        word_choices.append(suffix)

    # Randomly choose the number of characters to remove
    num_chars_to_remove = random.randint(5, 15)

    # Randomly remove characters from the username
    username = separator.join(word_choices)
    for i in range(num_chars_to_remove):
        if len(username) <= 4:
            break
        index = random.randint(0, len(username) - 1)
        username = username[:index] + username[index+1:]
        
    # Ensure the username is at least 6 characters long
    while len(username) < 6:
        username += str(random.randint(0, 9))

    # Truncate the username to 12 characters if it's longer than that
    if len(username) > 12:
        username = username[:12]

    print('username: %s' % username)
    return username
while True:
    generate_username1()
    time.sleep(.2)