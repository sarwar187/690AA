# 690AA
Minimizing sum of completion times and MAX-SAT problem

# MAX-SAT problem
The code for this problem is present in randomized.py. In order to use it run python randomized.py. In this problem we are given as input N literals and M clauses in Conjunctive Normal form with different weights and the objective is to set the literals in such a way so that the sum of weights of satisfied clauses is maximized. In order to take input for this problem, I define a negation array for each clause. So a clause such as (X1 OR X2 OR ~X4) is represented by 2 arrays: The literal array [1,2,4] and the negation array [0,0,1] (simply denotes which literal is negated). While running the code the user is first asked for the number of literals (N) and the number of clauses (M) and then for each clause the user is asked to enter the weight of the clause, the number of literals in the clause, the literal array (numbers separated by spaces) and the negation array ( numbers separated by spaces again). So a sample run will look like this:

python randomized.py

Number of literals: 5

Number of Clauses: 2

Enter the weight of Clause 1: 17

Enter the number of literals of Clause 1: 3

Enter the literals here separated by space: 1 2 3

Enter the negation array separated by space: 0 1 0

Enter the weight of Clause 2: 25

Enter the number of literals of Clause 2: 3

Enter the literals here separated by space: 2 4 5

Enter the negation array separated by space: 0 1 0

The code outputs the solution found by all the 4 techniques taught in class (Derandomized versions)

1) All literals are true iid with probability 0.5

2) All literals are true iid with probability p

3) All literals are true iid according to different probabilities found by solving a LP

4) Best of (3) and (2) giving a 3/4 approximation factor

# Sum of Completion Times Problem




