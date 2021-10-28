import numpy as np
import json
from Disk import Disk

class GameState(object):
    pole_names = ["None", "start", "middle", "finish"] # PILASTRI CON INDICI 1,2,3 PER COMODITA'
    num_disk_positions = len(pole_names)
    global dischi

#### INIT

    def __init__(self, num_disks, number=None):
        self.disks = list()
        self.disks_by_name = dict()
        self.disk_names = list()
        global dischi
        dischi=num_disks
        disk_names = ["orange", "yellow", "green", "blue", "purple"]
        disk_names = disk_names[:num_disks]
        parametri=dict({"orange":"start",
                        "yellow":"start",
                        "green":"start",
                        "blue":"start",
                        "purple":"start"})
        new_parametri=dict()
        for i in range(num_disks):
            new_parametri[disk_names[i]]=parametri[disk_names[i]]
       
        for idx in range(num_disks): #0...num-1
            disk = Disk()
            disk_name = disk_names[idx] # disk_names[0]

            self.disks.append(disk)
            self.disks_by_name[disk_names[idx]] = disk
            self.disk_names.append(disk_name)
            # print(self.disks)

#### STATO GIA ESISTENTE

        if number is not None:
            pos = self.num_disk_positions
            rest = number
            for disk_name in reversed(disk_names):
                disk = self.disks_by_name[disk_name]
                disk_idx = disk_names.index(disk_name)
                pole_idx = rest // pos ** disk_idx

                disk.pole = pole_idx
                rest = rest - pole_idx * pos ** disk_idx

    def get_disks(self):
        return int(dischi)

    @property
    def array(self):
        return np.array([disk.pole for disk in self.disks])

    def __str__(self):
        lines = ["{disk} is on pole {pole}".format(disk=self.disk_names[idx], 
                                                   pole=self.pole_names[pole])
                    for idx, pole in enumerate(self.array)]
        
        return "\n".join(lines)

    def __repr__(self):
        return "Tower of Hanoi GameState ID {id}".format(id=self.number)

#### ID DELLO STATO

    @property
    def number(self):
        pos = self.num_disk_positions

        number = 0
        for disk_idx, disk in enumerate(self.disks):
            pole_idx = disk.pole
            increment = pole_idx * pos ** disk_idx
            number += increment

        return number

#### SPOSTA DISCO

    def move(self, disk_name, pole_name):
        disk = self.disks_by_name[disk_name]
        pole = self.pole_names.index(pole_name)

        disk.pole = pole
        with open("data.json") as f:
            data=json.load(f)
        data[disk_name]=self.pole_names[pole]
        with open("data.json",'w') as f:
            json.dump(data,f)
        # print(data)
        
#### IN CASO DI ERRORI NEI MODULI

    def has_missing_disk(self):
        for disk_name, disk in self.disks_by_name.items():
            if disk.pole == 0:
                return (True, disk_name)
        else:
            return (False, None)

#### GOAL E START

    def is_goal(self):
        for disk in self.disks:
            if self.pole_names[disk.pole] != "finish":
                return False
        
        return True

    def is_start(self):
        for disk in self.disks:
            if self.pole_names[disk.pole] != "start":
                return False

        return True

#### DEBUG

if __name__ == "__main__":
    foo = GameState(3)
    foo.move("orange", "start")
    foo.move("yellow", "finish")
    foo.move("green", "start")

    goal_state = GameState(3)
    goal_state.move("orange","finish")
    goal_state.move("yellow","finish")
    goal_state.move("green","finish")

    starting_state = GameState(5)
    starting_state.move("orange","start")
    starting_state.move("yellow","start")
    starting_state.move("green","start")
    starting_state.move("blue","start")
    starting_state.move("purple","start")

    bar = GameState(4)
    bar.move("orange","finish")
    bar.move("yellow","finish")
    bar.move("green","finish")
    bar.move("blue","finish")

    print(starting_state, starting_state.number)