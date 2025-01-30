from MDP import MDP
import pandas as pd

class MDP_Scenario1(MDP):
    def __init__(self):
        # constructor method initializes an instance of the 'MDP' class
        print('Initializing..')
        self.create_state_space()
        # init_state: 
        # [0]The door is closed (T); 
        # [1]The door is open (F); 
        # [2]The robot is holding the suitcase (F);
        # [3]The robot is not holding the suitcase (T); 
        # [4]The suitcase is inside the room (F); 
        # [5]The suitcase is outside the room (T).
        self.init_state = (True, False, False, True, False, True)
        self.goal_states = [(True, False, True, False, False, True)]
        self.discount = 0.99

    def get_state_space(self):
        return self.state_space # state space represents all possible states the system can be in

    def get_actions(self):
        # returns the of possible actions that can be taken in the MDP
        # act1: Open the door
        # act2: Move to the room
        # act3: Pick up the suitcase
        # act4: Dropoff the suitcase inside the room
        # act5: Exit the task
        self.actions = ["act1", "act2", "act3", "act4", "act5"]
        return self.actions
    
    def decode_actions(self, act):
        match act:
            case "act1":
                act_string = "Open the door"
            case "act2":
                act_string = "Move to the room"
            case "act3":
                act_string = "Pick up the suitcase"
            case "act4":
                act_string = "Dropoff the suitcase inside the room"
            case "act5":
                act_string = "Exit the task"
            case _:
                act_string = "No action is taken"
        return act_string

    def get_transition_probability(self, state, action, next_state):
        # intended to return the transition probability from one state to another given an action
        # list all possible transition:
        if (# Condition 1 - act1 "Open the door": 
            # fact1 "The door is closed" becomes False after the action
            # fact2 "The door is open" becomes True after the action
            # other facts stay the same
            ((action == "act1") and 
             (next_state[0] == False) and (next_state[1] == True) and 
             (state[2] == next_state[2]) and (state[3] == next_state[3]) and 
             (state[4] == next_state[4]) and (state[5] == next_state[5]))
            # Condition 2 - act2 "Move to the room":
            # fact1 "The door is closed" is False, and still False after the action
            # fact2 "The door is open" is True, and still True after the action
            # If the robot is holding the suitcase (fact3 True, fact4 False):
                # fact5 "The suitcase is inside the room" becomes True after the action
                # fact6 "The suitcase is outside the room" becomes False after the action
            # If the robot is not holding the suitcase (fact3 False, fact4 True):
                # fact5 "The suitcase is inside the room" is False, and still False after the action
                # fact6 "The suitcase is outside the room" is True, and still True after the action
            # other facts stay the same
            or ((action == "act2") and 
                (state[0] == False) and (next_state[0] == False) and 
                (state[1] == True) and (next_state[1] == True) and 
                (state[2] == True) and (next_state[2] == True) and
                (state[3] == False) and (next_state[3] == False) and
                (next_state[4] == True) and (next_state[5] == False))
            or ((action == "act2") and 
                (state[0] == False) and (next_state[0] == False) and 
                (state[1] == True) and (next_state[1] == True) and 
                (state[2] == False) and (next_state[2] == False) and
                (state[3] == True) and (next_state[3] == True) and
                (next_state[4] == False) and (next_state[5] == True))
            # Condition 3 - act3 "Pick up the suitcase": 
            # fact3 "The robot is holding the suitcase" becomes True after the action
            # fact4 "The robot is not holding the suitcase" becomes False after the action
            # other facts stay the same
            or ((action == "act3") and 
                (next_state[2] == True) and (next_state[3] == False) and 
                (state[0] == next_state[0]) and (state[1] == next_state[1]) and 
                (state[4] == next_state[4]) and (state[5] == next_state[5]))
            # Condition 4 - act4 "Dropoff the suitcase inside the room": 
            # fact3 "The robot is holding the suitcase" is True, then becomes False after the action
            # fact4 "The robot is not holding the suitcase" is False, then becomes True after the action
            # fact5 "The suitcase is inside the room" is True, and still True after the action
            # fact6 "The suitcase is outside the room" is False, and still False after the action
            # other facts stay the same
            or ((action == "act4") and 
                (state[2] == True) and (next_state[2] == False) and 
                (state[3] == False) and (next_state[3] == True) and 
                (state[4] == True) and (next_state[4] == True) and 
                (state[5] == False) and (next_state[5] == False) and 
                (state[0] == next_state[0]) and (state[1] == next_state[1]))
            # Condition 5 - act5 "Exit the task": 
            # enter to absorber state "Terminate" after the action
            or ((action == "act5") and (next_state == "Terminate"))):
            return 1
        else:
            return 0

    def get_init_state(self):
        return self.init_state # returns the initial state of the MDP

    def get_state_hash(self, state):
        return str(state) # returns a hashable representation (specifically a string) of a given state
                          # this can be useful for storing states in data structures like dictionaries or sets

    def get_goal_states(self):
        return self.goal_states # returns a list of goal states for the MDP
    
    def create_state_space(self):
        list_state_space = []
        # state[0] = fact1: The door is closed
        # state[1] = fact2: The door is open 
        # state[2] = fact3: The robot is holding the suitcase
        # state[3] = fact4: The robot is not holding the suitcase
        # state[4] = fact5: The suitcase is inside the room
        # state[5] = fact6: The suitcase is outside the room
        for fact1 in (True, False):
            for fact2 in (True, False):
                for fact3 in (True, False):
                    for fact4 in (True, False):
                        for fact5 in (True, False):
                            for fact6 in (True, False):
                                current_state = (fact1, fact2, fact3, fact4, fact5, fact6)
                                list_state_space.append(current_state)
        terminate_state = ("Terminate")
        list_state_space.append(terminate_state)
        self.state_space = list_state_space
        # print(self.state_space)

    def decode_state(self, state):
        string_state = []
        if (state[0] == True):
            string_state.append("The door is closed")
        if (state[1] == True):
            string_state.append("The door is open")
        if (state[2] == True):
            string_state.append("The robot is holding the suitcase")
        if (state[3] == True):
            string_state.append("The robot is not holding the suitcase")
        if (state[4] == True):
            string_state.append("The suitcase is inside the room")
        if (state[5] == True):
            string_state.append("The suitcase is outside the room")
        if (state == "Terminate"):
            string_state.append("Terminate")
        return string_state
    
    def read_rewards_excel(self, file_title):
        # read by default 1st sheet of an excel file
        df = pd.read_excel(file_title)
        df_slice = df.iloc[1, 89:119] # note: currently still read the first response only
        # print(df_slice)
        reward_list = df_slice.tolist()
        n_facts = len(mdp.get_init_state())
        n_actions = len(mdp.get_actions())
        rewards_matrix = [[0 for _ in range(n_actions)] for _ in range(n_facts)]
        idx = 0
        for i in range(n_facts):
            for j in range(n_actions):
                rewards_matrix[i][j] = int(reward_list[idx])
                idx = idx + 1
        self.rewards_matrix = rewards_matrix

    def read_rewards_excel_all_lines(self, file_title):
        # read by default 1st sheet of an excel file
        df = pd.read_excel(file_title)
        # print(df)
        row = len(df)
        rewards_matrix_all = []
        for id in range(1, row):
            if (pd.isna(df.iloc[id, 89]) == False): # check whether it is USAR robot case
                # print(i, df.iloc[id, 89:119].tolist())
                reward_list = df.iloc[id, 89:119].tolist()
                n_facts = len(mdp.get_init_state())
                n_actions = len(mdp.get_actions())
                rewards_matrix = [[0 for _ in range(n_actions)] for _ in range(n_facts)]
                idx = 0
                for i in range(n_facts):
                    for j in range(n_actions):
                        rewards_matrix[i][j] = int(reward_list[idx])
                        idx = idx + 1
                rewards_matrix_all.append(rewards_matrix)
            else:
                rewards_matrix_all.append("None")
        self.rewards_matrix_all = rewards_matrix_all

    def get_rewards_matrix(self):
        return self.rewards_matrix

    def get_rewards_matrix_all(self):
        return self.rewards_matrix_all
    
    def get_reward(self, state, action, rewards_matrix):
        # Define rewards for each state-action pair
        # rewards_matrix = mdp.get_rewards_matrix()
        rewards_matrix = rewards_matrix
        # print(state)
        # print(action)
        action_idx = int(action[3]) - 1 # get the index of the action, based on the fourth char, for example "act1" -> 1 - 1 = 0
        idx = 0
        sum_rewards = 0
        for fact in state:
            if (fact == True):
                # print(rewards_matrix[idx][action_idx])
                sum_rewards = sum_rewards + rewards_matrix[idx][action_idx]
            idx = idx + 1
        # print(sum_rewards)
        return sum_rewards

    def value_iteration(self, rewards_matrix, epsilon=0.001):
        # initialize V with 0
        V = {mdp.get_state_hash(s): 0 for s in mdp.get_state_space()}
        # print(mdp.discount)
        # # while True:
        # delta = 0
        # for s in mdp.get_state_space():
        #     s_hash = mdp.get_state_hash(s)
        #     v = V[s_hash]
        #     # for R(s, a)
        #     V[s_hash] = max([sum([mdp.get_transition_probability(s, a, s_prime) * (mdp.get_reward(s, a) + mdp.discount * V[mdp.get_state_hash(s_prime)]) for s_prime in mdp.get_state_space()]) for a in mdp.get_actions()])
        #     # for R(s, a, s')
        #     # V[s_hash] = max([mdp.discount * sum([mdp.get_transition_probability(s, a, s_prime) * (mdp.get_reward(s, a, s_prime) + V[mdp.get_state_hash(s_prime)]) for s_prime in mdp.get_state_space()]) for a in mdp.get_actions()])
        #     delta = max(delta, abs(v - V[s_hash]))
        #     #print(delta)
        #     print("s :", s)
        #     print("s_hash: ", s_hash)
        #     print("v: ", v)
        #     print("V[s_hash]: ", V[s_hash])
        #     # if delta < epsilon:
        #     #     break
        while True:
            delta = 0
            for s in mdp.get_state_space():
                s_hash = mdp.get_state_hash(s)
                v = V[s_hash]
                # for R(s, a)
                V[s_hash] = max([sum([mdp.get_transition_probability(s, a, s_prime) * (mdp.get_reward(s, a, rewards_matrix) + mdp.discount * V[mdp.get_state_hash(s_prime)]) for s_prime in mdp.get_state_space()]) for a in mdp.get_actions()])
                # for R(s, a, s')
                # V[s_hash] = max([mdp.discount * sum([mdp.get_transition_probability(s, a, s_prime) * (mdp.get_reward(s, a, s_prime) + V[mdp.get_state_hash(s_prime)]) for s_prime in mdp.get_state_space()]) for a in mdp.get_actions()])
                delta = max(delta, abs(v - V[s_hash]))
            # print(delta)
            if delta < epsilon:
                self.delta = delta
                break
        return V
    
    def get_policy(self, V, rewards_matrix):
        # pass
        # initialize P with None
        P = {mdp.get_state_hash(s): None for s in mdp.get_state_space()}
        for s in mdp.get_state_space():
            s_hash = mdp.get_state_hash(s)
            v = V[s_hash]
            # for R(s, a)
            # V[s_hash] = max([sum([mdp.get_transition_probability(s, a, s_prime) * (mdp.get_reward(s, a) + mdp.discount * V[mdp.get_state_hash(s_prime)]) for s_prime in mdp.get_state_space()]) for a in mdp.get_actions()])
            max_value = float('-inf')
            best_action = None
            for a in mdp.get_actions():
                value = sum([mdp.get_transition_probability(s, a, s_prime) * 
                            (mdp.get_reward(s, a, rewards_matrix) + mdp.discount * V[mdp.get_state_hash(s_prime)]) 
                            for s_prime in mdp.get_state_space()])
                if value >= max_value:
                    max_value = value
                    best_action = a
            V[s_hash] = max_value
            P[s_hash] = best_action
            delta = max(self.delta, abs(v - V[s_hash]))
        P['Terminate'] = None
        # self.P = P
        # print("delta: ", delta)
        # print("V: ", V)
        # print("P: ", P)
        return P

    def get_trajectory(self, init_state, P):
        # init_state = self.init_state
        # P = self.P
        trajectory = []
        state = init_state
        max_steps = 10
        t = 0
        while ((t < max_steps)):
            s_hash = mdp.get_state_hash(state)
            action = P[s_hash]
            trajectory.append((state, action))
            # To get the full trajectory, we need to know the next_state after execute the (state, action)
            next_state = mdp.get_next_state(state, action)
            if (next_state == "Terminate"):
                trajectory.append((next_state, "None"))
                break
            state = tuple(next_state)
            t = t + 1
        # print(trajectory)
        return trajectory
        
    def get_next_state(self, state, action):
        # intended to return the next_state, given (state, action) pair
        next_state = list(state)
        # Condition 1 - act1 "Open the door": 
        # fact1 "The door is closed" becomes False after the action
        # fact2 "The door is open" becomes True after the action
        # other facts stay the same
        if (action == "act1"):
            next_state[0] = False
            next_state[1] = True
        # ==========
        # # Condition 2 - act2 "Move to the room": 
        # # fact5 "The suitcase is inside the room" becomes True after the action
        # # fact6 "The suitcase is outside the room" becomes False after the action
        # # other facts stay the same
        # elif (action == "act2"):
        #     next_state[4] = True
        #     next_state[5] = False
        # ==========
        # Condition 2 - act2 "Move to the room":
        # If the robot is holding the suitcase (fact3 True, fact4 False):
            # fact5 "The suitcase is inside the room" becomes True after the action
            # fact6 "The suitcase is outside the room" becomes False after the action
        # If the robot is not holding the suitcase (fact3 False, fact4 True):
            # fact5 "The suitcase is inside the room" is False, and still False after the action
            # fact6 "The suitcase is outside the room" is True, and still True after the action
        # other facts stay the same
        elif ((action == "act2") and (state[2] == True) and (state[3] == False)):
            next_state[4] = True
            next_state[5] = False
        # elif ((action == "act2") and (state[2] == False) and (state[3] == True)):
        #     next_state[4] = False
        #     next_state[5] = True
        # Condition 3 - act3 "Pick up the suitcase": 
        # fact3 "The robot is holding the suitcase" becomes True after the action
        # fact4 "The robot is not holding the suitcase" becomes False after the action
        # other facts stay the same
        elif (action == "act3"):
            next_state[2] = True
            next_state[3] = False
        # Condition 4 - act4 "Dropoff the suitcase inside the room": 
        # fact3 "The robot is holding the suitcase" is True, then becomes False after the action
        # fact4 "The robot is not holding the suitcase" is False, then becomes True after the action
        # other facts stay the same
        elif (action == "act4"):
            next_state[2] = False
            next_state[3] = True
        # Condition 5 - act5 "Exit the task": 
        # enter to absorber state "Terminate" after the action
        elif (action == "act5"):
            next_state = "Terminate"
        return next_state

    def compare_trajectories(self, T1, T2):
        if (T1 == T2):
            print("SIMILAR")
        else:
            print("DIFFERENT")
    

