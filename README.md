# Sudoku

**A sorta-Bayesian sudoku solver**

Backtracking? Bah, boring. This sudoku solver works with a probability distribution for each cell.

At each iteration, it takes a group of nine cells (a row, column, or block), and:

* normalises each of them (so the total probability in each cell is 1)
* normalises the group (so the probability of each number in the entire row is 1)
* normalises the cells again

Each iteration tends to make the sudoku 'more solved'.

**I think this requires Python 3.8. Beware of the walrus!**
