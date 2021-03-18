import pickle
import os

def count_word(token_list):
    """convert a stream of tokens into list of dictionary of term, frequency pairs

    Args:
        token_list (list): list of tokens

    Returns:
        dict: dictionary of term, frequency pairs
    """
    count = {}
    for term in token_list:
        if term not in count:
            count[term] = 1
        else:
            count[term] += 1
    return count


def merge_lists(list_1, list_2):
    """merge two lists into one
    """
    i = 0
    j = 0
    list = []
    while i < len(list_1) and j < len(list_2):
        if list_1[i] < list_2[j]:
            list.append(list_1[i])
            i += 1
        elif list_1[i] > list_2[j]:
            list.append(list_2[j])
            j+= 1
        elif list_1[i] == list_2[j]:
            list.append(list_1[i])
            i += 1
            j += 1
    list.extend(list_1[i:])
    list.extend(list_2[j:])
    return list

