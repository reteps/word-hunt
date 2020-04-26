import smbus

def getBytes(s):
    return [ord(b) for b in s]
I2Cbus = smbus.SMBus(1)
print('sent command.')
def move(x,y,adr=0x04):
    packet = getBytes('1,{},{},'.format(x, y))
    I2Cbus.write_i2c_block_data(adr, packet[0], packet[1:])
def click(on,adr=0x04):
    packet = getBytes('2,{},0,'.format(int(on)))
    I2Cbus.write_i2c_block_data(adr, packet[0], packet[1:])
