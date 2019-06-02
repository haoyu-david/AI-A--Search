from search import *
import time

def make_rand_8puzzle():
	l = random.sample(range(9), 9)
	state = tuple(l)
	eightPuzzle = EightPuzzle(state)
	while not eightPuzzle.check_solvability(state):
		l = random.sample(range(9), 9)
		state = tuple(l)
	eightPuzzle = EightPuzzle(state)

	return eightPuzzle

def display(state):
	l = list(state)
	for i in range(len(l)):
		if l[i] == 0:
			l[i] = '*'

	for i in range(0, len(l), 3):
		print(l[i], end=' ')
		print(l[i+1], end=' ')
		print(l[i+2])

	return

def make_rand_yPuzzle():
	l = random.sample(range(9), 9)
	l.insert(1, 9)
	l.insert(9, 10)
	l.insert(11, 11)

	state = tuple(l)
	yPuzzle = YPuzzle(state)
	while not yPuzzle.check_solvability(state):
		l = random.sample(range(9), 9)
		l.insert(1, 9)
		l.insert(9, 10)
		l.insert(11, 11)
		state = tuple(l)
	yPuzzle = YPuzzle(state)

	return yPuzzle

def displayY(state):
	l = list(state)
	for i in range(len(l)):
		if l[i] == 0:
			l[i] = '*'
		if l[i] == 9 or l[i] == 10 or l[i] == 11:
			l[i] = ' '

	for i in range(0, len(l), 3):
		print(l[i], end=' ')
		print(l[i+1], end=' ')
		print(l[i+2])

	print(l)
	return

def manhattan(node):
	state = node.state
	index_goal = {1:[0,0], 2:[0,1], 3:[0,2], 4:[1,0], 5:[1,1], 6:[1,2], 7:[2,0], 8:[2,1], 0:[2,2]}
	index_state = {}
	index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2]]

	for i in range(len(state)):
		index_state[state[i]] = index[i]
	mhd = 0
	for i in range(9):
		if (i != 0):
			mhd = mhd + abs(index_goal[i][0] - index_state[i][0]) + abs(index_goal[i][1] - index_state[i][1])

	return mhd

def manhattanY(node):
	state = node.state
	index_goal = {1:[0,0], 2:[0,2], 3:[1,0], 4:[1,2], 5:[1,3], 6:[2,0], 7:[2,1], 8:[2,2], 0:[3,1]}
	index_state = {}
	index = [[0,0], [0,1], [0,2], [1,0], [1,1], [1,2], [2,0], [2,1], [2,2], [3,0], [3,1], [3,2]]

	for i in range(len(state)):
		index_state[state[i]] = index[i]
	mhd = 0
	for i in range(9):
		if (i != 0 and i != 9 and i != 10 and i != 11):
			mhd = mhd + abs(index_goal[i][0] - index_state[i][0]) + abs(index_goal[i][1] - index_state[i][1])

	return mhd

def maxh(n):
	eightPuzzle = EightPuzzle((0, 0, 0, 0, 0, 0, 0, 0, 0))
	return max((eightPuzzle.h(n), manhattan(n)))

def maxhY(n):
	yPuzzle = YPuzzle((0,0,0,0,0,0,0,0,0,0,0,0))
	return max((yPuzzle.h(n), manhattanY(n)))

# def astar_search_max(problem, h1, h2):
# 	"""A* search is best-first graph search with f(n) = g(n)+h(n).
#     You need to specify the h function when you call astar_search, or
#     else in your Problem subclass."""
# 	# h = memoize(h or problem.h, 'h')
# 	return best_first_graph_search(problem, lambda n: n.path_cost + max(h1(n), h2(n)))

def timing(fun, prob, h):
	start_time = time.time()

	node = fun(prob, h)

	elapsed_time = time.time() - start_time

	print(node.depth)
	print(f'elapsed time (in seconds): {elapsed_time}')
	return


