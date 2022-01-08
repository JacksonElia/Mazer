# Mazer
Uses PyQt5 to paint the mazes. The user can make a maze and then watch as it is solved. Uses brute force threading to solve the maze. Randomly generated mazes are a future addition.

# How it works
The maze is solved by brute force. Essentially, if there is a pathway that it can go into, it does it. 
![image](https://user-images.githubusercontent.com/85963782/148633159-c61a91a1-379c-4e30-93ed-53e3cd8266f0.png)

Each time it branches off into another pathway, it makes a new thread for that pathway. Each thread has a list with its complete history, so when the end is found the shortest path from start to end can be found.
![image](https://user-images.githubusercontent.com/85963782/148633176-bd40226e-b35a-4fdb-a005-d9a66d123ea1.png)

# How to edit a maze
Clicking the edit button changes the gui slightly to:
![image](https://user-images.githubusercontent.com/85963782/148633207-5bf6eeeb-dfe4-415f-802d-82f2b01dd94a.png)
When the user is editing, they can place the start and end of the maze, add or remove walls, and change the height and width of the maze.

# Use
You're free to use this code as long as you credit me.
