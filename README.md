# Reinforcement_Learning_Automated_Car_Simulation

The goal of this exercise is to guide your car to move in a multi-lane straight road
(represented using a rectangular grid) simulator (details explained later). In addition to your
car, there are other cars also moving along the road. You need to design an algorithm which
can take your car from its start position to the end of the road as soon as possible while
avoiding other cars. Other cars are moving randomly. At any step, your car can view up to 4
cells in front, left and right, i.e., it will not be able to look at the other cars which are beyond
its visibility range of 4 cells. (This visibility range of 4 is configurable and your algorithm
should work irrespective of visibility range).
We describe the state, operators and goal state for this problem below.
State: State of the car is its location, i.e., the grid cell it is currently present in.
Operators/Actions: Following are the available operators or actions for the car
(Forward, Forward-2x, Forward-3x, Left, Right, None)
1. Forward – Moves the car one step ahead in the same lane.
2. Forward-2x – Moves the car two steps ahead in the same lane.
3. Forward-3x – Moves the car three steps ahead in the same lane.
4. Left – Moves the car in the left lane and one step forward
5. Right – Moves the car in the right lane and one step forward.
6. None – Stays at the same place.
If the action is unsuccessful then the car will stay at the same place. Action will be
unsuccessful if there is a wall or another car present in the intended direction of move. For
example, a forward will be unsuccessful if there is another car present in front of your car.
As the left action moves a car to the left and one step forward, a left action taken in grid cell
(5,3) will be unsuccessful if there is a car in either of (4,3) or (4,4).
