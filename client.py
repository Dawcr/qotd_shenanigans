""" Small program to access the almost forgotten Quote of the Day protocol(https://www.gkbrk.com/qotd-protocol), fallen into disuse due to unneccessity and vulnerabilities.
    Interestingly enough there is a trojan named Skun that also uses port 17 for backdoor.
    Please enjoy the excessive comments"""

import socket #Needed to establish the connection
import random #Can probably remove the whole random package
import time #Used to avoid flooding the server with requests
import os #Used to clear the console
import msvcrt #Used to flush the input buffer

#Bunch of constants wannabe
SERVER_LIST = ["djxmmx.net"] #If only I found more than server that was still active, server address obtained from https://www.gkbrk.com/qotd-protocol and https://wiki.freepascal.org/QOTD, djxmmx.net provides quotes rather than quote of the day
PORT = 17 #Port 17 is dedicated to Quote of the Day Protocol(https://www.rfc-editor.org/rfc/rfc865.txt)
FORMAT = "utf-8" #Basically the whole web is encoded in UTF-8
BUFFER_SIZE = 4096 #To store the longest of quotes, as long as it's under 4096 bytes, although 512 should've been enough?
WAIT_TIME = 60 #Make sure to wait at least x seconds to avoid flooding the server with requests

quotes = [] #Store already received quotes to repopulate console after a clear() #HACK: should implement a way to remove the last line of output instead

def clear():
    """Function to clear the screen, only Windows implemented"""
    #If using Windows
    if os.name == "nt":
        os.system("cls")

def sleep(period):
    """Function for waiting, displays the remaining waiting amount in seconds

       Args:
           period::int
               The amount of time in seconds to wait"""
    if period < 0: #WHO PASSED IN A NEGATIVE NUMBER
        return
    
    for second in reversed(range(period)): 
        print('\r' + str(second) + " " * 42, end="") #Use carriage return to overwrite previous text in line #HACK: using trailing spaces to overwrite possible multiple digit numbers, but how many trailing spaces? That's the question.
        time.sleep(1)

def get_quote():
    """Function to get a quote from one of the listed servers, server chosen at random"""
    server = random.choice(SERVER_LIST) #Sadly random of 1 is always 1
    quote = socket.create_connection((server, PORT)).recv(BUFFER_SIZE).decode(FORMAT) #Connect to the address, then receive and decode the quote
    
    print("\rfrom " + server + ":\n" + quote + "\n\n") #HACK: using carriage return character '\r' to avoid the 0 from the sleep() countdown, should find an alternative
    quotes.append("from " + server + ":\n" + quote + "\n\n") #Store the quote for future printing

while True:
    get_quote() #Get a new quote
    oldtime = time.time() #Store the time the quote was received so the countdown can start
    
    while msvcrt.kbhit(): #Flush any input buffer on Windows to avoid queuing up thousands of requests, one character at a time
        msvcrt.getch() 
    if input("Press q to exit or ENTER to continue").lower() == "q": #Too lazy to implement checking for "quit" as well
        break
    
    clear() #Clear the console so only quotes remain
    for quote in quotes: #Fill the console with previously obtained quotes, one quote at a time
        print(quote)
        
    if (wait_period := int(oldtime + WAIT_TIME - time.time())) > 0: #If not enough time has passed since the last quote request, wait before proceeding
        sleep(wait_period)
