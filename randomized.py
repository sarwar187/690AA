#This code solves the MAX_SAT problem. THe input for a MAX_SAT is a set of N variables and M clauses 
#where each clause consists of disjunction of some number of variables and their negation. The 
# objective is to maximize the weight of the satisfied clauses.

#The input should be provided in the following way:
# In the first line enter the number of variables N when prompted 
# In the second line enter the number of clauses M when prompted
# For each clause first enter the weight of the clause and then the number of literals in that clause 
# Then enter the literals separated by space and the negation array separated by space on being prompted

#are you assuming literals in a clause are ordered?
#can we store the clauses already satisfied? It would reduce the complexity from n^2 to n

import numpy as np  
import random
import sys
from scipy.optimize import linprog

#Take Input

N=int(raw_input("Number of literals: "))
M=int(raw_input("Number of Clauses: "))

weights=[]
clauses=[]
negation=[]

for i in range(M):
    weights.append(int(raw_input("Enter the weight of Clause "+str(i+1)+": ")))
    no_of_literals=int(raw_input("Enter the number of literals of Clause "+str(i+1)+": "))
    clauses.append([int(x) for x in raw_input("Enter the literals here separated by space: ").split()])
    negation.append([int(x) for x in raw_input("Enter the negation array separated by space: ").split()])

#Checks if a clause is already satisfied by determined literals

def is_clause_already_satisfied(index_of_clause,literals_determined):
    for literal_index,literal in enumerate(clauses[index_of_clause]):
        if(literal<=len(literals_determined)):
            if (negation[index_of_clause][literal_index]+literals_determined[literal-1]==1):
                return True
    return False            

#For a set of determined literals and random literals returns the expected weight of satisfied clauses
#when all literals are set true independently with probability 0.5
def conditional_expectation_method1(literals_determined):
    val=0.0
    for i in range(len(clauses)):
        if (is_clause_already_satisfied(i,literals_determined)):
            val+=weights[i]
        else:
            number_of_random_literals=len([c for c in clauses[i] if c>len(literals_determined)])
            val+=(1-(0.5)**number_of_random_literals)*weights[i]
    return val             

# Derandomized version of algorithm with all literals are random iid with probability of being set true=0.5
def derandomized_algorithm_method1():
    literals_determined=[]
    for i in range(N):
        if(conditional_expectation_method1(literals_determined+[1])>conditional_expectation_method1(literals_determined+[0])):
            literals_determined=literals_determined+[1]
        else:
            literals_determined=literals_determined+[0]
    return literals_determined

#For a set of determined literals and random literals returns the expected weight of satisfied clauses
#when all literals are set true independently with probability p
def conditional_expectation_method2(literals_determined,p):
    val=0.0
    for i in range(len(clauses)):
        if (is_clause_already_satisfied(i,literals_determined)):
            val+=weights[i]
        else:
            number_of_negated_random_literals=len([c for (index,c) in enumerate(clauses[i]) if (c>len(literals_determined) and negation[i][index]==1)])
            number_of_unnegated_random_literals=len([c for (index,c) in enumerate(clauses[i]) if (c>len(literals_determined) and negation[i][index]==0)])
            val+=(1-((p)**number_of_negated_random_literals)*((1-p)**(number_of_unnegated_random_literals)))*weights[i]
    return val             

# Derandomized version of algorithm with all literals are random iid with probability of being set true=p
def derandomized_algorithm_method2():
    p=(np.sqrt(5)-1)*0.5
    literals_determined=[]
    for i in range(N):
        if(conditional_expectation_method2(literals_determined+[1],p)>conditional_expectation_method2(literals_determined+[0],p)):
            literals_determined=literals_determined+[1]
        else:
            literals_determined=literals_determined+[0]
    return literals_determined

#Solves linear program showed in class
def solve_linear_program():
    c= np.concatenate((np.array(weights),np.zeros(N)))
    A_ub=np.zeros((M,M+N))
    B_ub=np.zeros(M)
    for i in range(M):
        A_ub[i,i]=1;counter=0
        for index,j in enumerate(clauses[i]):
            if(negation[i][index]==0):
                A_ub[i,M-1+j]=-1
            else:
                A_ub[i,M-1+j]=1;counter+=1
        B_ub[i]=counter
    res = linprog(-c, A_ub=A_ub, b_ub=B_ub, bounds=(0,1),options={"disp": True}) 
    return res.x           

#For a set of determined literals and random literals returns the expected weight of satisfied clauses
#when all literals are set true independently according to a given probability vector            
def conditional_expectation_method3(literals_determined,probability_vector):
    val=0.0
    for i in range(len(clauses)):
        if (is_clause_already_satisfied(i,literals_determined)):
            val+=weights[i]
        else:
            prob_clause_notsatisfied=1.0
            prob_clause_notsatisfied=np.product([probability_vector[c-1] for (index,c) in enumerate(clauses[i]) if (c>len(literals_determined) and negation[i][index]==1)])
            prob_clause_notsatisfied*=np.product([1-probability_vector[c-1] for (index,c) in enumerate(clauses[i]) if (c>len(literals_determined) and negation[i][index]==0)])
            #print prob_clause_notsatisfied
            val+=(1-prob_clause_notsatisfied)*weights[i]
    return val             

#Derandomized version of algorithm using randomized rounding of Linear Program
def derandomized_algorithm_method3():
    probability_vector=solve_linear_program()[M:]
    literals_determined=[]
    for i in range(N):
        if(conditional_expectation_method2(literals_determined+[1],probability_vector)>conditional_expectation_method2(literals_determined+[0],probability_vector)):
            literals_determined=literals_determined+[1]
        else:
            literals_determined=literals_determined+[0]
    return literals_determined

#Best solution that give 3/4 approximation factor
def best_solution_from_method3_and_method2():
    solution1=derandomized_algorithm_method2()
    solution2=derandomized_algorithm_method3()
    if conditional_expectation_method1(solution1)>conditional_expectation_method1(solution2):
        return solution1
    else:
        return solution2    


print derandomized_algorithm_method1()
print derandomized_algorithm_method2()
print derandomized_algorithm_method3()
print best_solution_from_method3_and_method2()
    



