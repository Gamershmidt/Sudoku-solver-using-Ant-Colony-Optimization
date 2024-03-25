# Sudoku Solver using Ant Colony Optimization

## Table of Contents

- [Project Idea](#project-idea)
- [Method/Technique](#methodtechnique)
  - [Pheromone Management](#pheromone-management)
  - [Brief Algorithm Description](#brief-algorithm-description)
- [Dataset Explanation](#dataset-explanation)

## Project Idea

The goal of the project is to develop a Sudoku solver using the Ant Colony Optimization (ACO) algorithm. The solver will be capable of generating solutions for Sudoku puzzles of varying levels of complexity. The implementation of the ACO algorithm to solve Sudoku puzzles is a project that combines puzzle-solving techniques with bioinspired optimization.

## Method/Technique

The Ant Colony Optimization method was chosen to implement Sudoku problems.

### Pheromone Management

**Pheromone matrix:** 
A 2D array that represents the amount of pheromone associated with each possible value for each cell in the Sudoku grid. Initially, all cells have equal pheromone levels, typically set to  $\frac{1}{81}$, indicating an equal likelihood for any value to be chosen for any cell.

- **Global:**
  Updated periodically based on successful solutions to reinforce paths that lead to successful solutions.
- **Local:**
  At each step of ant exploration, local pheromone levels associated with the chosen value in the current cell are updated. This helps the ants choose various paths.

While the puzzle is not solved, during each iteration, ants sequentially traverse the Sudoku board, making one move per iteration. If a cell being explored is not fixed, the ant selects a value from its set of possible values, fixes it in the cell, and updates local pheromone levels. This reinforcement of successful choices aids subsequent ants in selecting promising values.

### Brief Algorithm Description

While puzzle is not solved, during each iteration, antssequentially traverse the Sudoku board, making one move per iteration. If a cell being explored is not fixed, the ant selects a value from its set of possible values, fixes it in the cell, and updates local pheromone levels. This reinforcement of successful choices aids subsequent ants in selecting promising values.

If a cell ends up with an empty set of possible values during exploration, it’s marked as incorrect. Each ant tracks the number of cells it has fixed, subtracting any incorrect cells encountered.

## Dataset Explanation

Our dataset will comprise various Sudoku puzzles that our program will have to solve. The link below leads to the code used for generating Sudoku puzzles. It produces a single string of numbers, where zeros represent empty spaces on the Sudoku grid with size \(9 \times 9\). We will use this code to create 100 examples for our dataset ([accessible link](https://www.kaggle.com/datasets/bryanpark/sudoku)).
