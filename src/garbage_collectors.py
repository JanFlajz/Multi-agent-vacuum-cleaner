
import sys
import PySimpleGUI as sg

from agent_control import *
from read_input import  *
import random


#Coordinates of the end point of all agents
BINNER_X = 1
BINNER_Y = 1

#Symbolizes the head of the given agent
all_agents_color = 'Red'



'''
This class is division of maze into parts for every agent.
Each agent has its own part of maze that he searches for 
if he searches his own part and it is still not end of searching,
he changes to a different maze subdivision
'''

def draw_grid(maze_properties:dict)->None:

    '''

    :param maze_properties: Attributes of the given maze that help create graphic representation of the algorithm
    :type maze_properties: dict
    :return: None
    '''
    maze_properties['canvas'].TKCanvas.create_rectangle(
        1, 1, maze_properties['gridSize'], maze_properties['gridSize'], outline='BLACK', width=1)
    for x in range(maze_properties['cellCountX']):
        maze_properties['canvas'].TKCanvas.create_line(
            ((maze_properties['cell_size'] * x), 0), ((maze_properties['cell_size'] * x),
                                       maze_properties['gridSize']),
            fill='BLACK', width=1)
    for z in range(maze_properties['cellCountY']):
        maze_properties['canvas'].TKCanvas.create_line(
            (0, (maze_properties['cell_size'] * z)
             ), (maze_properties['gridSize'], (maze_properties['cell_size'] * z)),
            fill='BLACK', width=1)


def draw_cell(x:int, y:int, maze_properties:dict, color='GREY')-> None:
    '''
    Draw cell to the screen
    :param x: X position of the cell
    :type x: int
    :param y: Y position of the cell
    :type y: int
    :param maze_properties: Attributes of the given maze that help create graphic representation of the algorithm
    :type maze_properties: dict
    :param color: Color of the cell
    :type color: str
    :return: None
    '''
    maze_properties['canvas'].TKCanvas.create_rectangle(
        x, y, x + maze_properties['cell_size'], y + maze_properties['cell_size'],
        outline='BLACK', fill=color, width=1)


def define_cells(maze:CMaze, maze_properties:dict)-> None:
    '''

    :param maze: Instance of the maze used in the problem
    :type maze: CMaze
    :param maze_properties: Attributes of the given maze that help create graphic representation of the algorithm
    :type maze_properties: dict
    :return: None
    '''
    for row in range(maze.sizeY):
        for column in range(maze.sizeX):
            if(maze.maze_cells[row][column].get_type() == CFieldType.WALL):
                draw_cell((maze_properties['cell_size'] * column), (maze_properties['cell_size'] * row), maze_properties)
            elif(maze.maze_cells[row][column].get_type() == CFieldType.AGENT):
                draw_cell((maze_properties['cell_size'] * column), (maze_properties['cell_size'] * row), maze_properties, 'Red')
            elif(maze.maze_cells[row][column].get_type() == CFieldType.GARBAGE):
                draw_cell((maze_properties['cell_size'] * column), (maze_properties['cell_size'] * row), maze_properties, 'Gold')
            elif(maze.maze_cells[row][column].get_type() == CFieldType.COLLECTOR):
                draw_cell((maze_properties['cell_size'] * column),
                          (maze_properties['cell_size']*row), maze_properties,'Purple')


def refresh(posX: int, posY: int, maze_properties:dict,color:str) -> None:
    '''
    Changes the color of the cell in the maze defined by its coordinates
    :param posX: X position of the cell
    :type posX: int
    :param posX: Y position of the cell
    :type posX: int
    :param maze_properties: Attributes of the given maze that help create graphic representation of the algorithm
    :type maze_properties: dict
    :param color: Color of the cell
    :return: None

    '''
    draw_cell(posX * maze_properties['cell_size'], posY * maze_properties['cell_size'], maze_properties, color)
    maze_properties['window'].Read(timeout=10)



def prepare_maze()-> tuple[CMaze,dict,list,list]:

    '''
    Prepares the maze for multiagent system of roombas
    :return newly created maze from input file
    :rtype CMaze
    :return: maze_properties: Changed attributes of the given maze that help create graphic representation of the algorithm
    :rtype dict
    '''
    num_of_agents = int(sys.argv[1])
    #num_of_garbage = 5
    num_of_garbage = random.randint(num_of_agents * 3, num_of_agents * 5)
    print("Number of garbage to find:", num_of_garbage)
    new_maze = CMaze()
    agent_paths,path_matrix = new_maze.read_input_file(num_of_garbage, num_of_agents)
    maze_properties = {'cellCountY': new_maze.sizeY, 'cellCountX': new_maze.sizeX, 'gridSize': 680, 'canvas': False,
                  'window':False, 'cellMAP': False, 'num_of_agents' : num_of_agents, 'num_of_garbage': num_of_garbage}
    maze_properties['cell_size'] = maze_properties['gridSize'] / maze_properties['cellCountX']
    return new_maze, maze_properties,agent_paths, path_matrix



def prepare_layout(maze_properties:dict)->dict:
    '''
    Prepares the graphic representation of the maze
    :param maze_properties: Attributes of the given maze that help create graphic represntation of the algorithm
    :type: maze_properties: dict
    :return: maze_properties: Changed attributes of the given maze that help create graphic represntation of the algorithm
    :rtype dict
    '''

    layout = [[sg.Canvas(size=(maze_properties['gridSize'], maze_properties['gridSize']-100),
                         background_color='white',
                         key='canvas')]]
    maze_properties['window'] = sg.Window(
        'Garbage Agents', layout, resizable=True, finalize=True)
    maze_properties['canvas'] = maze_properties['window']['canvas']
    return maze_properties


def move_agents(mover:CMover, maze_properties:dict)->None:
    '''
    Runs the robot moving algorithm
    :param mover: Class that handles the movement of the agents
    :type mover: CMover
    :param maze_properties: Attributes of the given maze that help create graphic represntation of the algorithm
    :type: maze_properties: dict
    :return: None
    '''


    while True:
        num_agents_at_start = 0

        for agent in mover.agents:

            if agent.returned_home:
                num_agents_at_start += 1
            else:
                refresh(agent.current_pos_x, agent.current_pos_y, maze_properties, agent.get_color())
                pos_y,pos_x = mover.move_one_agent(agent)
                agent.set_curr_pos(pos_y=pos_y,pos_x=pos_x)
                refresh(agent.current_pos_x, agent.current_pos_y, maze_properties, all_agents_color)

        refresh(BINNER_X, BINNER_Y, maze_properties, 'Purple')
        if num_agents_at_start == len(mover.agents):
            print("All garbage was collected!")
            break

def main():

    maze, maze_properties,agent_paths,path_matrix = prepare_maze()

    mover = CMover(maze, maze_properties['num_of_agents'], agent_paths,path_matrix)

    maze_properties = prepare_layout(maze_properties)

    draw_grid(maze_properties)
    define_cells(maze, maze_properties)
    maze_properties['window'].Read(timeout=2000)

    mover.set_up_agents()

    move_agents(mover,maze_properties)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: program.py [number of agents]")
        sys.exit(2)
    main()
