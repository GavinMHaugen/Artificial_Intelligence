#this function will look through the given sudoku grid and return the nearest cell
# that has a zero value(aka: a cell that needs to be filled in)
def LocateEmptyCell(SudokuGrid, i , j):

	for x in range(i, 9):
		for y in range(j, 9):
			if SudokuGrid[x][y] == 0:
				return x, y

	for x in range(0, 9):
		for y in range(0, 9):
			if SudokuGrid[x][y] == 0:
				return x, y
	#if none of the for loops trigger a return value then it will return -1 -1
	return -1, -1

#this function will look through each row and column 
def Valid(SudokuGrid, i, j, e):

	ValidRowSol = all([e != SudokuGrid[i][x] for x in range(9)])
	if ValidRowSol:

		ValidColSol = all([e != SudokuGrid[x][j] for x in range(9)])
		if ValidColSol:
			TopXSection = 3 * (i/3)
			TopYSection = 3 * (j/3)
			for x in range(TopXSection, TopXSection+3):
				for y in range(TopYSection, TopYSection+3):
					if SudokuGrid[x][y] == e:
						return False
			return True
	return False

def Solve(SudokuGrid, i=0, j=0):
	i, j = LocateEmptyCell(SudokuGrid, i, j)

	if i == -1:
		return True

	for e in range(1,10):
		if Valid(SudokuGrid, i, j, e):
			SudokuGrid[i][j] = e
			if Solve(SudokuGrid, i, j):
				return True
			SudokuGrid[i][j] = 0
	return False
