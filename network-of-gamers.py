# --------------------------- #
# Intro to CS Final Project   #
# Gaming Social Network       #
# --------------------------- #
#

# Background
# ==========
# You and your friend have decided to start a company that hosts a gaming
# social network site. Your friend will handle the website creation (they know 
# what they are doing, having taken our web development class). However, it is 
# up to you to create a data structure that manages the game-network information 
# and to define several procedures that operate on the network. 
#
# In a website, the data is stored in a database. In our case, however, all the 
# information comes in a big string of text. Each pair of sentences in the text 
# is formatted as follows: 
# 
# <user> is connected to <user1>, ..., <userM>.<user> likes to play <game1>, ..., <gameN>.
#
# For example:
# 
# John is connected to Bryant, Debra, Walter.John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.
# 
# Note that each sentence will be separated from the next by only a period. There will 
# not be whitespace or new lines between sentences.
# 
# Your friend records the information in that string based on user activity on 
# the website and gives it to you to manage. You can think of every pair of
# sentences as defining a user's profile.
#
# Consider the data structures that we have used in class - lists, dictionaries,
# and combinations of the two (e.g. lists of dictionaries). Pick one that
# will allow you to manage the data above and implement the procedures below. 
# 
# You may assume that <user> is a unique identifier for a user. For example, there
# can be at most one 'John' in the network. Furthermore, connections are not 
# symmetric - if 'Bob' is connected to 'Alice', it does not mean that 'Alice' is
# connected to 'Bob'.
#
# Project Description
# ====================
# Your task is to complete the procedures according to the specifications below
# as well as to implement a Make-Your-Own procedure (MYOP). You are encouraged 
# to define any additional helper procedures that can assist you in accomplishing 
# a task. You are encouraged to test your code by using print statements and the 
# Test Run button. 
# ----------------------------------------------------------------------------- 

# Example string input. Use it to test your code.
example_input="John is connected to Bryant, Debra, Walter.\
John likes to play The Movie: The Game, The Legend of Corgi, Dinosaur Diner.\
Bryant is connected to Olive, Ollie, Freda, Mercedes.\
Bryant likes to play City Comptroller: The Fiscal Dilemma, Super Mushroom Man.\
Mercedes is connected to Walter, Robin, Bryant.\
Mercedes likes to play The Legend of Corgi, Pirates in Java Island, Seahorse Adventures.\
Olive is connected to John, Ollie.\
Olive likes to play The Legend of Corgi, Starfleet Commander.\
Debra is connected to Walter, Levi, Jennie, Robin.\
Debra likes to play Seven Schemers, Pirates in Java Island, Dwarves and Swords.\
Walter is connected to John, Levi, Bryant.\
Walter likes to play Seahorse Adventures, Ninja Hamsters, Super Mushroom Man.\
Levi is connected to Ollie, John, Walter.\
Levi likes to play The Legend of Corgi, Seven Schemers, City Comptroller: The Fiscal Dilemma.\
Ollie is connected to Mercedes, Freda, Bryant.\
Ollie likes to play Call of Arms, Dwarves and Swords, The Movie: The Game.\
Jennie is connected to Levi, John, Freda, Robin.\
Jennie likes to play Super Mushroom Man, Dinosaur Diner, Call of Arms.\
Robin is connected to Ollie.\
Robin likes to play Call of Arms, Dwarves and Swords.\
Freda is connected to Olive, John, Debra.\
Freda likes to play Starfleet Commander, Ninja Hamsters, Seahorse Adventures."

remove_primary_from_secondary = True
remove_self_from_secondary = True

#------------------------------------------------------------------------------
# conj stands for conjugation

class ParsedInfo(object):
	"""abstract class for Parsed Information sentence"""
	def __init__(self, conj_start=-1):
		super(ParsedInfo, self).__init__()
		self.conj_start = conj_start
		self.info = None

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return str(self.__class__.__name__) + '(' + \
			str(self.conj_start) + ', ' + str(self.info) + ')'

class ParsedConns(ParsedInfo):
	"""Parsed Connections sentence"""
	conj_str = " is connected to "
	conj_len = len(conj_str)

	def __init__(self, conj_start):
		super(ParsedConns, self).__init__(conj_start)
				
		
class ParsedGames(ParsedInfo):
	"""Parsed Games sentence"""
	conj_str = " likes to play "
	conj_len = len(conj_str)

	def __init__(self, conj_start):
		super(ParsedGames, self).__init__(conj_start)

# Used in network
class UserInfo(object):
	"""Information for individual network users"""
	def __init__(self, games=[], connections=[]):
		super(UserInfo, self).__init__()
		self.games = games
		self.connections = connections

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		return str(self.__class__.__name__) + \
		'(connections=' + str(self.connections) + ', '+ \
		'games=' + str(self.games) + ')'
		

