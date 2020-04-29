
import json
SIZE = 4
directions = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1)
]

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

def get_neighbors(r, c):
    neighbors = []
    for d in directions:
        new_r = r + d[0]
        new_c = c + d[1]
        if new_r >= SIZE or new_c >= SIZE or new_r < 0 or new_c < 0:
           continue
        neighbors.append((new_r, new_c, d[0], d[1]))
    return neighbors


def allPossibleWords(board, min_length, max_length, trie_dict):
    combinations = {}

    def depth_first_search(r, c, visited, trie, current_word, direction):
        if (r, c) in visited:  # Cannot go to this cell again, so return
            return
        letter = board[r][c]
        visited.append((r, c))
        if letter in trie:  # has subnode
            current_word += letter
            if trie[letter]['valid'] and len(current_word) >= min_length and len(current_word) <= max_length:
                combinations[current_word] = direction
            for n in get_neighbors(r, c):
                new_r = n[0]
                new_c = n[1]
                depth_first_search(
                    new_r, new_c, visited[:], trie[letter], current_word, direction + [(n[3], n[2])])
    for r in range(SIZE):
        for c in range(SIZE):
            start = board[r][c]
            depth_first_search(r, c, [], trie_dict, "", [(c, r)])
    return combinations
if __name__ == '__main__':
    words = []
    trie = {}
    with open('words_alpha.txt') as f:
       words = f.read().splitlines()
    trie = generate_trie(words, trie)
    with open('dict_trie.json','w') as f:
        f.write(json.dumps(trie))
