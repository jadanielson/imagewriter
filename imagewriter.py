import serial

class Imagewriter:
    def __init__(self, device):
        #Open serial port to printer
        self.ser = serial.Serial(device)

        #Include eighth data bit
        self.ser.write(b'\x1b\x5a\x00\x32') # Esc Z Ctrl-@ Space

        #Auto linefeed when line full
        self.ser.write(b'\x1b\x44\x20\x00') # Esc D Space Ctrl-@

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
        self.ser.write(string.encode('ascii', 'replace'))


    # Clear line buffer
    def cancelline(self):
        self.ser.write(b'\x18') # Ctrl-X

    # Set which font to print in
    # 0 = Correspondence, 1 = Draft, 2 = Near Letter Quality
    def setfont(self, font):
        self.ser.write(b'\x1b\x61') # Esc a
        self.ser.write(str(font).encode('ascii'))

    # Enable or disable Double-width printing
    def doublewidth(self, dw: bool):
        if dw:
            self.ser.write(b'\x0e') # Ctrl-N
        else:
            self.ser.write(b'\x0f') # Ctrl-O

    # Enable or disable underline
    def underline(self, ul: bool):
        if ul:
            self.ser.write(b'\x1b\x58') # Esc X
        else:
            self.ser.write(b'\x1b\x89') # Esc Y
    
    # Enable or disable boldface
    def boldface(self, bf: bool):
        if bf:
            self.ser.write(b'\x1b\x21') # Esc !
        else:
            self.ser.write(b'\x1b\x22') # Esc "

    # Enable or disable Half-height text
    def halfheight(self, hh: bool):
        if hh:
            self.ser.write(b'\x1b\x77') # Esc w
        else:
            self.ser.write(b'\x1b\x57') # Esc W

    # Enable or disable superscript (also disables subscript)
    def superscript(self, ss: bool):
        if ss:
            self.ser.write(b'\x1b\x78') # Esc x
        else:
            self.ser.write(b'\x1b\x7a') # Esc z

    # Enable or disable subscript (also disables superscript)
    def subscript(self, ss: bool):
        if ss:
            self.ser.write(b'\x1b\x79') # Esc y
        else:
            self.ser.write(b'\x1b\x7a') # Esc z

    def slashedzero(self, sz: bool):
        if sz:
            self.ser.write(b'\x1b\x44\x00\x01') # Esc D Ctrl-@ Ctrl-A
        else:
            self.ser.write(b'\x1b\x5a\x00\x01') # Esc Z Ctrl-@ Ctrl-A