# ----------------------------------------------------------------------------- 
# create_data_structure(string_input): 
#   Parses a block of text (such as the one above) and stores relevant 
#   information into a data structure. You are free to choose and design any 
#   data structure you would like to use to manage the information.
# 
# Arguments: 
#   string_input: block of text containing the network information
#
#   You may assume that for all the test cases we will use, you will be given the 
#   connections and games liked for all users listed on the right-hand side of an
#   'is connected to' statement. For example, we will not use the string 
#   "A is connected to B.A likes to play X, Y, Z.C is connected to A.C likes to play X."
#   as a test case for create_data_structure because the string does not 
#   list B's connections or liked games.
#   
#   The procedure should be able to handle an empty string (the string '') as input, in
#   which case it should return a network with no users.
# 
# Return:
#   The newly created network data structure
def create_data_structure(string_input):
	network = {}

	def next_conjugation():
		conj_conns = string_input.find(ParsedConns.conj_str)
		conj_games = string_input.find(ParsedGames.conj_str)
		
		# Return type indicates conjugation/info type
		if (conj_conns == -1) or (conj_games < conj_conns):
			# -1 can also be returned
			return ParsedGames(conj_start=conj_games)

		else:
			return ParsedConns(conj_start=conj_conns)

	while 1:
		parsed = next_conjugation() # some subclass of ParsedInfo
		conj = parsed.conj_start
		if conj == -1:
			break

		end = string_input.find(".")

		parsed.user = string_input[:conj]
		parsed.info = string_input[(conj+parsed.conj_len) : end] # string
		parsed.info = parsed.info.split(', ') # list of strings

		add_parsed_info(network, parsed)

		if end == -1:
			break
		string_input = string_input[end+1:]

	return network

def add_parsed_info(network, parsed):
	if isinstance(parsed, ParsedConns):
		try:
			# user already added to network
			network[parsed.user].connections = parsed.info
		except KeyError:
			# new user to network
			network[parsed.user] = UserInfo(connections=parsed.info)

	if isinstance(parsed, ParsedGames):
		try:
			network[parsed.user].games = parsed.info
		except KeyError:
			network[parsed.user] = UserInfo(games=parsed.info)
	
#------------------------------------------------------------------------------
def a_user_not_in_network(network, users):
	for u in users:
		if u not in network:
			return True
	return False

# ----------------------------------------------------------------------------- # 
# Note that the first argument to all procedures below is 'network' This is the #
# data structure that you created with your create_data_structure procedure,    #
# though it may be modified as you add new users or new connections. Each       #
# procedure below will then modify or extract information from 'network'        # 
# ----------------------------------------------------------------------------- #

# ----------------------------------------------------------------------------- 
# get_connections(network, user): 
#   Returns a list of all the connections that user has
#
# Arguments: 
#   network: the gamer network data structure
#   user:    a string containing the name of the user
# 
# Return: 
#   A list of all connections the user has.
#   - If the user has no connections, return an empty list.
#   - If the user is not in network, return None.
def get_connections(network, user):
	try:
		return network[user].connections
	except KeyError:
		return None

# ----------------------------------------------------------------------------- 
# get_games_liked(network, user): 
#   Returns a list of all the games a user likes
#
# Arguments: 
#   network: the gamer network data structure
#   user:    a string containing the name of the user
# 
# Return: 
#   A list of all games the user likes.
#   - If the user likes no games, return an empty list.
#   - If the user is not in network, return None.
def get_games_liked(network, user):
	try:
		return network[user].games
	except KeyError:
		return None

# ----------------------------------------------------------------------------- 
# add_connection(network, user_A, user_B): 
#   Adds a connection from user_A to user_B. Make sure to check that both users 
#   exist in network.
# 
# Arguments: 
#   network: the gamer network data structure 
#   user_A:  a string with the name of the user the connection is from
#   user_B:  a string with the name of the user the connection is to
#
# Return: 
#   The updated network with the new connection added.
#   - If a connection already exists from user_A to user_B, return network unchanged.
#   - If user_A or user_B is not in network, return False.
def add_connection(network, user_A, user_B):
	if (user_A not in network) or (user_B not in network):
		return False

	if user_B not in get_connections(network, user_A):
		network[user_A].connections.append(user_B)

	return network

# ----------------------------------------------------------------------------- 
# add_new_user(network, user, games): 
#   Creates a new user profile and adds that user to the network, along with
#   any game preferences specified in games. Assume that the user has no 
#   connections to begin with.
# 
# Arguments:
#   network: the gamer network data structure
#   user:    a string containing the name of the user to be added to the network
#   games:   a list of strings containing the user's favorite games, e.g.:
#		     ['Ninja Hamsters', 'Super Mushroom Man', 'Dinosaur Diner']
#
# Return: 
#   The updated network with the new user and game preferences added. The new user 
#   should have no connections.
#   - If the user already exists in network, return network *UNCHANGED* (do not change
#     the user's game preferences)
def add_new_user(network, user, games):
	if user not in network:
		network[user] = UserInfo(games=games)

	return network
		