class YPuzzle(Problem):
	""" The problem of sliding tiles numbered from 1 to 8 on a 3x3 board,
    where one of the squares is a blank. A state is represented as a tuple of length 9,
    where element at index i represents the tile number  at index i (0 if it's an empty square) """

	def __init__(self, initial, goal=(1, 9, 2, 3, 4, 5, 6, 7, 8, 10, 0, 11)):
		""" Define goal state and initialize a problem """

		self.goal = goal
		Problem.__init__(self, initial, goal)

	def find_blank_square(self, state):
		"""Return the index of the blank square in a given state"""

		return state.index(0)

	def actions(self, state):
		possible_actions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
		index_blank_square = self.find_blank_square(state)

		if (index_blank_square == 0 or index_blank_square == 2):
			possible_actions.remove('UP')
			possible_actions.remove('LEFT')
			possible_actions.remove('RIGHT')
		elif (index_blank_square == 1 or index_blank_square == 9 or index_blank_square == 11):
			possible_actions.remove('UP')
			possible_actions.remove('DOWN')
			possible_actions.remove('LEFT')
			possible_actions.remove('RIGHT')
		elif (index_blank_square == 3):
			possible_actions.remove('LEFT')
		elif(index_blank_square == 4):
			possible_actions.remove('UP')
		elif (index_blank_square == 5):
			possible_actions.remove('RIGHT')
		elif (index_blank_square == 6):
			possible_actions.remove('LEFT')
			possible_actions.remove('DOWN')
		elif (index_blank_square == 8):
			possible_actions.remove('RIGHT')
			possible_actions.remove('DOWN')
		elif(index_blank_square == 10):
			possible_actions.remove('DOWN')
			possible_actions.remove('LEFT')
			possible_actions.remove('RIGHT')

		return possible_actions

	def result(self, state, action):
		""" Given state and action, return a new state that is the result of the action.
        Action is assumed to be a valid action in the state """

		# blank is the index of the blank square
		blank = self.find_blank_square(state)
		new_state = list(state)

		delta = {'UP': -3, 'DOWN': 3, 'LEFT': -1, 'RIGHT': 1}
		neighbor = blank + delta[action]
		new_state[blank], new_state[neighbor] = new_state[neighbor], new_state[blank]

		return tuple(new_state)

	def goal_test(self, state):
		""" Given a state, return True if state is a goal state or False, otherwise """

		return state == self.goal

	def check_solvability(self, state):
		""" Checks if the given state is solvable """

		if state.index(1) != 0 and state.index(1) != 3:
			return False
		if state.index(2) != 2 and state.index(2) != 5:
			return False
		if state.index(7) != 7 and state.index(7) != 10:
			return False
		if state[0] != 1 and state[3] != 0:
			return False
		if state[2] != 2 and state[5] != 0:
			return False
		if (state[7] == 7 and state[10] != 0):
			return False

		inversion = 0
		for i in range(len(state)):
			for j in range(i + 1, len(state)):
				if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
					inversion += 1

		if (state[0] == 0 and state[3] == 1):
			return inversion % 2 == 0
		if (state[2] == 0 and state[5] != 2):
			return inversion % 2 != 0

		return inversion % 2 != 0

	def h(self, node):
		""" Return the heuristic value for a given state. Default heuristic function used is
        h(n) = number of misplaced tiles """

		return sum(s != g for (s, g) in zip(node.state, self.goal))


def main():
	for i in range(10):
		eightPuzzle = make_rand_8puzzle()
		display(eightPuzzle.initial)
		print(eightPuzzle.initial)
		timing(astar_search, eightPuzzle, eightPuzzle.h)
		timing(astar_search, eightPuzzle, manhattan)
		timing(astar_search, eightPuzzle, maxh)
		print()

	for i in range(10):
		yPuzzle = make_rand_yPuzzle()
		displayY(yPuzzle.initial)
		timing(astar_search, yPuzzle, yPuzzle.h)
		timing(astar_search, yPuzzle, manhattanY)
		timing(astar_search, yPuzzle, maxhY)
		print()

if __name__ == '__main__':
	main()