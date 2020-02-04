def compute_ranks(number, games):
	# points = []
	# goal_diff = []
	# goals_scored = []

	points = [0]*number
	goal_diff = [0]*number
	goals_scored = [0]*number


	# defining 4 arrays of length number - as number of teams = number
	# points for team 0, 1, 2, ... , number-1
	# goal_diff for team 0, 1, 2, ... , number-1
	# goals_scored by team 0, 1, 2, ... , number-1
	# league_position of team 0, 1, 2, ... , number-1


	for i in range(0, number):
	# print(points)
		for j in range(0, number):
			if i != j :
				# print(i,j)
				for k in range(0, len(games)):

					if games[k][0] == i and games[k][1] == j:
						goal_diff[i] += games[k][2] - games[k][3]
						goal_diff[j] += games[k][3] - games[k][2]
						goals_scored[i] += games[k][2]
						goals_scored[j] += games[k][3]

						if games[k][2] > games[k][3]:
							points[i] += 2
						# give Home Team 2 points and Away Team 0 points
						elif games[k][2] == games[k][3]:
							points[i] += 1
							points[j] += 1
						# give Home Team 1 point and Away Team 1 point
						elif games[k][2] < games[k][3]:
							points[j] += 2
						# give Home Team 0 point and Away Team 2 points



	# points_rankdict = {v: k+1 for k,v in enumerate(sorted(set(points),reverse=True))}
	# # creates a mapping (without repeats) where team with most points gets top rank
	# points_ranked = [points_rankdict[i] for i in points]


	rankdict = {v: k+1 for k,v in enumerate(sorted(set(points),reverse=True))}
	# creates a mapping (without repeats) where team with most points gets top rank
	ranked = [rankdict[i] for i in points]

	for i in range(0, number):
		for j in range(0, number):
			if i != j :
				if ranked[i] == ranked[j] and goal_diff[i] > goal_diff[j]:
					ranked[j] = ranked[i] + 1
					for k in range(0, number):
						if ranked[k] > max(ranked[j]-1,ranked[i]) and k != i and k != j:
							ranked[k] += 1
				elif ranked[i] == ranked[j] and goal_diff[i] == goal_diff[j] and goals_scored[i] > goals_scored[j]:
					ranked[j] = ranked[i] + 1
					for k in range(0, number):
						if ranked[k] > max(ranked[j]-1,ranked[i]) and k != i and k != j:
							ranked[k] += 1
				elif ranked[i] == ranked[j] and goal_diff[i] == goal_diff[j] and goals_scored[i] == goals_scored[j]:
					ranked[j] = ranked[i]
					ranked[i] = ranked[j]
					for k in range(0, number):
						if ranked[k] > max(ranked[j]-1,ranked[i]) and k != i and k != j:
							ranked[k] += points.count(i)

	print('points: ', points)
	print('goal_diff: ', goal_diff)
	print('goals_scored: ', goals_scored)
#	print(list(enumerate(points)))
	print('ranking: ',ranked)

compute_ranks(6,
		[[0, 5, 2, 2],
		 [1, 4, 0, 2],
         [2, 3, 1, 2],
         [1, 5, 2, 2],
         [2, 0, 1, 1],
         [3, 4, 1, 1],
         [2, 5, 0, 2],
         [3, 1, 1, 1],
         [4, 0, 2, 0]]   )
# games[0] = Home Team
# games[1] = Away Team
# games[2] = Home Goals
# games[3] = Away Goals
