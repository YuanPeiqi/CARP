import numpy as np
import sys
import copy

# distance[u][v] indicates the minimum distance from u to v
distance = []
# weight[(u,v)] indicates the cost of edge (u,v)
weight = {}
# demand[(u,v)] indicates the demand of task (u,v)
demand = {}
# result set for routes chosen
opt_route = []
# cost set for routes chosen
opt_cost = []
# load set for routes chosen
opt_load = []


def Floyd(size):
    for k in range(1, size):
        for i in range(1, size):
            for j in range(1, size):
                if distance[i][k] + distance[k][j] < distance[i][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]


def better(task, next_task, rule_num, current_load):
    if next_task is None:
        return True
    # maximize the distance from the task to the depot
    if rule_num == 1:
        return distance[task[1]][1] > distance[next_task[1]][1]
    # minimize the distance from the task to the depot
    elif rule_num == 2:
        return distance[task[1]][1] < distance[next_task[1]][1]
    # maximize the term dem(t)/sc(t), where dem(t) and sc(t) are demand and serving cost of task t, respectively
    elif rule_num == 3:
        return demand[task] / weight[task] > demand[next_task] / weight[next_task]
    # minimize the term dem(t)/sc(t), where dem(t) and sc(t) are demand and serving cost of task t, respectively
    elif rule_num == 4:
        return demand[task] / weight[task] < demand[next_task] / weight[next_task]
    else:
        if current_load <= int(0.5 * information['CAPACITY']):
            return distance[task[1]][1] > distance[next_task[1]][1]
        else:
            return distance[task[1]][1] < distance[next_task[1]][1]


def path_scanning(rule_num):
    capacity = information['CAPACITY']
    uncompleted = [item for item in demand.keys()]
    cost_set = []
    route_set = []
    while uncompleted:
        route = []
        load, cost = 0, 0
        src = information['DEPOT']
        next_distance = 0
        while uncompleted and next_distance != float('Inf'):
            next_distance = float('Inf')
            next_task = None
            for task in uncompleted:
                if demand[task] + load <= capacity:
                    if distance[src][task[0]] < next_distance:
                        next_distance = distance[src][task[0]]
                        next_task = task
                    elif distance[src][task[0]] == next_distance and better(task, next_task, rule_num, load):
                        next_task = task
            if next_task is not None:
                route.append(next_task)
                uncompleted.remove(next_task)
                uncompleted.remove((next_task[1], next_task[0]))
                load += demand[next_task]
                cost += next_distance + weight[next_task]
                src = next_task[1]
        cost += distance[src][1]
        cost_set.append(cost)
        opt_load.append(load)
        route_set.append(route)
    total_cost = 0
    for i in cost_set:
        total_cost += i
    return cost_set, route_set, total_cost


def format_print():
    cost = 0
    print('s ', end='')
    for i in range(len(opt_route)):
        cost += opt_cost[i]
        print('0,' + str(opt_route[i]).replace('[', '').replace(']', '').replace(' ', '') + ',0', end='')
        if i != len(opt_route) - 1:
            print(',', end='')
        # print('Route_' + str(i) + ': ' + str(route_set[i]))
        # print('Cost_' + str(i) + ': ' + str(cost_set[i]))
    print('\nq ' + str(cost))


'''Single Insertion: In the single insertion move, a task is removed from its current position and re-inserted into 
another position of the current solution or a new empty route. If the selected task belongs to an edge task, both its 
directions will be considered when inserting the task into the “target position.” The direction leading to a better 
solution will be chosen.'''


