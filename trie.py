def gen_trie(word, t_node):
    if word == "":
        return
    first_letter = word[0]
    if first_letter not in t_node:
        # valid at end of search, so there is no subnodes
        t_node[first_letter] = {'valid': len(word) == 1}
    # Generate trie without first letter
    gen_trie(word[1:], t_node[first_letter])


'''
Converts dictionary into trie structure for easy lookup
'''


def generate_trie(dictionary, trie):
    for word in dictionary:
        word = word.lower()
        gen_trie(word, trie)
    return trie
