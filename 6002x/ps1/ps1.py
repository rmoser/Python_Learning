###########################
# 6.00.2x Problem Set 1: Space Cows 

from ps1_partition import get_partitions
import time
import timeit
from statistics import mean, stdev

#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """

    cow_dict = dict()

    f = open(filename, 'r')
    
    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])
    return cow_dict


# Problem 1
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    # Reformat cows into dict by weight
    _cows = dict()
    for name, weight in cows.items():
        if weight not in _cows:
            _cows[weight] = []
        _cows[weight].append(name)

    # Init loop variables
    loads = []
    load = []
    weight = 0

    while _cows:  # Ends when all cows have been allocated to a load
        while _cows and min(_cows.keys()) <= limit - weight:
            for i in sorted(_cows.keys(), reverse=True):

                # Add the heaviest cow that will fit to the load and recalculate available space
                if weight + i <= limit:
                    cow = _cows[i].pop()
                    load.append(cow)
                    weight += i
                    if not _cows[i]:
                        _cows.pop(i)  # Remove empty lists so we know there are no more cows with this weight
                    break

        # We should have a "full" load now
        loads.append(load)
        weight = 0
        load = []

    return loads


# Problem 2
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    valid = []
    for loads in get_partitions(cows):
        _weight = [sum(cows[x] for x in load) for load in loads]
        # print(f"w: {_weight}")
        if max(_weight) <= limit:
            # print(f"valid: {valid}")
            # print(f"loads: {loads}")
            # print(f"{len(loads)} < {len(valid)}: {len(loads) < len(valid)}")
            if not valid or len(loads) < len(valid):
                valid = loads
                # print(f"Saved valid: {valid}")

    return valid

        
# Problem 3
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows("ps1_cow_data.txt")
    limit = 10
    loops = 10

    times_greedy = []
    for i in range(loops):
        start = time.time()
        greedy_cow_transport(cows, limit)
        end = time.time()
        times_greedy.append(end - start)

    times_brute = []
    for i in range(loops):
        start = time.time()
        brute_force_cow_transport(cows, limit)
        end = time.time()
        times_brute.append(end - start)

    print(f"Greedy: m {mean(times_greedy)} / s {stdev(times_greedy)}")
    print(f"Brute : m {mean(times_brute)} / s {stdev(times_brute)}")


"""
Here is some test data for you to see the results of your algorithms with. 
Do not submit this along with any of your answers. Uncomment the last two
lines to print the result of your problem.
"""

cows = load_cows("ps1_cow_data.txt")
limit=100
print(cows)

# print(greedy_cow_transport(cows, limit))
# print(brute_force_cow_transport(cows, 10))

# print(greedy_cow_transport({'Patches': 60, 'Polaris': 20, 'Muscles': 65, 'Louis': 45, 'Clover': 5, 'MooMoo': 85, 'Lotus': 10, 'Milkshake': 75, 'Miss Bella': 15, 'Horns': 50}, 100))
# print(greedy_cow_transport({'Patches': 60, 'Polaris': 20, 'Muscles': 65, 'Louis': 45, 'Clover': 5, 'MooMoo': 85, 'Lotus': 10, 'Milkshake': 75, 'Miss Bella': 15, 'Horns': 50}, 100))

# print(brute_force_cow_transport({'Boo': 20, 'Horns': 25, 'MooMoo': 50, 'Miss Bella': 25, 'Milkshake': 40, 'Lotus': 40}, 100))
# print(brute_force_cow_transport({'Buttercup': 11, 'Betsy': 39, 'Starlight': 54, 'Luna': 41}, 145))

compare_cow_transport_algorithms()
