


import heapq


from ant_colony_opt import *
from field import *



def new_cmp_lt(self, a,b):
    return a[0] < b[0]


class CPath:
        '''
        This class holds the path used in aco algorithm
        '''

        def __init__(self, start_field: CField, end_field: CField, len: int):
            self.start_field = start_field
            self.end_field = end_field
            self.length = len




class CGarbage:
    def __init__(self,pos_y: int,pos_x:int,id:int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id = id

    def __str__(self)-> str:
        return str(self.id) + ': [' + str(self.pos_y) + ',' + str(self.pos_x) + ']'
    def __eq__(self, other)-> bool:
        return self.id == other.id

    def get_pos_y(self)-> int:
        return self.pos_y
    def get_pos_x(self)->int:
        return self.pos_x

class CMaze:
    '''
    This class holds the loaded maze
    '''
    
    def __getitem__(self, y,x):
        return self[y][x]

    def __init__(self):
        self.agent_starting_position = []
        self.maze = []
        self.garbage = []
        self.garbage.append(CGarbage(1,1,0))
        self.paths = []
        self.num_of_garbage = 0
        self.num_of_agents = 0
        self.distance_matrix = np.zeros(shape=(1,1 ))
        self.path_matrix = [[]]



    def field_is_valid(self, maze:list, pos_y:int, pos_x:int):
        if maze[pos_y][pos_x] != 'X':
            if maze[pos_y][pos_x] != 'B' or (pos_y != 1 and pos_x != 1):
                return True
        return False
    def prepare_line(self, line:list):
        s = ''
        for c in line:
            s += c
        return s

    def generate_garbage(self, maze:list, num_of_garbage:int):

        for i in range(num_of_garbage):
            partX = random.randint(3,self.sizeX - 3)
            partY = random.randint(3,self.sizeY - 3)


            if(self.field_is_valid(maze, partY, partX)):
                partY = partY
                partX = partX
            elif(self.field_is_valid(maze, partY + 1, partX)):
                partY = partY +1
            elif(self.field_is_valid(maze, partY - 1, partX)):
                partY = partY -1
            elif(self.field_is_valid(maze, partY , partX + 1)):
                partX = partX +1
            elif(self.field_is_valid(maze, partY , partX - 1)):
                partX = partX -1


            selected_line = list(maze[partY])
            selected_line[partX] = 'B'
            print("Garbage " + str(i+1) + " at coordinates: [" +str(partY) + ',' + str(partX) + ']')

            maze[partY] = self.prepare_line(selected_line)
            self.garbage.append(CGarbage(partY,partX, i+1))
        print()



    def reconstruct_path(self,start_field:CField,end_field:CField,path:dict)->[list,int]:
        '''
        Reconstructs the generated path so agents have precounted path
        :param start_field: Starting position of path
        :type start_field: CField
        :param end_field: End position of the path
        :type end_field: CField
        :param path: Dictionary path that connects neighbours
        :type path: dict
        :return: path as list and its length
        '''

        curr_field = end_field
        final_path =[]
        while True:
            final_path.append(curr_field)
            if curr_field == start_field:
                return final_path[::-1], len(final_path)
            curr_field = path[curr_field]





    def generate_path_ASTAR(self,start_field:CField, garbage_end_field:CField)-> tuple[list,int]:
        '''
        Generates all paths from garbage to garbage using ASTAR algorithm
        :param start_field: Field to run the a* from
        :type start_field: CField
        :param garbage_end_field: Final destination of the algorithm
        :type garbage_end_field: CField
        :return: path and its lenght
        '''
        expansion = []
        start_field.distance =0
        heapq.heappush(expansion,(0,start_field))
        path = {}
        while len(expansion)>0:
            current_field = heapq.heappop(expansion)[1]
            if current_field.pos_x == garbage_end_field.pos_x and current_field.pos_y == garbage_end_field.pos_y:
                return self.reconstruct_path(start_field,current_field,path)
            new_distance = current_field.distance +1
            for neighbour in current_field.neighbours:
                neighbour.distance = new_distance
                if (neighbour.get_type() == CFieldType.GARBAGE or neighbour.get_type() == CFieldType.EMPTY or neighbour.distance > new_distance) \
                        and neighbour.get_type() != CFieldType.WALL:
                    path[neighbour] = current_field
                    if (neighbour.get_type() != CFieldType.OPEN):
                        heapq.heappush(expansion,(new_distance + count_euclidean_distance_of_fields(neighbour, garbage_end_field), neighbour))
                    else:
                        neighbour.distance = new_distance + count_euclidean_distance_of_fields(neighbour, garbage_end_field)
                    neighbour.set_type(CFieldType.OPEN)
            current_field.set_type(CFieldType.CLOSED)


        return expansion,0

    def generate_all_paths(self):
        nmb_paths = 1
        print("Generating paths...")
        matrix_size = self.num_of_garbage
        self.distance_matrix = np.zeros(shape=(matrix_size, matrix_size))
        self.path_matrix = [[[] for _ in range(matrix_size)] for _ in range(matrix_size)]

        for idx1, g1 in enumerate(self.garbage):
            for idx2, g2 in enumerate(self.garbage):

                self.tmp_path = []
                self.tmp_path_dict = {}
                if g1 == g2:
                    self.distance_matrix[idx1][idx2] = 0
                    continue
                if idx1 < idx2:

                    self.temp_start_field = self.maze_cells[g1.get_pos_y()][g1.get_pos_x()]


                    path,distance = self.generate_path_ASTAR(self.maze_cells[g1.get_pos_y()][g1.get_pos_x()],
                                                        self.maze_cells[g2.get_pos_y()][g2.get_pos_x()])

                    self.distance_matrix[idx1][idx2] = distance
                    self.path_matrix[idx1][idx2] = path

                    nmb_paths += 1
                    maze = self.set_up_maze(self.lines)
                    self.assign_neighbours(maze)

                else:
                    self.distance_matrix[idx1][idx2] = self.distance_matrix[idx2][idx1]
                    self.path_matrix[idx1][idx2] = self.path_matrix[idx2][idx1][::-1]
        print("All paths generated!\n")


    def set_up_maze(self,lines:list):
        maze = [[CField(CFieldType.EMPTY) for i in range(self.sizeX)] for j in range(self.sizeY)]
        y = 0
        for line in lines:
            x = 0
            for letter in line.strip():

                maze[y][x].set_pos_x(x)
                maze[y][x].set_pos_y(y)
                if (letter == 'X'):
                    maze[y][x].set_type(CFieldType.WALL)
                elif (letter == 'B'):
                    maze[y][x].set_type(CFieldType.GARBAGE)

                elif (letter == 'S'):
                    maze[y][x].set_type(CFieldType.AGENT)
                x += 1
            y +=1
        maze[1][1].set_type(CFieldType.COLLECTOR)
        return maze

    def assign_neighbours(self,maze:list):
        for j in range(self.sizeX -1):
            for i in range (self.sizeY -1):
                if maze[i][j].get_type() != CFieldType.WALL:
                    if maze[i-1][j].get_type() != CFieldType.WALL:
                        maze[i][j].save_neighbour(maze[i - 1][j])
                    if maze[i+1][j].get_type() != CFieldType.WALL:
                        maze[i][j].save_neighbour(maze[i + 1][j])
                    if maze[i][j-1].get_type() != CFieldType.WALL:
                        maze[i][j].save_neighbour(maze[i][j-1])
                    if maze[i][j+1].get_type() != CFieldType.WALL:
                        maze[i][j].save_neighbour(maze[i][j+1])

        self.maze_cells = maze

    def read_input_file(self, num_of_garbage:int, num_of_agents:int)->tuple[list,list]:
        
        with open('maze.txt') as file:
            self.lines = file.readlines()
            file.close()
        self.sizeY = len(self.lines)
        self.sizeX = len(self.lines[0])


        #self.generate_agents(self.lines, num_of_agents)
        self.generate_garbage(self.lines, num_of_garbage)
        self.num_of_garbage = num_of_garbage+1
        self.num_of_agents = num_of_agents

        maze = self.set_up_maze(self.lines)
        self.assign_neighbours(maze)
        self.generate_all_paths()
        mTSP = ACO_TSP(self.distance_matrix,self.num_of_agents,self.num_of_garbage)
        best_routes,_ = mTSP.find_paths()
        return best_routes,self.path_matrix



   




        

