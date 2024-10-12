import imagewriter
from datetime import date
import calendar

iw = imagewriter.Imagewriter('/dev/ttyS0')
iw.slashedzero(True)

##### Header

dayofweek = calendar.day_name[date.today().weekday()]
title = "Justin's News"
datestring = date.today().strftime("%d %B %Y")
leftspaces = 28-(3+dayofweek.__len__())
rightspaces = 80-52-(1+datestring.__len__())

iw.boldface(True)
iw.repeatchar(b'\xd6',80)
iw.carriagereturn()
iw.linefeed()

iw.printchar(b'\xd6')
iw.printstr(dayofweek)
iw.repeatchar(b'\x20',leftspaces)
iw.doublewidth(True)
iw.printstr(title)
iw.doublewidth(False)
iw.repeatchar(b'\x20',rightspaces)
iw.printstr(datestring)
iw.printchar(b'\xd6')
iw.carriagereturn()
iw.linefeed()

iw.repeatchar(b'\xd6',80)
iw.carriagereturn()
iw.linefeed()
iw.boldface(False)

iw.linefeed(2)

##### Weather Section

iw.boldface(True)
iw.printchar(b'\xd6')
iw.printstr('Weather')
iw.carriagereturn()
iw.linefeed()

iw.repeatchar(b'\xd6',8)
iw.carriagereturn()
iw.linefeed()
iw.boldface(True)