# Multi-agent-vacuum-cleaner

In this project, I developed a multiagent system of vacuum cleaners. 
The goal is to find the most efficient way of cleaning all garbage in the maze.
The vacuum cleaners know the coordinates of all pieces of garbage. The optimal shortest path between each piece of garbage and is computed using the A* algorithm and the optimal path for each individual cleaner is computed using the Ant colony optimization algorithm. 

The program also uses PySimpleGUI library for graphical interface.



##Usage
cd src
pip -r install requirements.txt
python .\garbage_collectors.py [num of agents]