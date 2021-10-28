from TowerOfHanoi.GameState import GameState

#################################################### BREADTH FIRST


def get_possible_moves(game_state): 
    # Per ogni pilastro verifica chi e' al top e se puo' essere spostato altrove

    possible_moves = list()
    dischi=game_state.get_disks()
    # print("Number of disks: ",dischi)
    disk_on_top = [10, 10, 10, 10]

    for disk, pillar in enumerate(game_state.array):
        if disk < disk_on_top[pillar]:
            disk_on_top[pillar] = disk

    for pillar, disk in enumerate(disk_on_top):
        if disk == 10: # e' l'indice 0
            continue

        pole_name = game_state.pole_names[pillar]
        disk_name = game_state.disk_names[disk]

#### MOVIMENTI

        if pole_name == "start":
            if disk_on_top[2] > disk:
                target_pillar = "middle"
                next_state = GameState(dischi, game_state.number)
                next_state.move(disk_name, target_pillar)
                possible_moves.append((next_state, (disk_name, pole_name, target_pillar)))

            if disk_on_top[3] > disk:
                target_pillar = "finish"
                next_state = GameState(dischi, game_state.number)
                next_state.move(disk_name, target_pillar)
                possible_moves.append((next_state, (disk_name, pole_name, target_pillar)))

        if pole_name == "middle":
            if disk_on_top[1] > disk:
                target_pillar = "start"
                next_state = GameState(dischi, game_state.number)
                next_state.move(disk_name, target_pillar)
                possible_moves.append((next_state, (disk_name, pole_name, target_pillar)))
            if disk_on_top[3] > disk:
                target_pillar = "finish"
                next_state = GameState(dischi, game_state.number)
                next_state.move(disk_name, target_pillar)
                possible_moves.append((next_state, (disk_name, pole_name, target_pillar)))

        if pole_name == "finish":
            if disk_on_top[1] > disk:
                target_pillar = "start"
                next_state = GameState(dischi, game_state.number)
                next_state.move(disk_name, target_pillar)
                possible_moves.append((next_state, (disk_name, pole_name, target_pillar)))
            if disk_on_top[2] > disk:
                target_pillar = "middle"
                next_state = GameState(dischi, game_state.number)
                next_state.move(disk_name, target_pillar)
                possible_moves.append((next_state, (disk_name, pole_name, target_pillar)))

    return possible_moves

#### PATH OTTIMALE
def find_optimal_path(state): 
    element = (state, list())

    visited = list()
    queue = list()
    queue.append(element)

    while queue:
        state, path = queue.pop(0)
        if state.is_goal(): 
            # Path con meno movimenti è anche il più corto quindi è ottimale
            optimal_path = path
            break
        else:
            for next_state, move in get_possible_moves(state):
                next_path = [el for el in path]
                next_path.append(move)
                if next_state.number in visited:
                    continue
                else:
                    visited.append(next_state.number)
                element = (next_state, next_path)
                queue.append(element)
    else:
        # Coda finita senza soluzioni
        print("No path could be found.")
        optimal_path = None

    return optimal_path

#### AZIONE OTTIMALE
def optimal_action(game_state):
    # formato   IDX_DISCO DA A
    path = find_optimal_path(game_state)
    return path[0]

#### DEBUG

if __name__ == "__main__":
    foo = GameState(4)
    foo.move("orange", "start")
    foo.move("yellow", "start")
    foo.move("green", "start")
    foo.move("blue", "start")
    # foo.move("purple", "start")

    # print(foo.array)
    # path = find_optimal_path(foo) 
    # print(path)
    print(optimal_action(foo))