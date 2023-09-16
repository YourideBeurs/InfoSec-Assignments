def strip_non_alpha(text):
    return ''.join([c.lower() for c in text if c.isalpha()])


def break_vigenere(ciphertext, k_min, k_max):
    best_k = 0
    max_std_dev = 0
    frequencies = []
    for k in range(k_min, k_max + 1):
        std_dev = 0
        freqs = []
        for i in range(k):
            freq = [0] * 26
            for j in range(i, len(ciphertext), k):
                freq[ord(ciphertext[j])-97] += 1

            # calculate standard deviation in a more complicated way, cannot use numpy
            squares_sum = sum(x * x for x in freq)
            std_dev += (squares_sum / 26 - (sum(x for x in freq) / 26) ** 2) ** 0.5

            freqs.append(freq)
        print(f'The sum of {k} std. devs: {std_dev:.2f}')
        if std_dev > max_std_dev:
            max_std_dev = std_dev
            best_k = k
            frequencies = freqs

    key_guess = ''

    for i in range(best_k):
        max_index = frequencies[i].index(max(frequencies[i]))
        expected_code = (max_index - 4) % 26
        expected_char = chr(expected_code + 97)
        key_guess += expected_char

    print()
    print('Key guess:')
    print(key_guess)


min_k = input()
max_k = input()

encrypted_text = []
while True:
    try:
        line = input()
    except EOFError:
        break
    encrypted_text.append(line)

encrypted_text = '\n'.join(encrypted_text)
encrypted_text = strip_non_alpha(encrypted_text)

break_vigenere(encrypted_text, int(min_k), int(max_k))
