# robot_pathfinding_MDP
This is a project for the Artificial Intelligence course of TÉLÉCOM Nancy. The goal of the project is to implement a robot that can find the shortest path in a maze using Markov Decision Process.

## How to run the code
To run the code, you need to have python 3.6 installed on your computer.
You also need to install the following python libraries:
  - numpy
  - random
  - tkinter
  - customtkinter
  - Pillow

Then, you can run the code by typing the following command in the terminal:
```
python3 ui.py
```

## How to use the interface
The interface is composed of 2 parts.

The right part is the settings panel. You can change :
  - the discount factor (gamma)
  - the size of the maze
  - the reward for the goal
  - the reward for the swamp 
  - the reward for the firecamp.

Once you have changed the settings, you can click on the "Generate grid" button to create the maze.

The left part is the maze. You can click on the cells to change their state. The cells can be:
  - Green: the cell is empty
  - Grey: the cell is the starting point
  - Red: the cell is the goal 
  - Brown: the cell is a swamp
  - Orange: the cell is a firecamp

There can be only one starting point and one goal in the maze. The firecamps are optional.

Once you have created the maze, you can click on the "Find path !" button to solve the maze.

## How to read the results

The value of each cell is displayed in the cell. 

The policy of each cell is displayed by an arrow in the cell. 

The path from the starting point to the goal is displayed by red arrows.
