import json
import sys
import subprocess

size = 4
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

def get_neighbors(r, c):
    neighbors = []
    for d in directions:
        new_r = r + d[0]
        new_c = c + d[1]
        if new_r >= size or new_c >= size or new_r < 0 or new_c < 0:
           continue
        neighbors.append((new_r, new_c))
    return neighbors

def depth_first_search(r, c, visited, trie, current_word, direction):
    if (r, c) in visited: # Cannot go to this cell again, so return
        return
    letter = board[r][c]
    visited.append((r, c))
    if letter in trie: # has subnode
        current_word += letter
        if trie[letter]['valid'] and len(current_word) >= 3:
            print('Found {} by traveling coords {}'.format(current_word, direction, start))
        for n in get_neighbors(r, c):
            new_r = n[0]
            new_c = n[1]
            depth_first_search(new_r, new_c, visited[:], trie[letter], current_word, direction + [n])
# Problem 1: Turn board into graph
# DFS
if __name__ == '__main__':
    # First get board
    screenshot_command = "raspi2png"
    preprocess_image_command = 'convert snapshot.png -crop 350x350+800+500 -fill white -fuzz 10% +opaque "#000000" processed.png'
    ocr_command = "gocr -i processed.png"
    subprocess.run(screenshot_command)
    subprocess.run(preprocess_image_command.split(" "))
    output = subprocess.run(ocr_command.split(" "), stdout=subprocess.PIPE)
    res = output.stdout.decode("utf-8").replace('l','I').lower().rstrip()
    # output.stdout.replace('l','I').lower()
    print(res)
    num_letters = len(res.replace(' ','',-1).replace('\n','',-1))
    if num_letters != 16:
        print('Error parsing!')
        print(res)
        exit()
    board = [list(row) for row in res.replace(' ','',-1).split('\n')]
    trie_node = {}
    with open('dict_trie.json') as f:
        trie_node = json.load(f)
     
    for row in board:
        for cell in row:
            print(cell, end=" ")
        print(len(row))
    for r in range(size):
        for c in range(size):
            start = board[r][c]
            depth_first_search(r, c, [], trie_node, "", [(r,c)])
'''
from every cell
    if word has more subnotes in TRIE
        call(cell, "", [cell], [])
def call(cell, word, visited, validword)
find neighbors
add cell to visited
newword
if word is valid:
    add word to validword
if word has more subnodes in TRIE
call(neighborcell, newword, visited, validword)
'''
# Problem 2: Validate word fast
'''
TRIE data structure
basically a graph of all words as a tree
mark end of word with a flag valid=true/false
'''

