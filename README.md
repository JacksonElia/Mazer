# Mazer
Uses PyQt5 to paint the mazes. The user can make a maze and then watch as it is solved. Uses brute force threading to solve the maze. Randomly generated mazes are a future addition.

# How it works
The maze is solved by brute force. Essentially, if there is a pathway that it can go into, it does it. 



Each time it branches off into another pathway, it makes a new thread for that pathway. Each thread has a list with its complete history, so when the end is found the shortest path from start to end can be found.

# Use
You're free to use this code as long as you credit me.
