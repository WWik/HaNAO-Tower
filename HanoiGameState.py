from naoqi import ALProxy, ALModule
import json
from TowerOfHanoi.GameState import GameState

class USRHanoiGameState(ALModule):
    
    global num_disks

    try:
        num_disks=input("Insert number of disks: (default 5)  ")
    except:num_disks=5

    def __init__(self, name, config=None):
        
        ALModule.__init__(self, name)
        self.name = name
        self.tts = ALProxy("ALTextToSpeech")
        self.memory = ALProxy("ALMemory")
        self.posture = ALProxy("ALRobotPosture")
        
        
        disk_names = ["orange", "yellow", "green", "blue", "purple"]
        parametri=dict({"orange":"start",
                        "yellow":"start",
                        "green":"start",
                        "blue":"start",
                        "purple":"start"})
                        
        new_parametri=dict()
        for i in range(num_disks):
            new_parametri[disk_names[i]]=parametri[disk_names[i]]
        print("PARAMETRI: ",new_parametri)

        try:
            with open("data.json","w") as f:
                json.dump(new_parametri,f)
        except:
            pass


    def __enter__(self):
        return self

    def get_disks(self):
        return int(num_disks)

    def __exit__(self, exec_type, ethresholdsvalue, traceback):
        print("Exit")

    def get_gamestate(self):
        if not self.posture._isRobotInPosture("USRLookAtTower", 0.02, 0.02)[0]:
            self.posture.goToPosture("USRLookAtTower", 1.0)

        state = self.detect_disks()

        print("The current gamestate is:" + str(state.array))
        return state

    def detect_disks(self):
        data=None
        with open("data.json") as f:
            data=json.load(f)
        game_state = GameState(int(num_disks))
        for disk in data:
            pole=data[disk]
            print("Disk {} is in pole \"{}\"".format(disk,pole))
            game_state.move(disk,pole)
        return game_state


