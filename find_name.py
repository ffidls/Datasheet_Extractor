import parsing_pdf
import trash_in_text

# s = '08055A821FAT2A\xa0 08055A821FAT4A\xa0 08055A821JAT2A\xa0 08055A821KAT2A\xa0 08055A821KAT4A'
v = parsing_pdf.Parsing()
a = parsing_pdf.CleanPDF()


def test(lst):
    cleaning = trash_in_text.Trash()
    dck = {}
    no_type_pn = []
    max_len = [0, '']
    for el in lst:
        if cleaning.sort_trash(el):
            clean_el = a.del_trash(el)
            dck, max_len = dck_f(dck, clean_el, max_len)
            no_type_pn.append(clean_el)

    s = get_all_len_type(dck)
    s = sorted(s, reverse=True)
    return dck, no_type_pn, s


def dck_f(dck, word, mmax):  # 2 type dck - dck = {len(PN): [3words_5nums, PN...]} (?) ** -speed
    """if ' ' in word:
        word = word.replace(' ', '')"""
    count_next_dck = 1

    for el_key_len_PN in dck:
        type_PN = dck[el_key_len_PN][0]
        count_len_type = int(el_key_len_PN[:1])
        len_type = int(el_key_len_PN[el_key_len_PN.index('_') + 1:])
        len_word = len(word)

        if type_PN is None and len_word == len_type:  # add new PN and his type
            try:
                new_type, ind_type = find_new(dck[el_key_len_PN][1], word)
                dck[el_key_len_PN][0] = f"{ind_type[len(ind_type) - 1]}_{new_type}"
                return dck, mmax
            except Exception:  # ??
                # print(word)
                continue
        if (len_word == len_type) and type_PN[2:] == word[:int(type_PN[0]) + 1]:  # add PN
            dck[el_key_len_PN].append(word)
            if len(dck[el_key_len_PN]) > mmax[0]:
                mmax[0], mmax[1] = len(dck[el_key_len_PN]), el_key_len_PN
            return dck, mmax

        elif len_word == len_type:
            count_next_dck = count_len_type + 1

    dck[f"{count_next_dck}_{len(word)}"] = [None, word]
    return dck, mmax  # dck = {'len(PN)':['4_0805A','08055A821FAT2A' ...]} // p.s (ind[0] - len; ind[1-...] - PN)


def find_new(first_el, second_el):
    el, ind_lst = '', []
    a = 0
    for ind in range(len(first_el)):
        word = first_el[ind]
        if word == second_el[ind] and a < 3:  # a - ???
            el += word
            ind_lst.append(ind)
            a += 1
    return el, ind_lst


def get_all_len_type(dck):
    max_len = []
    for key in dck:
        max_len.append(len(dck[key]))

    return max_len