if __name__ == "__main__":
    mdp = MDP_Scenario1()
    # Debugging purpose
    # state_space = mdp.get_state_space()
    # print("State space:\n", state_space)
    # print(len(mdp.get_state_space()))
    # actions = mdp.get_actions()
    # print("Actions:\n", actions)
    # print(len(mdp.get_actions()))
    # print("Init state: ", mdp.get_init_state())
    # print("Decode init state: ", mdp.decode_state(mdp.get_init_state()))
    # print("Goal states: ", mdp.get_goal_states())
    # print("Decode goal states: ", mdp.decode_state(mdp.get_goal_states()[0]))
    # state = mdp.get_init_state()
    # next_state = mdp.get_goal_states()[0]
    # action = "act1"
    # print("Action taken: ", mdp.decode_actions(action))
    # print("Probability: ", mdp.get_transition_probability(state, action, next_state))

    '''
    # Read rewards matrix given by participant - specific line
    file_title = 'Goals vs Rewards Survey 3.0 - Specify Objective - Prolific_December 4, 2024_18.25.xlsx'
    mdp.read_rewards_excel(file_title)
    rewards_matrix = mdp.get_rewards_matrix()
    print("\nRewards matrix given by participant:")
    for row in rewards_matrix:
            print(row)
    # print(mdp.get_reward(state, action))

    # Check the transition probability
    # print("\nList of (s,a,s_prime) that has probability equal 1:")
    # n = 0
    # for a in mdp.get_actions():
    #     for s in mdp.get_state_space():
    #         for s_prime in mdp.get_state_space():
    #             if mdp.get_transition_probability(s, a, s_prime) == 1 :
    #                 n = n + 1
    #                 print("#", n)
    #                 print("s: ", mdp.decode_state(s))
    #                 print("a: ", mdp.decode_actions(a))
    #                 print("s_prime: ", mdp.decode_state(s_prime))

    # Call value iteration
    V = mdp.value_iteration(rewards_matrix)
    # print("\nValue iteration calculation result:")
    # print(V)

    # Call get_policy
    P = mdp.get_policy(V, rewards_matrix)
    # print("\nThe policy from user-defined matrix:")
    # print(P)

    # Call get_trajectory
    init_state = mdp.get_init_state()
    T = mdp.get_trajectory(init_state, P)
    # print(T)
    print("The trajectory (state-action pairs) from user-defined matrix:")
    T_length = len(T)
    for i in range(T_length):
        state = T[i][0]
        action = T[i][1]
        print(i+1, mdp.decode_state(state), " -> ", mdp.decode_actions(action))

    # Compare the trajectories
    T_video = [((True, False, False, True, False, True), 'act3'), ((True, False, True, False, False, True), 'act1'), ((False, True, True, False, False, True), 'act2'), ((False, True, True, False, True, False), 'act4'), ((False, True, False, True, True, False), 'act5'), ('Terminate', 'None')]
    mdp.compare_trajectories(T, T_video)
    '''

    # Read rewards matrix given by participant - all lines
    file_title = 'Goals vs Rewards Survey 3.0 - Specify Objective - Prolific_December 4, 2024_18.25.xlsx'
    mdp.read_rewards_excel_all_lines(file_title)
    rewards_matrix_all = mdp.get_rewards_matrix_all()
    idx = 0
    for rewards in rewards_matrix_all:
        idx = idx + 1
        if (rewards != "None"):
            print("\nResponse line",idx)
            print("Rewards matrix given by participant:")
            for row in rewards:
                    print(row)

            # Call value iteration
            V = mdp.value_iteration(rewards)

            # Call get_policy
            P = mdp.get_policy(V, rewards)

            # Call get_trajectory
            init_state = mdp.get_init_state()
            T = mdp.get_trajectory(init_state, P)
            # print(T)
            print("The trajectory (state-action pairs) from user-defined matrix:")
            T_length = len(T)
            for i in range(T_length):
                state = T[i][0]
                action = T[i][1]
                print(i+1, mdp.decode_state(state), " -> ", mdp.decode_actions(action))

            # Compare the trajectories
            T_video = [((True, False, False, True, False, True), 'act3'), ((True, False, True, False, False, True), 'act1'), ((False, True, True, False, False, True), 'act2'), ((False, True, True, False, True, False), 'act4'), ((False, True, False, True, True, False), 'act5'), ('Terminate', 'None')]
            mdp.compare_trajectories(T, T_video)
    # raise SystemExit(0)
    # '''