def single_insertion():
    delta_cost = 0
    # Record task that need to be changed
    candidate_task = None
    # Record the route containing the task
    candidate_route = None
    # Whether the current task is flipped
    reverse_flag = False
    # Record the position to insert
    expected_position = None
    # Cost change caused by removing
    remove_cost = None
    # Cost change caused by insertion
    insertion_cost = None

    for route in opt_route:
        for task in route:
            # Deep copy the current route
            route_copy = copy.deepcopy(route)
            # Add depot to both ends as the src point and des point and remove selected task, which is convenient for calculation
            route_copy.append((1, 1))
            route_copy.insert(0, (1, 1))
            idx = route_copy.index(task)
            route_copy.remove(task)
            current_remove_cost = (opt_route.index(route), distance[route_copy[idx - 1][1]][route_copy[idx][0]] - \
                                    distance[route_copy[idx - 1][1]][task[0]] - distance[task[1]][route_copy[idx][0]])
            # Insertion of the same route
            for i in range(1, len(route_copy)):
                # Difference caused by removing the current task and insertion
                current_delta_cost = current_remove_cost[1] + distance[route_copy[i - 1][1]][task[0]] + \
                                     distance[task[1]][route_copy[i][0]] - \
                                     distance[route_copy[i - 1][1]][route_copy[i][0]]
                # Insertion of the reverse of the task
                reverse_current_delta_cost = current_remove_cost[1] + distance[route_copy[i - 1][1]][task[1]] + \
                                             distance[task[0]][route_copy[i][0]] - \
                                             distance[route_copy[i - 1][1]][route_copy[i][0]]
                if current_delta_cost < delta_cost:
                    delta_cost = current_delta_cost
                    remove_cost = current_remove_cost
                    insertion_cost = (opt_route.index(route), distance[route_copy[i - 1][1]][task[0]] + \
                                        distance[task[1]][route_copy[i][0]] - distance[route_copy[i - 1][1]][route_copy[i][0]])
                    candidate_task = task
                    candidate_route = route
                    expected_position = (opt_route.index(route), i - 1)
                    reverse_flag = False
                if reverse_current_delta_cost < delta_cost:
                    delta_cost = reverse_current_delta_cost
                    remove_cost = current_remove_cost
                    insertion_cost = (opt_route.index(route), distance[route_copy[i - 1][1]][task[1]] + \
                                        distance[task[0]][route_copy[i][0]] - distance[route_copy[i - 1][1]][route_copy[i][0]])
                    candidate_task = task
                    candidate_route = route
                    expected_position = (opt_route.index(route), i - 1)
                    reverse_flag = True

            # Insertion of different route
            for i in range(len(opt_route)):
                # If another route is not the current route and the load does not exceeds capacity, then continue
                if opt_route[i] != route and opt_load[i] + demand[task] <= information['CAPACITY']:
                    another_route_copy = copy.deepcopy(opt_route[i])
                    another_route_copy.append((1, 1))
                    another_route_copy.insert(0, (1, 1))
                    for j in range(1, len(another_route_copy)):
                        current_delta_cost = current_remove_cost[1] + distance[another_route_copy[j - 1][1]][task[0]] + \
                                             distance[task[1]][another_route_copy[j][0]] - \
                                             distance[another_route_copy[j - 1][1]][another_route_copy[j][0]]
                        reverse_current_delta_cost = current_remove_cost[1] + distance[another_route_copy[j - 1][1]][task[1]] + \
                                                     distance[task[0]][another_route_copy[j][0]] - \
                                                     distance[another_route_copy[j - 1][1]][another_route_copy[j][0]]
                        if current_delta_cost < delta_cost:
                            delta_cost = current_delta_cost
                            remove_cost = current_remove_cost
                            insertion_cost = (i, distance[another_route_copy[j - 1][1]][task[0]] + \
                                                    distance[task[1]][another_route_copy[j][0]] - \
                                                    distance[another_route_copy[j - 1][1]][another_route_copy[j][0]])
                            candidate_task = task
                            candidate_route = route
                            expected_position = (i, j - 1)
                            reverse_flag = False
                        if reverse_current_delta_cost < delta_cost:
                            delta_cost = reverse_current_delta_cost
                            remove_cost = current_remove_cost
                            insertion_cost = (i, distance[another_route_copy[j - 1][1]][task[1]] + \
                                                    distance[task[0]][another_route_copy[j][0]] - \
                                                    distance[another_route_copy[j - 1][1]][another_route_copy[j][0]])
                            candidate_task = task
                            candidate_route = route
                            expected_position = (i, j - 1)
                            reverse_flag = True
    if candidate_task:
        candidate_route.remove(candidate_task)
        opt_cost[remove_cost[0]] += remove_cost[1]
        opt_cost[insertion_cost[0]] += insertion_cost[1]
        opt_load[remove_cost[0]] -= demand[candidate_task]
        opt_load[insertion_cost[0]] += demand[candidate_task]
        if reverse_flag:
            opt_route[expected_position[0]].insert(expected_position[1], (candidate_task[1], candidate_task[0]))
        else:
            opt_route[expected_position[0]].insert(expected_position[1], candidate_task)


if __name__ == '__main__':
    # Receive the arguments and read the file
    file_path = sys.argv[1]
    termination = sys.argv[3]
    seed = sys.argv[5]
    instance_file = open(file_path, mode='r', newline='')
    content = instance_file.readlines()
    instance_file.close()

    # Store the information of graph given by the file
    information = {content[i].replace('\n', '').split(' : ')[0]: int(content[i].replace('\n', '').split(' : ')[1]) for i
                   in range(1, 8)}

    # Get the graph data
    graph_size = information['VERTICES'] + 1
    distance = [[float('Inf') if i != j else 0 for j in range(graph_size)] for i in range(graph_size)]
    for i in range(9, len(content) - 1):
        u, v, c, d = list(map(int, content[i].replace('\n', '').split()))
        if d:
            demand[(u, v)] = d
            demand[(v, u)] = d
        weight[(u, v)] = c
        weight[(v, u)] = c
        distance[u][v] = c
        distance[v][u] = c

    # Run Floyd's algorithm to find minimum distances of each vertices pair
    Floyd(graph_size)
    final_cost = float('Inf')
    for rule in range(1, 6):
        current_cost, current_route, current_total_cost = path_scanning(rule)
        if current_total_cost < final_cost:
            final_cost = current_total_cost
            opt_cost = current_cost
            opt_route = current_route
    for _ in range(1000):
        single_insertion()
    format_print()
