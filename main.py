import serial
import json
import sys
import subprocess
import time
import solver
import math
def screenshot_until_success(new_picture=True, location="processed.png"):
    cmd = 'convert snapshot.png -crop 340x360+800+500 -fill white -fuzz 10% +opaque "#000000" -fill white -draw "rectangle 0,80 400,100" -draw "rectangle 0,180 400,200" -draw "rectangle 0,260 400,280" processed.png'
    preprocess_image_command = 'convert snapshot.png -crop 340x360+800+500 -fill white -fuzz 10% +opaque "#000000" -fill white'
    p2 = ['-draw', '\"rectangle 0,80 400,100\"', '-draw "rectangle 0,180 400,200"', '-draw "rectangle 0,260 400,280"', 'processed.png']
    ocr_command = "gocr -i " + location
    if new_picture:
        subprocess.run(["raspi2png"])
        output,error  = subprocess.Popen(
                    cmd, universal_newlines=True, shell=True,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    output = subprocess.run(ocr_command.split(" "), stdout=subprocess.PIPE)
    letter_map = {'0':'O','l':'I',' ':'','\r':'', '%':'','_':'','$':'S',',':'','-':'','"':'',"'":''}
    res = output.stdout.decode("utf-8")
    print(res)
    for replacement in letter_map:
        res = res.replace(replacement, letter_map[replacement], -1)
    res = res.lower().lstrip().rstrip()
    print(res)
    num_letters = len(res.replace('\n', '', -1))
    if num_letters != 16:
        print('Error parsing... Retrying!')
        print(num_letters)
        return screenshot_until_success(new_picture, location)
    # Return board
    return [list(row) for row in res.split('\n')]

MOUSE_LOOKUP_TABLE = {
    (1, 0): [44, 0], # x, y
    (0, 1): [0, 21],
    (-1, 0): [-44, 0],
    (0, -1): [0, -21]
}
ser = serial.Serial(            
port='/dev/ttyS0',
baudrate = 38400)

def move(x, y, speed):
    print('Move {} {}'.format(int(x),int(y)))
    packet = str.encode('M{:04}{:04}#'.format(x, y))
    time.sleep(speed)
    ser.write(packet)

def click(on, adr=0x04):
    print('Click ',on==1)
    packet = str.encode('C{}0000000#'.format(on))
    time.sleep(0.03)
    ser.write(packet)
def correctMouseCoords(deltaPos, counter):
    if deltaPos in MOUSE_LOOKUP_TABLE:
        m = MOUSE_LOOKUP_TABLE[deltaPos]
        return (m[0], m[1]), counter
    x = deltaPos[0] * 54
    if x != 0:
        counter+=1
    if counter > 50:
        x += 1
        counter -= 50
    y = deltaPos[1] * 26
    return (x, y), counter
def moveToOnBoard(newpos, currentx, currenty, speed,counter):
    deltaPos = (newpos[0] - currentx, newpos[1] - currenty)
    diff,counter = correctMouseCoords(deltaPos,counter)
    diffx = diff[0]
    diffy = diff[1]
    # print('New Word, deltaX: {}, deltaY: {}'.format(diffx, diffy))
    if (abs(diffx) > 110):
        move(math.copysign(110, diffx), 0, speed)
        move(math.copysign(45, diffx), 0, speed)
        if abs(diffy) == 26:
            move(0, math.copysign(21, diffy), speed)
        else:
            move(0, diffy, speed)
        return counter
    if diffx != 0 or diffy != 0:
        move(diffx, diffy, speed)
    return counter
def initMouse(speed):
    move(-82, 23, speed)
if __name__ == '__main__':
    board = []
    speed = 0.02
    trie_node = {}

    with open('dict_trie.json') as f:
        trie_node = json.load(f)
    if len(sys.argv) == 1:
        sys.argv.append('!')
    input('ready.')
    if sys.argv[1] == 'test':
        move(0, -20, speed)
        board = screenshot_until_success(False)
    elif sys.argv[1] == 'windows':
        board = screenshot_until_success(False, "windows_processed.pnm")
    elif sys.argv[1] == 'mouse':
        while True:
            mode = int(input("Move or Click(1/2):"))
            if mode ==2:
                left_c = int(input("Left click on(1/0):"))
                click(left_c)
            elif mode == 1:
                x = int(input("x change:"))
                y = int(input("y change:"))
                move(x, y, 0.05)
            else:
                print("Exiting...")
                exit()
    elif sys.argv[1] == 'spam':
        s = input('speed > ')
        move(0,-50, s)
        while True:
            move(50, 0, s);
            move(0, 50, s)
            click(1)
    else:
        move(0, -20, speed)
        time.sleep(3)
        board = screenshot_until_success()

    # Load dictionary
    for row in board:
        print(len(board))
    words = solver.allPossibleWords(board, 3, 11, trie_node)
    max_scores = {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0,9:0,10:0}
    score_map = {3: 100,4: 400, 5: 800, 6: 1400, 7: 1700, 8:2000,9:1,10:1}
    currentPosX = 0
    currentPosY = 0
    initMouse(speed)
    c = 0
    for word in sorted(words,key=len,reverse=True):
        max_scores[len(word)] += score_map[len(word)]

        print('{:10} -> {}'.format(word, words[word]))
        startingPos = words[word][0]
        c = moveToOnBoard(startingPos, currentPosX, currentPosY, speed, c)
        currentPosX = startingPos[0]
        currentPosY = startingPos[1]
        click(1)
        for direct in words[word][1:]:
            coord,c=correctMouseCoords(direct,c)
            move(coord[0],coord[1],speed)
            currentPosX += direct[0]
            currentPosY += direct[1]
            if currentPosX < 0 or currentPosY < 0 or currentPosX > 3 or currentPosY > 3:
                print('ERROR',word, currentPosX, currentPosY)
                exit()
        click(0)
    total_max_score = 0
    for length in max_scores:
        if max_scores[length] != 0:
            print('{} -> {}'.format(length, max_scores[length]))
        total_max_score += max_scores[length]
    print('T -> {}'.format(total_max_score))
