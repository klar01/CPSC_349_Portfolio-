# CPSC481-AI-Connect-4-Project

A repository for files related to the AI Connect 4 project for the Fall 2024 CSUF CPSC481 Artificial Intelligence class.

Collaborators: Klarissa Navarro, Edward Cardenas, Erika Dickson

## Prerequisites

- Python 3.8 or higher installed on your computer.
  If Python is not installed on your system, download and install it from the official Python website: (https://www.python.org/downloads/)
- `pip` package manager (comes with Python).

## Setup Instructions

### Steps:

1. Use github desktop to clone the repository

2. In VScode Click view and click Terminal

3. In the terminal enter `pip install -r requirements.txt`

4. To run the program, after installing all requirements, enter `python main.py`

5. Have fun playing **multiplayer** or going against our AI in **solo** mode!


## Project Description

This is a Python-based Connect 4 game with the following features:
- **Human vs Human**: Play against another player locally.
- **Human vs AI**: Challenge an AI opponent with difficulty levels determined by the depth of its decision-making (3, 4, or 5).

The AI uses a **Minimax algorithm with Alpha-Beta pruning** for decision-making and an **evaluation function** to assess the game state.


## Features

- **Multiple Game Modes**: Choose between Human vs Human, Human vs AI, and AI vs AI.
- **Graphical User Interface**: Built using `pygame` for an interactive gaming experience.


## How the Evaluation Works

The AI uses the **`evaluate_window`** and **`score_position`** functions to analyze the board. Here's a breakdown:

### `evaluate_window(window, piece)`
This function evaluates a slice of the board (a "window") for potential moves:
- **Score Increases**:
  - `+100`: Four in a row (winning condition).
  - `+10`: Three in a row with an open slot.
  - `+4`: Two in a row with two open slots.
  - `+6`: AI's "double threat" (two pairs of two in a row).
- **Score Decreases**:
  - `-8`: Opponent's three in a row with an open slot (block needed).
  - `-4`: Opponent's two in a row with two open slots.
  - `-6`: Opponent's "double threat."

### `score_position(piece)`
This function evaluates the entire board for the given player:
- **Center Column Priority**: Assigns higher weights to moves in the center column to control the board.
- **Horizontal, Vertical, and Diagonal Windows**: Scores all potential four-in-a-row windows on the board using the `evaluate_window` function.

The AI uses this scoring system to identify the best possible move by maximizing its score while minimizing the opponent's.




