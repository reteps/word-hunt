I2Cbus = None
try:
    import smbus
    I2Cbus = smbus.SMBus(1)
except ImportError:
    print('Could not import i2c library')
import json
import sys
import subprocess
import time
import solver
import math
def screenshot_until_success(new_picture=True, location="processed.png"):
    preprocess_image_command = 'convert snapshot.png -crop 350x350+800+500 -fill white -fuzz 10% +opaque "#000000" processed.png'
    ocr_command = "gocr -i " + location
    if new_picture:
        subprocess.run(["raspi2png"])
        subprocess.run(preprocess_image_command.split(" "))
    output = subprocess.run(ocr_command.split(" "), stdout=subprocess.PIPE)
    letter_map = {'0':'O','l':'I',' ':'','\r':''}
    
    res = output.stdout.decode("utf-8")
    for replacement in letter_map:
        res = res.replace(replacement, letter_map[replacement], -1)
    res = res.lower().rstrip()
    print(res)
    num_letters = len(res.replace('\n', '', -1))
    if num_letters != 16:
        print('Error parsing... Retrying!')
        print(num_letters)
        time.sleep(1)
        return screenshot_until_success(new_picture, location)
    # Return board
    return [list(row) for row in res.split('\n')]


def getBytes(s):
    return [ord(b) for b in s]

def move(x, y,adr=0x04):
    print('Move {} {}'.format(int(x),int(y)))
    packet = getBytes('3,{},{},'.format(x, y))
    I2Cbus.write_i2c_block_data(adr, packet[0], packet[1:])
    time.sleep(0.5)

def click(on, adr=0x04):
    print('Click ',on)
    packet = getBytes('2,{},0,'.format(on))
    I2Cbus.write_i2c_block_data(adr, packet[0], packet[1:])
    time.sleep(0.5)
def moveToOnBoard(newpos, currentx, currenty):
    diffx = (newpos[0] - currentx) * 44
    diffy = (newpos[1] - currenty) * 21
    print('New Word, deltaX: {}, deltaY: {}'.format(diffx, diffy))
    if (abs(diffx) > 127):
        move(math.copysign(127, diffx), 0)
        diffx -= math.copysign(127, diffx)
        print('Now diffx is', diffx)
    if diffx != 0 and diffy != 0:
        move(diffx,diffy)
def initMouse():
    move(-88, 5)
if __name__ == '__main__':
    board = []
    if len(sys.argv) == 1:
        sys.argv.append('!')
    if sys.argv[1] == 'test':
        board = screenshot_until_success(False)
    elif sys.argv[1] == 'windows':
        board = screenshot_until_success(False, "windows_processed.pnm")
    elif sys.argv[1] == 'mouse':
        if I2Cbus is None:
            print('Cannot, no mouse.')
            exit()
        while True:
            mode = int(input("Move or Click(1/2):"))
            if mode == 999:
                exit()
                x = int(input("x coord:"))
                y = int(input("y coord:"))
            elif mode ==2:
                left_c = int(input("Left click on(1/0):"))
                click(left_c)
            elif mode == 1:
                x = int(input("x change:"))
                y = int(input("y change:"))
                move(x, y)
            elif mode == 4:
                singleclick()            
            else:
                print("Exiting...")
                exit()
    else:
        board = screenshot_until_success()

    # Load dictionary
    trie_node = {}
    with open('dict_trie.json') as f:
        trie_node = json.load(f)
    for row in board:
        print(len(board))
    words = solver.allPossibleWords(board, 3, 8, trie_node)
    max_scores = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    score_map = {3: 100,4: 400, 5: 800, 6: 1400, 7: 1700, 8:2000}
    currentPosX = 0
    currentPosY = 0
    initMouse()
    for word in sorted(words,key=len)[:3]:
        max_scores[len(word)] += score_map[len(word)]
        print('{:10} -> {}'.format(word, words[word]))
        startingPos = words[word][0]
        moveToOnBoard(startingPos, currentPosX, currentPosY)
        click(1)
        for direct in words[word][1:]:
            x_change = direct[1]
            y_change = direct[0]
            currentPosX += x_change
            currentPosY += y_change
            move(x_change * 44, y_change * 21)
        click(0)
    total_max_score = 0
    for length in max_scores:
        if max_scores[length] != 0:
            print('{} -> {}'.format(length, max_scores[length]))
        total_max_score += max_scores[length]
    print('T -> {}'.format(total_max_score))
