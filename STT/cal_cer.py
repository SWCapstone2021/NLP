import Levenshtein as Lev


def char_distance(ref, hyp):
    ref = ref.replace(' ', '')
    hyp = hyp.replace(' ', '')

    dist = Lev.distance(hyp, ref)
    length = len(ref.replace(' ', ''))

    return dist, length


def calculate_CER(y, y_hat):
    total_dist = 0
    total_length = 0
    for ref, hyp in zip(y, y_hat):
        dist, length = char_distance(ref, hyp)
        total_dist += dist
        total_length += length

    cer = float(total_dist / total_length) * 100
    return cer


if __name__ == '__main__':
    y = ['밖에 요즘 나갔다 오면은 옷이라든지 뭐 얼굴 세수만 해 때가 확 끼잖아ㄴㄹㄴㄴㄹㄴㄹ, 너는']
    y_hat = ['그']

    cer = calculate_CER(y, y_hat)

    print(cer)
