'''
This file serves for implementation of ACO algorithm for optimizing the TSP problem.
https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms

Implementation was inspired by this video https://www.youtube.com/watch?v=u7bQomllcJw

This is basic implementation of the ACO algorithm that works like this:

For each agent it computes the next state by updating the probabilities based on pheromone and distance matrix (create_new_path()).
Then it updates the pheromone level based on constant Q.
This runs for 1000 iterations

The multiagent version is done by dividing the original path to the size of max num_of_garbage/num_of_agents +1.
This does not lead to the best solution for mTSP.
It is just a possible modification :)

'''


import numpy as np
import random
class ACO_TSP():
    def __init__(self,distance_matrix:np.ndarray, num_of_agents:int,num_of_garbage:int):

        self.num_of_garbage = num_of_garbage
        self.num_of_agents = num_of_agents

        #matrix of distances computed using A*
        self.distance_matrx = distance_matrix
        #heurisitc matrix that defines the desirability of transition to another state with small coeficient to remove division by zero in the
        self.heuristic_matrix = 1/(self.distance_matrx + 1e-12)

        #number of iteration of the experiment
        self.num_of_ants = 1000
        #constant that changes pheromone level
        self.Q = 100
        #controls the trail level of the move to the next state
        self.alfa = 1
        #controls the attractivness of the move to the next state
        self.beta =2
        #pheromon evaporetion coeficient
        self.rho = 0.15
        #pheromons on given paths
        self.pheromones_matrix = np.ones(shape=(num_of_garbage, num_of_garbage))/num_of_garbage

    def count_path_len(self, path:list)->int:
        '''
        Computes the length of selected path. Uses the units from the original distance matrix
        :param path: Path to have its distance computed
        :type path: list
        :return length of the path
        :rtype int
        '''
        return sum(self.distance_matrx[path[i]][path[i + 1]] for i in range(len(path) - 1))
    def update_pheromones(self,paths:list,distances:list)->None:
        '''
        Updates the pheromones for all routes in the paths
        :param paths: All generated paths in one iteration
        :type paths: list
        :param distances: All generated paths in one iteration
        :type distances: list
        '''
        self.pheromones_matrix = self.pheromones_matrix *(1-self.rho)

        for path,distance in zip(paths,distances):
            deposited_pheromone = self.Q/distance
            for i in range(len(path)-1):
                self.pheromones_matrix[path[i]][path[i+1]] += deposited_pheromone
                self.pheromones_matrix[path[i+1]][path[i]] += deposited_pheromone


    def count_garbage_probabilities(self,current_garbage:int,remaining_garbage:list)->np.array:
        '''
        Computes probabilites of garbe being next in the path
        :param current_garbage: most recent point in the path
        :type current_garbage: int
        :param remaining_garbage: remaining garbages
        :type remaining_garbage: list
        :return: Probabilities of each remaining garbage being picked
        '''
        probabilities = []
        for next_garbage in remaining_garbage:
            tau = self.pheromones_matrix[current_garbage][next_garbage] ** self.alfa
            eta = self.heuristic_matrix[current_garbage][next_garbage] ** self.beta
            probabilities.append(tau*eta)
        probabilities = np.array(probabilities)
        return probabilities / sum(probabilities)
    def create_new_path(self,unsucced_garbage:set)->list:
        '''
        Generates new path from set of remaining garbage
        :param unsucced_garbage: set of remaining garbage
        :rtype set
        :return: new generated path
        :rtype: list
        '''
        new_path = []
        starting_point = 0
        new_path.append(starting_point)
        current_garbage = starting_point
        while unsucced_garbage:
            unsucced_garbage_list = list(unsucced_garbage)

            g_probabilities = self.count_garbage_probabilities(current_garbage, unsucced_garbage_list)

            next_garbage = random.choices(unsucced_garbage_list, weights=g_probabilities, k=1)[0]

            new_path.append(next_garbage)
            unsucced_garbage.remove(next_garbage)

            current_garbage = next_garbage
            '''
            This distributes the paths among the agents which does not always lead to same-length paths.    
            '''
            if len(new_path) > self.num_of_garbage / self.num_of_agents+1:
                break
        new_path.append(starting_point)
        return new_path


    def find_paths(self)->tuple[list,float]:
        '''
        Finds the best paths for all agents using ACO
        :return: list of the best paths and the best (smallest) length
        :rtype: tuple
        '''
        best_paths = []
        best_len =  float("inf")

        for i in range(self.num_of_ants):
            all_paths = []
            all_distances = []
            #the zero symbolizes the starting point
            unsucced_garbage = set(range(1,self.num_of_garbage))

            for _ in range(self.num_of_agents):
                if not unsucced_garbage: break
                new_path = self.create_new_path(unsucced_garbage)
                all_paths.append(new_path)
                all_distances.append(self.count_path_len(new_path))

            total_len = sum(all_distances)

            if total_len < best_len:
                best_paths = all_paths
                best_len = total_len
            self.update_pheromones(all_paths,all_distances)

        return best_paths,best_len




