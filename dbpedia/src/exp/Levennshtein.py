import Levenshtein
def string_similarity(s1, s2):
    s1 = s1.decode('utf8')
    s2 = s2.decode('utf8')
    edit_distance = Levenshtein.distance(s1, s2)
    len_s1 = len(s1)
    len_s2 = len(s2)

    if len_s1 > len_s2:
        max = len_s1
    else:
        max = len_s2

    string_similarity = 1.0 - float(edit_distance) / max
    print string_similarity


if __name__ == "__main__":
    string_similarity("United States","USS United States")