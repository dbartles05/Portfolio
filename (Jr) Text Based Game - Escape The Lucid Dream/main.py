# Text Based Game
# Dustyn Bartles
# 3/21/22
# Jr
# ------------------

import pygame
import winsound
import sys
import random
import time


slowText = 100
mediumText = 200
fastText = 300
superSlowText = 25

def loadMap():
    H1A1 = "\n" "You: I'm in the start of the walk-in hallway.. Why am i here? I just wanna wake up.." "\n"

    H2A2 = "\n" "You: I'm in the middle of the walk-in hallway.." "\n"

    H3A3 = "\n" "You: I'm at the end of the walk-in hallway." "\n"

    H4A4 = "\n" "You: Another hallway.. greaaattt. I'm at the start of the bedroom hallway.." "\n"

    H5A5 = "\n" "You: I'm in the middle of the bedroom hallway.. Man I'm tired of this. " "\n"

    H6A6 = "\n" "You: Does it ever end? I'm still in the middle of the bedroom hallway somehow.." "\n"

    H7A7 = "\n" "You: FINALLY. I'm at the end of the bedroom hallway.." "\n"

    H8A8 = "\n" "You: THE DINING ROOM! so many good memories here.. and bad." "\n"

    H9A9 = "\n" "You: was never aloud over here.. (At The Locked Door) " "\n"

    H10A10 = "\n" "You: Great food was cooked here at one point.. (The Kitchen)" "\n"

    H11A11 = "\n" "You: I'm at the beginning of the Laundry room.." "\n"

    H12A12 = "\n" "You: I'm at the end of the Laundry room.. Aka near the backdoor." "\n"

    R1A1 = "\n" "You: The bathroom.. nothing really special here.." "\n"

    R2A2 = "\n" "You: My old bedroom! *In the corner of the room you see the computer glowing the letter (E) E?*" "\n"

    R3A3 = "\n" "You: My sisters room.. *On  the TV the letter (V) shows* " \
           "E V ?" "\n"

    R4A4 = "\n" "You: My parents room.. Man im getting emotional, It all looks just as i remembered. "\
           "*You hear a voice say the letter I.. E V I ?* " \
           "Please just let me go home!" "\n"

    R5A5 = "\n" "You: My parents bathroom.. nice *You see a bloody letter L on the mirror* " \
           "An L? E V I L.. EVIL?" "\n"

    R6A6 = "\n" "You: My parents always kept this room locked and never let me in it.." "\n" \
           "\n" "what is all this??..  Filing cabinets??" "\n" \
           "\n" "*You begin searching them* (2 minutes later) " "\n" \
           "\n" "*You find a paper with the code (999) on it*" "\n"\


    R7A7 = "\n" "You: I'm at the backdoor.. and of course its locked. I need the keys" "\n"

    R8A8 = "\n" "You: The old living room! so many memories here.." "\n"


                                        # Hallways


    myMap = {"H1": {"LocDesc": H1A1, "e": "No", "w": "No", "n": "H2", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H2": {"LocDesc": H2A2, "e": "R8", "w": "No", "n": "H3", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H3": {"LocDesc": H3A3, "e": "No", "w": "H4", "n": "H8", "s": "H2", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H4": {"LocDesc": H4A4, "e": "H3", "w": "H5", "n": "R1", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H5": {"LocDesc": H5A5, "e": "H4", "w": "H6", "n": "No", "s": "R2", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H6": {"LocDesc": H6A6, "e": "H5", "w": "H7", "n": "No", "s": "R3", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H7": {"LocDesc": H7A7, "e": "H6", "w": "No", "n": "R4", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H8": {"LocDesc": H8A8, "e": "H10", "w": "No", "n": "H9", "s": "H3", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H9": {"LocDesc": H9A9, "e": "No", "w": "R6", "n": "No", "s": "H8", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H10": {"LocDesc": H10A10, "e": "No", "w": "H8", "n": "H11", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "No", "count": 0},

             "H11": {"LocDesc": H11A11, "e": "H12", "w": "No", "n": "No", "s": "H10", "puzzle": "No", "lock": "No",
                     "rsound": "No", "count": 0},

             "H12": {"LocDesc": H12A12, "e": "No", "w": "H11", "n": "No", "s": "R7", "puzzle": "No", "lock": "No",
                     "rsound": "No", "count": 0},

                                        # Rooms

             "R1": {"LocDesc": R1A1, "e": "No", "w": "No", "n": "No", "s": "H4", "puzzle": "No", "lock": "No",
                    "rsound": "Yes", "count": 0},

             "R2": {"LocDesc": R2A2, "e": "No", "w": "No", "n": "H5", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "Yes", "count": 0},

             "R3": {"LocDesc": R3A3, "e": "No", "w": "No", "n": "H6", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "Yes", "count": 0},

             "R4": {"LocDesc": R4A4, "e": "R5", "w": "No", "n": "No", "s": "H7", "puzzle": "No", "lock": "No",
                    "rsound": "Yes", "count": 0},

             "R5": {"LocDesc": R5A5, "e": "No", "w": "R4", "n": "No", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "Yes", "count": 0},

             "R6": {"LocDesc": R6A6, "e": "H9", "w": "No", "n": "No", "s": "No", "puzzle": "No", "lock": "EVIL",
                    "rsound": "Yes", "count": 0},

             "R7": {"LocDesc": R7A7, "e": "No", "w": "No", "n": "H12", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "Yes", "count": 0},

             "R8": {"LocDesc": R8A8, "e": "No", "w": "H2", "n": "No", "s": "No", "puzzle": "No", "lock": "No",
                    "rsound": "Yes", "count": 0}}

    return myMap

def checkDirection(direction, currLoc):
    LowerD = direction.casefold()
    newSpot = currLoc.get(LowerD)
    # print(newSpot)
    if newSpot != "No":
        return newSpot
    else:
        return None


def HandleSounds():
    DoorOpen.play()
    Walking.play()


def HandleLock1():
    passwordPrompt = "\n" + "Please enter the password for The Locked Door: " "\n"
    passwordEntered = input(passwordPrompt)
    if passwordEntered != R6password:
                 print("\n" + "Sorry, that password was incorrect" + "\n")
                 return False

    elif passwordEntered == R6password:
        print("\n" "Password Correct" + "\n")
        print("\n" "Locked Door Opening.." + "\n")
        DoorOpen.play()
        return True


def HandleLock2():
    passwordPrompt2 = "\n" + "Please enter the 3 Digit PIN Number Code to Exit: " "\n"
    passwordEntered2 = input(passwordPrompt2)
    if passwordEntered2 != R7password:
                 print("\n" + "Sorry, that PIN was incorrect" + "\n")
                 print("\n" + "You: Incorrect?? How?? Maybe I should try it backwards??" + "\n")
                 return False

    elif passwordEntered2 == R7password:
        print("\n" "PIN Correct" + "\n")
        print("\n" "Locked Door Opening.." + "\n")
        print("\n" "You Escaped!" + "\n")
        print("\n" "You: Finally! i'm out! Thank god! I got out before anything bad could happen.. *The lucid dream slowly starts to fade away..*" + "\n")
        print("\n" "*You wake up, like nothing ever happened.. what a WScrazy dream..*" + "\n")
        print("\n" "Thanks for playing!" + "\n")
        DoorOpen.play()
        time.sleep(5)
        sys.exit(2)


def slow_type(t,speed):
    TypeSound = "./sounds" + "/" + "typing.wav"
    winsound.PlaySound(TypeSound,winsound.SND_ALIAS | winsound.SND_ASYNC )
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random()*1.0/speed)
    winsound.PlaySound(None,winsound.SND_ALIAS)
    print(' ')

maplist = loadMap()
startLoc = "H1"
prePlayerLoc = startLoc
playerLoc = startLoc
keepPlaying = True

R6password = "EVIL"
R6passwordEntered = ""
R7password = "666"
R7passwordEntered = ""

pygame.mixer.init()

# Sounds
DoorOpen = pygame.mixer.Sound("sounds/DoorOpen.wav")
DoorOpen.set_volume(1.0)

Walking = pygame.mixer.Sound("sounds/Walking.wav")
Walking.set_volume(1.0)


while keepPlaying:
    currLoc = maplist.get(playerLoc)
    lockName = currLoc.get("lock")
    puzzleName = currLoc.get("puzzle")
    currLoc["count"] += 1
    slow_type(currLoc.get("LocDesc"),slowText)

    prompt = "\n" "You: Where should I go next? (N = Forward, E = Right, S = Backwards, W = Left) : " "\n"
    playerAction = input(prompt)
    prevPlayerLoc = currLoc

    if playerAction.lower() == "q":
        keepPlaying = False
    else:
        newLoc = checkDirection(playerAction.lower(), currLoc)

        if newLoc == "R1":
            print("\n" "Bathroom Door Opening.." + "\n")
            DoorOpen.play()

        if newLoc == "R2":
            print("\n" "Your Bedroom Door Opening.." + "\n")
            DoorOpen.play()

        if newLoc == "R3":
            print("\n" "Your Sisters Bedroom Door Opening.." + "\n")
            DoorOpen.play()

        if newLoc == "R4":
            print("\n" "Your Parents Bedroom Door Opening.." + "\n")
            DoorOpen.play()

        if newLoc == "R5":
            print("\n" "Your Parents Bathroom Door Opening.." + "\n")
            DoorOpen.play()

        if newLoc == "R6":
            if HandleLock1() != True:
                newLoc = None

        if newLoc == "R7":
            if HandleLock2() != True:
                newLoc = None


        if newLoc == "R8":
            print("\n" "Living Room Doors Opening.." + "\n")
            DoorOpen.play()

        if newLoc == "H1" or newLoc == "H2" or newLoc == "H3" or newLoc == "H4" or newLoc == "H5" or newLoc == "H6" or \
           newLoc == "H7" or newLoc == "H8" or newLoc == "H9" or newLoc == "H10" or newLoc == "H11" or newLoc == "H12":
           print("\n" "*Walking*" "\n")
           Walking.play()

        if newLoc != None:
            playerLoc = newLoc
        else:
            print("\n" "You: I can't go that way.." "\n")
