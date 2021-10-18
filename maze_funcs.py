from threading import *
from time import sleep
# For copying 2D List
import copy


# Function that makes the 2d list for the maze and adds the original values
def make_maze(width, height):
    maze_row_list = []
    maze_wall_rect = "wall"
    maze_blank_rect = "blank"
    # For loop for rows
    for i in range(height):
        # For loop for tiles in rows (columns)
        maze_tile_list = []
        for j in range(width):
            # Adds wall tile dicts to tile list
            if (i == 0 or i == height - 1) or (j == 0 or j == width - 1):
                maze_tile_dict = {"x_coord": j * 50, "y_coord": i * 50, "tile_type": maze_wall_rect}
                maze_tile_list.append(maze_tile_dict)

            # Adds blank tile dicts to tile list
            else:
                maze_tile_dict = {"x_coord": j * 50, "y_coord": i * 50, "tile_type": maze_blank_rect}
                maze_tile_list.append(maze_tile_dict)
        maze_row_list.append(maze_tile_list)
    # Returns a list of the rows (2d list)
    return maze_row_list


# Changes the value of a specific tile of the maze
def edit_maze(maze_list, x_coord, y_coord, edit_mode):
    tile = maze_list[y_coord][x_coord]
    if edit_mode == "switch":

        # Checks if the tile is on the border of the maze
        if not (x_coord == 0 or maze_list[y_coord][-1] == maze_list[y_coord][x_coord]
                or y_coord == 0 or maze_list[-1][x_coord] == maze_list[y_coord][x_coord]):
            # Changes tile to wall or blank
            if tile["tile_type"] == "wall":
                tile["tile_type"] = "blank"
            elif tile["tile_type"] == "blank":
                tile["tile_type"] = "wall"

    elif edit_mode == "start" or edit_mode == "end":
        # Checks if the tile is a border and also that it isn't a corner
        if ((x_coord == 0 or maze_list[y_coord][-1] == maze_list[y_coord][x_coord]
             or y_coord == 0 or maze_list[-1][x_coord] == maze_list[y_coord][x_coord])
            and not ((x_coord == 0 and y_coord == 0) or maze_list[-1][0] == maze_list[y_coord][x_coord]
                or maze_list[0][-1] == maze_list[y_coord][x_coord] or maze_list[-1][-1] == maze_list[y_coord][x_coord])):

            # Checks to make sure there are no other starts or ends, if there is it removes them
            for row in maze_list:
                for row_tile in row:
                    if row_tile["tile_type"] == edit_mode:
                        row_tile["tile_type"] = "wall"
                tile["tile_type"] = edit_mode
    else:
        raise ValueError('edit mode must equal "switch", "start", or "end".')


# Makes it so the maze is only walls, starts, ends, and blanks
def clear_maze(maze_list):
    for row in maze_list:
        for tile in row:
            if tile["tile_type"] == "path" or tile["tile_type"] == "solving":
                tile["tile_type"] = "blank"


