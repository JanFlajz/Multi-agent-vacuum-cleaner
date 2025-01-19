
from agents import *


START_X = 1
START_Y = 1


colors = ['Green', 'Blue',  'Pink', 'Brown', 'Beige', 'Orange']
class CMover:

    '''
    This class controls the movement of the agents
    '''
    def __init__(self, maze, num_of_agents:int, agent_paths:list,path_matrix:list):
        self.maze_structure = maze
        self.maze_map = maze.maze_cells
        self.num_of_agents = num_of_agents

        self.agents = []
        self.agent_paths = agent_paths
        self.path_matrix = path_matrix


    def set_up_agents(self)->None:
        '''
        Prepares all agent for usage
        :return: None
        '''
        for i in range(self.num_of_agents):
            agent = CAgent(START_Y, START_X, i)
            agent.set_color(colors[agent.id % len(colors)])
            self.agents.append(agent)


    def move_one_agent(self, agent:CAgent)-> tuple[int,int]:
        '''
        Selects the next position of the agent from the matrix of paths
        :param agent Current agent to be moved
        :type agent CAgent
        :return new coordinates of the agent Y,X
        :rtype tuple[int,int]
        '''


        current_path  = self.agent_paths[agent.id]
        if len(current_path)>1:
            start_filed_idx = 0
            end_field_idx = 1
            if len(self.path_matrix[current_path[start_filed_idx]][current_path[end_field_idx]]) > 0:
                field = self.path_matrix[current_path[start_filed_idx]][current_path[end_field_idx]].pop(0)
                return field.get_pos_y(),field.get_pos_x()
            else:
                _ = self.agent_paths[agent.id].pop(0)
                if len(current_path) == 1:
                    print("Agent " + str(agent.id) + " is back home!")
                    return 1, 1
                print("Agent " + str(agent.id) + " picked up garbage at [" + str(agent.current_pos_y) +',' + str(agent.current_pos_x)+']')
                current_path = self.agent_paths[agent.id]

                field = self.path_matrix[current_path[start_filed_idx]][current_path[end_field_idx]].pop(0)
                return field.get_pos_y(), field.get_pos_x()

        else:
            agent.set_returned_home()
            return 1,1