# ----------------------------------------------------------------------------- 
# get_secondary_connections(network, user): 
#   Finds all the secondary connections (i.e. connections of connections) of a 
#   given user.
# 
# Arguments: 
#   network: the gamer network data structure
#   user:    a string containing the name of the user
#
# Return: 
#   A list containing the secondary connections (connections of connections).
#   - If the user is not in the network, return None.
#   - If a user has no primary connections to begin with, return an empty list.
# 
# NOTE: 
#   It is OK if a user's list of secondary connections includes the user 
#   himself/herself. It is also OK if the list contains a user's primary 
#   connection that is a secondary connection as well.
def get_secondary_connections(network, user):
	if user not in network:
		return None
	
	primary = get_connections(network, user)
	secondary = set([])

	for p in primary:
		secondary = secondary.union(set(get_connections(network, p)))

	if remove_primary_from_secondary:
		secondary = secondary.difference(primary)
	if remove_self_from_secondary:
		try:
			secondary.remove(user)
		except KeyError:
			pass

	return list(secondary)

# ----------------------------------------------------------------------------- 	
# count_common_connections(network, user_A, user_B): 
#   Finds the number of people that user_A and user_B have in common.
#  
# Arguments: 
#   network: the gamer network data structure
#   user_A:  a string containing the name of user_A
#   user_B:  a string containing the name of user_B
#
# Return: 
#   The number of connections in common (as an integer).
#   - If user_A or user_B is not in network, return False.
def count_common_connections(network, user_A, user_B):
	if (user_A not in network) or (user_B not in network):
		return False
	connections_A = get_connections(network, user_A)
	connections_B = get_connections(network, user_B)

	tally = 0
	for u in connections_A:
		if u in connections_B:
			tally += 1

	return tally

# ----------------------------------------------------------------------------- 
# find_path_to_friend(network, user_A, user_B): 
#   Finds a connections path from user_A to user_B. It has to be an existing 
#   path but it DOES NOT have to be the shortest path.
#   
# Arguments:
#   network: The network you created with create_data_structure. 
#   user_A:  String holding the starting username ("Abe")
#   user_B:  String holding the ending username ("Zed")
# 
# Return:
#   A list showing the path from user_A to user_B.
#   - If such a path does not exist, return None.
#   - If user_A or user_B is not in network, return None.
#
# Sample output:
#   >>> print find_path_to_friend(network, "Abe", "Zed")
#   >>> ['Abe', 'Gel', 'Sam', 'Zed']
#   This implies that Abe is connected with Gel, who is connected with Sam, 
#   who is connected with Zed.
# 
# NOTE:
#   You must solve this problem using recursion!
# 
# Hints: 
# - Be careful how you handle connection loops, for example, A is connected to B. 
#   B is connected to C. C is connected to B. Make sure your code terminates in 
#   that case.
# - If you are comfortable with default parameters, you might consider using one 
#   in this procedure to keep track of nodes already visited in your search. You 
#   may safely add default parameters since all calls used in the grading script 
#   will only include the arguments network, user_A, and user_B.
def find_path_to_friend(network, user_A, user_B):
	if (user_A not in network) or (user_B not in network):
		return False
	# your RECURSIVE solution here!

	def recurse_find(current_level, visited):
		# types: list of lists (paths), set of strings (users)

		# check current depth
		# last node is path[-1]
		for path in current_level:
			if path[-1] == user_B:
				return path
		
		next_level = []
		visited = visited.union(set([path[-1] for path in current_level]))

		for path in current_level:
			# potential next-level
			to_add = get_connections(network, path[-1])
			for nlu in to_add: # next-level user
				if nlu not in visited:
					next_level.append(path + [nlu])

		if next_level:
			return recurse_find(next_level, visited)
		else:
			# all leads have been exhausted, no solution
			return None
	
	return recurse_find([[user_A]], set([]))


# Make-Your-Own-Procedure (MYOP)
# ----------------------------------------------------------------------------- 
# Your MYOP should either perform some manipulation of your network data 
# structure (like add_new_user) or it should perform some valuable analysis of 
# your network (like path_to_friend). Don't forget to comment your MYOP. You 
# may give this procedure any name you want.

# Replace this with your own procedure! You can also uncomment the lines below
# to see how your code behaves. Have fun!


net = create_data_structure("")
net = create_data_structure(example_input)
print net

print get_connections(net, "Debra")
print get_connections(net, "Mercedes")
print get_games_liked(net, "John")

add_connection(net, "John", "Freda")
print "Freda" in get_connections(net, "John")

before = net["Debra"]
add_new_user(net, "Debra", [])
print net["Debra"] == before

add_new_user(net, "Nick", ["Seven Schemers", "The Movie: The Game"]) # True
print net["Nick"]

print get_secondary_connections(net, "Mercedes")
print count_common_connections(net, "Mercedes", "John")
print find_path_to_friend(net, "John", "Ollie")
print find_path_to_friend(net, "Ollie", "John")
print find_path_to_friend(net, "John", "Nick")
print find_path_to_friend(net, "Nick", "Ollie")
