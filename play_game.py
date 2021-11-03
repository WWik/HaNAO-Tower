from naoqi import ALBroker    
from naoqi import ALProxy

from HanoiGameState import USRHanoiGameState

import time, sys
import numpy as np
import yaml

from planner import find_optimal_path
from pyddl_hanoi import hanoiv3 


############### DEBUG ?

try : DEBUG = sys.argv[2]
except: DEBUG = False

############### INIT NAO
try : robot_ip = sys.argv[1]
except: robot_ip = "127.0.0.1"

myBroker = ALBroker("myBroker", "0.0.0.0", 0, robot_ip, 9559)

tts = ALProxy("ALAnimatedSpeech")
tts.setBodyLanguageModeFromStr("enabled")

posture = ALProxy("ALRobotPosture")

posture._loadPostureLibraryFromName("USRTowerOfHanoi.postures")
posture._generateCartesianMap()

posture.goToPosture("Sit", 1.0)

np.random.seed(42)
number_of_moves = 0

########## INIT LISTS

pole_animations = {
    "start": "tower_of_hanoi/PointStart",
    "middle": "tower_of_hanoi/PointMiddle",
    "finish": "tower_of_hanoi/PointGoal"
} 

pole_names = {
    "start": "the pole on my left",
    "middle": "the middle pole",
    "finish": "the pole on my right"    
}

########### INIT STRINGS CHE DEVE DIRE NAO

with open("strings.yaml", "r") as stream:
    strings = yaml.load(stream)

########### METODO TALK

def select_line(key):
    samples = list()
    for x in strings["conversation"][key]:
        samples.append(x[0])
    return np.random.choice(samples)

def analyze(step):
    return step[0], step[1], step[2]

###### MAIN

with USRHanoiGameState("USRHanoiGameState2", None) as HanoiGameState: 
    try:
        posture.goToPosture("Sit", 1.0)
        finish=0
        dischi=HanoiGameState.get_disks()
        tts.say("\\pau=400\\ ^start(tower_of_hanoi/Wave) Hi! \\pau=600\\ ^wait(tower_of_hanoi/Wave)")

        if DEBUG == False:
            
            time.sleep(1)
            tts.say(select_line("start").format(anim="tower_of_hanoi/Wave",num=dischi))
            tts.say(select_line("explanation"))
        
        
    #### BREADTH FIRST ALGORITHM ####
        game_state = HanoiGameState.get_gamestate()
        tts.say(select_line("order_disks").format(anim="tower_of_hanoi/PointStart"))
        time.sleep(3)
        while not game_state.is_start():
            game_state = HanoiGameState.get_gamestate()
        
        tts.say(select_line("begin"))
        time.sleep(3)
        import time
        bfa_duration=time.time()
        moves_to_goal=find_optimal_path(game_state)
        bfa_duration=time.time()-bfa_duration
        if DEBUG : print("Breadth First duration:",bfa_duration)

        tts.say(select_line("think").format(anim="tower_of_hanoi/Thinking"))
        
        time.sleep(5)
        
        if not moves_to_goal == None and DEBUG: print("BFA - SOLVED")
        
        for step in moves_to_goal:
            disk, from_pole, to_pole = analyze(step)
            game_state.move(disk,to_pole)
            if DEBUG : print("Move {} disk from {} to {} pole").format(disk,from_pole,to_pole)
            tts.say(select_line("ask_move").format(
                disk=disk,
                from_pole=pole_names[from_pole],
                to_pole=pole_names[to_pole],
                anim1=pole_animations[from_pole],
                anim2=pole_animations[to_pole]
            ))
            if DEBUG == True:
                game_state.array
            
            time.sleep(5)
            tts.say(select_line("thank_you").format(anim="tower_of_hanoi/Nodd"))
            number_of_moves += 1
            time.sleep(1)

        if game_state.is_goal():
            tts.say(select_line("congratulations").format(num_moves=number_of_moves))
            finish=1
            time.sleep(2)
        else:
            print("Oh no!")

    #### STRIPS ####
        tts.say("Now let's solve this game with STRIPS Algorithm")
        time.sleep(1.5)
        tts.say(select_line("think").format(anim="tower_of_hanoi/Thinking"))
        time.sleep(3)
        strips_duration=time.time()
        mosse=hanoiv3.runquiet(str(dischi),verbose=DEBUG)
        strips_duration=time.time()-strips_duration
        if DEBUG : print("STRIPS - SOLVED")
        tts.say("STRIPS solved this game with {num_moves} moves.".format(num_moves=len(mosse)))
        time.sleep(6)
        if DEBUG : print(strips_duration)
        finish=2

    #### END ####
        if finish==2:
            tts.say(select_line("compare").format(bfa=bfa_duration,sa=strips_duration))
            time.sleep(2)
            tts.say(select_line("compare_2").format(moves1=number_of_moves,moves2=len(mosse)))
            time.sleep(2)
            if DEBUG : 
                print(select_line("compare").format(bfa=bfa_duration,sa=strips_duration))
                print(select_line("compare_2").format(moves1=number_of_moves,moves2=len(mosse)))
            tts.say(select_line("about").format(anim="tower_of_hanoi/Wave"))
            time.sleep(1)
            tts.say("\\pau=400\\ ^start(tower_of_hanoi/Wave) Bye! Hope you come again to play! ^wait(tower_of_hanoi/Wave)")
            posture.goToPosture("Stand", 1.0)

    except KeyboardInterrupt:
        myBroker.shutdown()
        sys.exit(0)