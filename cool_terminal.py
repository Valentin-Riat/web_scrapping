"""
Please put the following line in the powershell if the ANSI codes do not displays correctly :

            reg add HKEY_CURRENT_USER\Console /v VirtualTerminalLevel /t REG_DWORD /d 1

"""

import time
import sys
# print(ord("━"))
# print(chr(9473))

# # for num in range(255) :
# #     print(chr(num),chr(num),chr(num), sep="")


# for i in range(10):


#     sys.stdout.flush()
#     # time.sleep(0.3)
#     #print("\u001b[2K",sep="")





def esc_code(command, num=0) :
    """
    ANSI escape codes to move the cursor, clear lines, and hide cursor
    if there is no '\n' in your print, don't forget to do sys.stdout.flush to display
    """
    if command == "up" :
        return f"\u001b[{num}A"
    if command == "down" :
        return f"\u001b[{num}B"
    if command == "right" :
        return f"\u001b[{num}C"
    if command == "left" :
        return f"\u001b[{num}D"
    if command == "next line" :
        return f"\u001b[{num}E"
    if command == "prev line" :
        return f"\u001b[{num}F"
    if command == "set col" :
        return f"\u001b[{num}G"
    if command == "set pos" :
        return f"\u001b[{num[0]};{num[1]}H"
    if command == "clear line" :
        return f"\u001b[2K"
    if command == "hide cursor" :
        return f"\033[?25l"
    if command == "disp cursor" :
        return f"\033[?25h"


def progess_bar(current, total, unit="", bar_size = 50) :
    """
    prints a loading bar on the current line
    leaves the cursor at the end of the progress bar, on the same line
    """
    UNICODE_char = chr(9473)
    COLOR = {
    "HEADER": "\033[95m",
    "BLUE"  : "\033[94m",
    "GREEN" : "\033[32m",
    "RED"   : "\033[91m",
    "YELLOW": "\033[33m",
    "GRAY"  : "\033[90m",
    "ENDC"  : "\033[0m",
    }
    progress = current*bar_size//total
    sys.stdout.write(esc_code("left",1000))
    sys.stdout.write(COLOR["GREEN"])
    
    for i in range(progress) :
        sys.stdout.write(UNICODE_char)


    sys.stdout.write(COLOR["RED"])
    for i in range(progress,bar_size):
        sys.stdout.write(UNICODE_char)

    sys.stdout.write(COLOR["BLUE"])
    sys.stdout.write(f"  {current}/{total} {unit}")
    sys.stdout.write(COLOR["GRAY"])
    sys.stdout.write(f"  ({int(current/total*100)} %)")
    sys.stdout.write(COLOR["ENDC"])
    sys.stdout.flush()
    return


COLOR = {
"HEADER": "\033[95m",
"BLUE"  : "\033[94m",
"GREEN" : "\033[32m",
"RED"   : "\033[91m",
"YELLOW": "\033[33m",
"GRAY"  : "\033[90m",
"ENDC"  : "\033[0m",
}

if __name__ == "__main__" :
    # print("\u001b[92m", "Testing Green!!", COLOR["ENDC"])
    # print("\n")
    for i in range(11):
        progess_bar(i,10,"Teams",100)
        time.sleep(0.2)
    


