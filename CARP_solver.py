import numpy as np
import sys

# distance[u][v] indicates the minimum distance from u to v
distance = []
# weight[(u,v)] indicates the cost of edge (u,v)
weight = {}
# demand[(u,v)] indicates the demand of task (u,v)
demand = {}
# result set for routes chosen
route_set = []
# cost set for routes chosen
cost_set = []


def Floyd(size):
    for k in range(1, size):
        for i in range(1, size):
            for j in range(1, size):
                if distance[i][k] + distance[k][j] < distance[i][j]:
                    distance[i][j] = distance[i][k] + distance[k][j]


def path_scanning():
    capacity = information['CAPACITY']
    uncompleted = [item for item in demand.keys()]
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
                    elif distance[src][task[0]] == next_distance:
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
        route_set.append(route)


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
    path_scanning()
    total_cost = 0
    print('s ', end='')
    for i in range(len(route_set)):
        total_cost += cost_set[i]
        print('0,' + str(route_set[i]).replace('[', '').replace(']', '').replace(' ', '') + ',0', end='')
        if i != len(route_set) - 1:
            print(',', end='')
        # print('Route_' + str(i) + ': ' + str(route_set[i]))
        # print('Cost_' + str(i) + ': ' + str(cost_set[i]))
    print('\nq ' + str(total_cost))
