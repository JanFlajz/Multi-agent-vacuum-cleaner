class CAgent:
    '''
    Class that handles the autonomy agent
    '''
    def __init__(self, start_pos_x:int, start_pos_y:int, id:int)-> None:
        '''
        Constructor of the class, creates new agent defined by its position and id
        :param start_pos_x: Starting X coordinate of the agent
        :type start_pos_x: int
        :param start_pos_y: Starting Y coordinate of the agent
        :type start_pos_y: int
        :param id: new id of the agent
        :type id: int
        :return: None
        '''
        self.current_pos_x = start_pos_x
        self.current_pos_y = start_pos_y
        self.returned_home = False
        self.id = id
        self.color = 'b'
        

    def set_color(self,color):
        self.color = color
    def get_color(self):
        return self.color
    def set_curr_pos(self,pos_y:int,pos_x:int)->None:
        self.current_pos_x = pos_x
        self.current_pos_y = pos_y

    def set_returned_home(self):
        self.returned_home = True