# Solves the maze and visualizes it
def solve_maze(maze_list, window):
    start_tile = {}
    end_tile = {}

    # Checks to make sure the maze has a start and end
    for row in maze_list:
        for tile in row:
            if tile["tile_type"] == "start":
                start_tile = tile
            elif tile["tile_type"] == "end":
                end_tile = tile
    if start_tile == {} or end_tile == {}:
        return

    # Gets the tile the maze starts in
    if start_tile["x_coord"] == 0:
        current_tile = maze_list[int(start_tile["y_coord"] / 50)][1]
    elif start_tile["y_coord"] == 0:
        current_tile = maze_list[1][int(start_tile["x_coord"] / 50)]
    elif start_tile["x_coord"] == (len(maze_list[0]) - 1) * 50:
        current_tile = maze_list[int(start_tile["y_coord"] / 50)][int(start_tile["x_coord"] / 50 - 1)]
    else:
        current_tile = maze_list[int(start_tile["y_coord"] / 50 - 1)][int(start_tile["x_coord"] / 50)]

    # Checks to make sure the tile the maze should start on isn't a wall
    if current_tile["tile_type"] == "wall":
        return
    else:
        current_tile["tile_type"] = "path"

        # This func takes the coords of a tile as input and the direction that it is checking in
        # from that, it keeps checking a direction until it runs into a wall or an intersection
        # if it runs into an intersection, it checks all of the directions from that tile
        def check_direction(tile_x, tile_y, tile_direction, return_2d_list=None):
            if return_2d_list is None:
                return_2d_list = []
            # A list of all the tiles in the direction it is checking
            direction_tile_list = [maze_list[tile_y][tile_x]]
            # A 2d list that has all of the tiles in it that the current path has taken
            path_2d_list_copy = copy.deepcopy(return_2d_list)
            
            # While used to check each tile in a direction, after it checks a tile it checks the next one based on i
            i = 1
            while True:
                # Change to set how fast the maze is solved
                sleep(.1)

                if tile_direction == "left":
                    direction_current_tile = maze_list[tile_y][tile_x - i]
                elif tile_direction == "up":
                    direction_current_tile = maze_list[tile_y - i][tile_x]
                elif tile_direction == "right":
                    direction_current_tile = maze_list[tile_y][tile_x + i]
                else:
                    direction_current_tile = maze_list[tile_y + i][tile_x]
                
                # Checks if the direction ran into a wall and exits it if it has
                if (direction_current_tile["tile_type"] == "wall"
                        or direction_current_tile["tile_type"] == "start"
                        or direction_current_tile["tile_type"] == "path"):
                    break

                direction_current_tile_x = int(direction_current_tile["x_coord"] / 50)
                direction_current_tile_y = int(direction_current_tile["y_coord"] / 50)

                # Checks if its at the end of the maze
                if (maze_list[direction_current_tile_y - 1][direction_current_tile_x]["tile_type"] == "end"
                        or maze_list[direction_current_tile_y + 1][direction_current_tile_x]["tile_type"] == "end"
                        or maze_list[direction_current_tile_y][direction_current_tile_x - 1]["tile_type"] == "end"
                        or maze_list[direction_current_tile_y][direction_current_tile_x + 1]["tile_type"] == "end"):

                    # Makes the current tile into a path
                    direction_current_tile["tile_type"] = "path"
                    direction_tile_list.append(direction_current_tile)
                    path_2d_list_copy.append(direction_tile_list)

                    # Sets the 2d list for the solved maze and then edits the tiles in it to show the solved path
                    window.solved_maze_list = copy.deepcopy(maze_list)
                    for direction_list in path_2d_list_copy:
                        for solved_tile in direction_list:
                            for tile_row in window.solved_maze_list:
                                for unsolved_tile in tile_row:
                                    if (unsolved_tile["x_coord"] == solved_tile["x_coord"]
                                            and unsolved_tile["y_coord"] == solved_tile["y_coord"]):
                                        unsolved_tile["tile_type"] = "solving"

                    # Sets the solved value, used to determine the shortest route and display it correctly
                    window.solved += 1
                    window.update()
                    return

                # Checks if its at an intersection
                elif (((tile_direction == "left" or tile_direction == "right") and (
                        maze_list[direction_current_tile_y - 1][direction_current_tile_x]["tile_type"] == "blank"
                        or maze_list[direction_current_tile_y + 1][direction_current_tile_x]["tile_type"] == "blank"))
                      or ((tile_direction == "up" or tile_direction == "down") and (
                        maze_list[direction_current_tile_y][direction_current_tile_x - 1]["tile_type"] == "blank"
                        or maze_list[direction_current_tile_y][direction_current_tile_x + 1]["tile_type"] == "blank"))):

                    # Adds the tile to the direction's current path and changes the tile to checked
                    direction_tile_list.append(direction_current_tile)
                    path_2d_list_copy.append(direction_tile_list)
                    direction_current_tile["tile_type"] = "path"
                    window.update()
                    break

                # Keeps checking in the direction if it hasn't run into a wall or an intersection
                else:
                    direction_tile_list.append(direction_current_tile)
                    path_2d_list_copy.append(direction_tile_list)
                    direction_current_tile["tile_type"] = "path"
                    window.update()
                    i += 1

            # Uses recursive functions to check the new intersections, passes in the current direction list which
            # gets added onto for each new direction. This 2d list is used to find the path to a certain tile.
            # Makes them all threads so that directions can be checked simultaneously
            if len(direction_tile_list) > 1:
                new_direction_current_tile = direction_tile_list[-1]
                new_direction_current_tile_x = int(new_direction_current_tile["x_coord"] / 50)
                new_direction_current_tile_y = int(new_direction_current_tile["y_coord"] / 50)

                recursive_t1 = Thread(target=check_direction, args=(new_direction_current_tile_x, new_direction_current_tile_y, "left", path_2d_list_copy))
                recursive_t2 = Thread(target=check_direction, args=(new_direction_current_tile_x, new_direction_current_tile_y, "up", path_2d_list_copy))
                recursive_t3 = Thread(target=check_direction, args=(new_direction_current_tile_x, new_direction_current_tile_y, "right", path_2d_list_copy))
                recursive_t4 = Thread(target=check_direction, args=(new_direction_current_tile_x, new_direction_current_tile_y, "down", path_2d_list_copy))
                recursive_t1.start()
                recursive_t2.start()
                recursive_t3.start()
                recursive_t4.start()

        # Starts the chain reaction of checking directions and finding intersections
        current_tile_x = int(current_tile["x_coord"] / 50)
        current_tile_y = int(current_tile["y_coord"] / 50)
        t1 = Thread(target=check_direction, args=(current_tile_x, current_tile_y, "left"))
        t2 = Thread(target=check_direction, args=(current_tile_x, current_tile_y, "up"))
        t3 = Thread(target=check_direction, args=(current_tile_x, current_tile_y, "right"))
        t4 = Thread(target=check_direction, args=(current_tile_x, current_tile_y, "down"))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
