import serial

class Imagewriter:
    def __init__(self, device):
        #Open serial port to printer
        self.ser = serial.Serial(device)

        #Include eighth data bit
        self.ser.write(b'\x1b\x44\x00\x32') # Esc D Ctrl-@ Space

    def linefeed(self, num = 1):
        if num > 0:
            self.ser.write(b'\x1bf')
        elif num < 0:
            self.ser.write(b'\x1br')
        for x in range(abs(num)):
            self.ser.write(b'\x0a')

    def formfeed(self):
        self.ser.write(b'\x0c')

    def carriagereturn(self):
        self.ser.write(b'\x0d')

    def printchar(self, char):
        self.ser.write(char)

    def repeatchar(self, char, num):
        self.ser.write(b'\x1bR')
        self.ser.write(str(num).zfill(3).encode('ascii'))
        self.ser.write(char)

    def printstr(self, string):
        self.ser.write(string.encode('ascii'))
