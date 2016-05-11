#Gavin Haugen
#AI Spring 2016
#Sudoku Solver

import sys

#The following three functions are used to check the constraint satisfaction 
#problem of the game of sudoku. In the game rules, the same number cannot be in the 
#same row, column, or 3x3 block
def Is_Same_Row(x,y):

	return (x/9 == y/9)

def Is_Same_Col(x,y):

	return (x-y) % 9 == 0

def Is_Same_Block(x,y):

	return (x/27 == y/27 and x%9/3 == y%9/3)

#Made the printing function so that a further expansion could be taken eventually if I wanted to expand the grid
#to x by x for harder or easier puzzles. 
def printGrid (numsPerRow, l):
    printStr = ""
    numsInRow = 1
    for i in range(len(l)):

        item = l[i]
        if numsInRow % numsPerRow == 0:
            printStr += "{0}\n".format(item)
            numsInRow = 1
        else:
            printStr += "{0}\t".format(item)
            numsInRow += 1
    return printStr



#This function takes in a list as an argument and is essentially a depth first search algorithm
#At the point of the function where it recurses, if none of the placements work out, the function will return back at the point where something else
#could actually be used 
#First: we find the nearest 0 and if there are none we return the finshed list printed as a grid because that means the puzzle is done
#Second: we make a set to put excluded numbers in so we know which ones to choose from
#		the number will be added to the excluded numbers if its in the same row, col, or block as the same num being checked
#Third: We check 1-9 to see if its not in the excluded numbers for the current position and if its not we add it to the curr pos and recurse
def RecursiveSolv(grid):
	CantUse = set()
	OneThruNine = '123456789'

	#First part
	FoundZero = grid.find('0')
	#this means that there are no more zeros and the puzzle should now be finished
	#or is already finished when put in as input
	if FoundZero == -1:
		print printGrid(9, grid)


	#Second part
	#we use 81 because 9x9 = 81 cells to check
	for x in range(81):
		if Is_Same_Row(FoundZero, x) or Is_Same_Col(FoundZero, x) or Is_Same_Block(FoundZero, x):
			CantUse.add(grid[x])

	#Third part
	for y in OneThruNine:
		if y not in CantUse:
			RecursiveSolv(grid[:FoundZero]+y+grid[FoundZero+1:])



#Main function to run everything and make sure input is correct
if __name__ == '__main__':
	if len(sys.argv) == 2 and len(sys.argv[1]) == 81:
		RecursiveSolv(sys.argv[1])