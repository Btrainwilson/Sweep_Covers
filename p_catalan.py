import sys
import operator as op
from functools import reduce
from itertools import permutations
#from sympy.utilities.iterables import multiset_permutations

import xlsxwriter

#Testing function
def test():

        workbook = xlsxwriter.Workbook('2019_1_1_Data.xlsx')
        worksheet = workbook.add_worksheet()

        '''#Test D(n,k)
        for j in range(2,10):
                for i in range(1,10):
                        print("D(%d,%d) = %d" %(j,i,D(j,i)))'''
        #Test P(n,k)
        for j in range(2,10):
                for i in range(1,10):
                        data = P(j,i)
                        print("P(%d,%d) = %d" %(j,i,data))
                        worksheet.write(j, i, data)

        workbook.close()

#Partition Tree enumeration function
#D is the bounded out degree of an infinite tree
#n is the number of partitions desired from the tree
def P(d,n):
        if(n == 1 or d == 1):
                return 2
        
        left_sum = 0
        right_sum = 0

        #Calculate distributions of n into 2 -> d
        for k in range(1,d - 1):
                minor_sum = 0
                for j in range(1,min(d - k + 1,n)):
                        minor_sum += D(d-k,j) * Distribution(k, n - j,d)   #For a given integer partition
                left_sum += ncr(d,k) * minor_sum
                
        right_sum = Distribution(d, n,d)
                

        return left_sum + right_sum + D(d,n)

#Special term for recursion based on integer partitions
#n = groups, k = integer
def Distribution(n,k,d):
        dist_sum = 0
        for p_set in part(k,n):
                permutation_list = list(set(permutations(p_set)))
                for perm in list(permutation_list):
                        product_term = 1        
                        for parti in perm:
                               product_term *= P(d,parti)
                        dist_sum += product_term
        return dist_sum

#Based on the work of : Bona & Mezo 
#https://arxiv.org/pdf/0705.2734.pdf
#Stirling number of n elements where k blocks have atleast 2 elements
def D(n,k):
        if(k > n or n < 1 or k < 1):
                return 0
        sum = 0
        for s in range(n - k, n + 1):
                sum += ncr(n,s) * ((-1)**(n - s))*stirling(s,s+k-n)
        if(sum == -1):
                return 0
        
        return sum

#From falsetru at StackOverflow
#https://stackoverflow.com/questions/18503096/python-integer-partitioning-with-given-k-partitions
#Partitions for distributing n balls into k bins
def part(n, k):
    def memoize(f):
        cache = [[[None] * n for j in range(k)] for i in range(n)]
        def wrapper(n, k, pre):
            if cache[n-1][k-1][pre-1] is None:
                cache[n-1][k-1][pre-1] = f(n, k, pre)
            return cache[n-1][k-1][pre-1]
        return wrapper

    @memoize
    def _part(n, k, pre):
        if n <= 0:
            return []
        if k == 1:
            if n <= pre:
                return [(n,)]
            return []
        ret = []
        for i in range(min(pre, n), 0, -1):
            ret += [(i,) + sub for sub in _part(n-i, k-1, i)]
        return ret
    return _part(n, k, n)


#N choose R
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

# Stirling Algorithm
# Cod3d by EXTR3ME
# https://extr3metech.wordpress.com
#N elements into k partitions
def stirling(n,k):
    n1=n
    k1=k
    if n<=0:
        return 1
     
    elif k<=0:
        return 0
     
    elif (n==0 and k==0):
        return -1
     
    elif n!=0 and n==k:
        return 1
     
    elif n<k:
        return 0
 
    else:
        temp1=stirling(n1-1,k1)
        temp1=k1*temp1
        return (k1*(stirling(n1-1,k1)))+stirling(n1-1,k1-1)

#Number of partitions that contain a single element.
def s_element(d,n):
        stirling_sum = 0
        for i in range(1, n):
                stirling_sum += stirling(d - 1,i)
        return d * stirling_sum

#Main Function

if __name__ == '__main__':
	test()
