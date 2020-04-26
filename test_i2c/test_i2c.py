import smbus

def convert(s):
    return [ord(b) for b in s]
adr = 0x04
x_coord = input('x coord')
y_coord = input('y coord')
I2Cbus = smbus.SMBus(1)
data = convert(x_coord+','+y_coord+',')
I2Cbus.write_i2c_block_data(adr, data[0], data[1:])
print('sent command.')
