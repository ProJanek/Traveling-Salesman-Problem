import numpy as np
import math
import matplotlib.collections as mc
import matplotlib.pylab as pl

def gen_lines(cities, itinerary):
    """Create a list of start and end points of the itinerary lines."""
    lines = []
    for j in range(len(itinerary)-1):
        lines.append([cities[itinerary[j]], cities[itinerary[j+1]]])
    return lines

def calculate_distance(lines):
    """Calculate the total distance of itinerary."""
    distance = 0
    for j in range(len(lines)):
        distance += math.sqrt((lines[j][1][0] - lines[j][0][0])**2 
                              + (lines[j][1][1] - lines[j][0][1])**2)
    return distance

def plot_itinerary(cities,itin,plottitle,file_name,distance):
    """Save the itinerary graph with information."""
    lc = mc.LineCollection(gen_lines(cities,itin), linewidths=2)
    x_list = list(zip(*cities))[0]
    y_list = list(zip(*cities))[1]
    fig, ax = pl.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    ax.plot(cities[itin[0]][0], cities[itin[0]][1], "or")
    ax.text(cities[itin[0]][0] - 0.04, cities[itin[0]][1] + 0.02, "START")
    ax.plot(cities[itin[-1]][0], cities[itin[-1]][1], "or")
    ax.text(cities[itin[-1]][0] - 0.03, cities[itin[-1]][1] + 0.02, "END")
    for i in range(len(cities)):
        ax.text(cities[i][0], cities[i][1] - 0.05, i)
    ax.text(0.75, 0, f"DISTANCE: {round(distance,2)}")
    pl.scatter(x_list, y_list)
    pl.title(plottitle)
    pl.xlabel('X Coordinate')
    pl.ylabel('Y Coordinate')
    pl.savefig(str(file_name) + '.png')
    pl.close()

def find_nearest(cities, idx, nnitinerary):
    """
    Find the nearest city based on the current position (idx) 
    and return its index.
    """
    point = cities[idx]
    mindist = float("inf")
    minidx = -1
    for j in range(0, len(cities)):
        dist = math.sqrt((point[0] - cities[j][0])**2 + (point[1] - cities[j][1])**2)
        if dist < mindist and dist > 0 and j not in nnitinerary:
            mindist = dist
            minidx = j
    return (minidx)     

def nearest_neigbor_search(cities, N):
    """Find the itinerary using the nearest neighbor method."""
    nnitinerary = [0]
    for j in range(N-1):
        nearest = find_nearest(cities, nnitinerary[-1], nnitinerary)
        nnitinerary.append(nearest)
    return nnitinerary

def perturb_search(cities, itinerary):
    """Find the itinerary using the perturb search  method"""
    neighborsid1 = math.floor(np.random.rand()*len(itinerary))
    neighborsid2 = math.floor(np.random.rand()*len(itinerary))

    if neighborsid1 != 0 and neighborsid2 !=0:
        itinerary_copy = itinerary.copy()

        itinerary_copy[neighborsid1] = itinerary[neighborsid2]
        itinerary_copy[neighborsid2] = itinerary[neighborsid1]

        distance1 = calculate_distance(gen_lines(cities,itinerary))
        distance2 = calculate_distance(gen_lines(cities,itinerary_copy))

        itinerarytoreturn = itinerary.copy()

        if distance2 < distance1:
            itinerarytoreturn = itinerary_copy.copy()
    else: 
        itinerarytoreturn = itinerary.copy()

    return(itinerarytoreturn.copy())

def simulated_annealing_v1(cities, itinerary, time):
    """
    Find a itinerary using the perturb search method 
    and the temperature function, which will allow to choose
    worse itinerary on the beginning - the goal is to find 
    the global maximum rather than the local maximum.
    The time argument measures how far we are through the process. 
    """
    neighborsid1 = math.floor(np.random.rand()*len(itinerary))
    neighborsid2 = math.floor(np.random.rand()*len(itinerary))

    if neighborsid1 != 0 and neighborsid2 !=0:
        itinerary_copy = itinerary.copy()

        itinerary_copy[neighborsid1] = itinerary[neighborsid2]
        itinerary_copy[neighborsid2] = itinerary[neighborsid1]

        distance1 = calculate_distance(gen_lines(cities,itinerary))
        distance2 = calculate_distance(gen_lines(cities,itinerary_copy))

        randomdraw = np.random.rand()
        temperature = 1/((time/1000)+1) # temperature function
        itinerarytoreturn = itinerary.copy()

        # if statement allowing to choose the worse itinerary at the beginning
        if (distance2 > distance1 and randomdraw < temperature) or distance1 > distance2:
            itinerarytoreturn = itinerary_copy.copy()
    else: 
        itinerarytoreturn = itinerary.copy()

    return(itinerarytoreturn.copy())

def simulated_annealing_v2(cities, itinerary, time):
    """
    Find a itinerary using the perturbation search method 
    with the temperature function, random selection of
    different perturbing methods and a condition to avoid 
    major setbacks.
    The time argument measures how far we are through the process.
    """
    neighborsid1 = math.floor(np.random.rand()*len(itinerary))
    neighborsid2 = math.floor(np.random.rand()*len(itinerary))

    if neighborsid1 != 0 and neighborsid2 !=0:
        itinerary_copy = itinerary.copy()

        randomdraw1 = np.random.rand()
        small = min(neighborsid1, neighborsid2)
        big  = max(neighborsid1, neighborsid2)

        if randomdraw1 >= 0.55:
            itinerary_copy[small:big] = itinerary_copy[small:big][::-1]
        elif randomdraw1 < 0.45:
            tempitin = itinerary_copy[small:big]
            del(itinerary_copy[small:big])
            neighborsid3 = math.floor(np.random.rand()*(len(itinerary_copy)-1)+1)
            for j in range(len(tempitin)):
                itinerary_copy.insert(neighborsid3 + j, tempitin[j])
        else:
            itinerary_copy[neighborsid1] = itinerary[neighborsid2]
            itinerary_copy[neighborsid2] = itinerary[neighborsid1]

        distance1 = calculate_distance(gen_lines(cities,itinerary))
        distance2 = calculate_distance(gen_lines(cities,itinerary_copy))

        randomdraw2 = np.random.rand()
        temperature = 1/((time/1000)+1) # temperature function
        itinerarytoreturn = itinerary.copy()

        scale = 3.5
        # if statement allowing to choose the worse (but not really bad) itinerary at the beginning
        if (distance2 > distance1 and randomdraw2 < (math.exp(scale*(distance1 - distance2))*temperature)) or distance1 > distance2:
            itinerarytoreturn = itinerary_copy.copy()
    else:
        itinerarytoreturn = itinerary.copy()

    return(itinerarytoreturn)

def simulated_annealing_v3(cities, itinerary, time, maxitin):
    """
    Find a itinerary using the perturbation search method 
    with the temperature function, random selection of
    different perturbing methods, condition to avoid major 
    setbacks and ability to reset the itinerary to the previous best.
    The time argument measures how far we are through the process.
    The maxitin argument tells how many perturbations will be done in total.
    """
    neighborsid1 = math.floor(np.random.rand()*len(itinerary))
    neighborsid2 = math.floor(np.random.rand()*len(itinerary))

    global mindistance # minimum distance achieved so far
    global minitinerary # itinerary of the minimum distance
    global minidx # time at which it was achieved

    if neighborsid1 != 0 and neighborsid2 !=0:
        itinerary_copy = itinerary.copy()

        randomdraw1 = np.random.rand()
        small = min(neighborsid1, neighborsid2)
        big  = max(neighborsid1, neighborsid2)

        if randomdraw1 >= 0.55:
            itinerary_copy[small:big] = itinerary_copy[small:big][::-1]
        elif randomdraw1 < 0.45:
            tempitin = itinerary_copy[small:big]
            del(itinerary_copy[small:big])
            neighborsid3 = math.floor(np.random.rand()*(len(itinerary_copy)-1)+1)
            for j in range(len(tempitin)):
                itinerary_copy.insert(neighborsid3 + j, tempitin[j])
        else:
            itinerary_copy[neighborsid1] = itinerary[neighborsid2]
            itinerary_copy[neighborsid2] = itinerary[neighborsid1]

        distance1 = calculate_distance(gen_lines(cities,itinerary))
        distance2 = calculate_distance(gen_lines(cities,itinerary_copy))

        randomdraw2 = np.random.rand() 
        temperature = 1/((time/1000)+1) # temperature function
        itinerarytoreturn = itinerary.copy()

        scale = 3.5
        # if statement allowing to choose the worse (but not really bad) itinerary at the beginning
        if (distance2 > distance1 and randomdraw2 < (math.exp(scale*(distance1 - distance2))*temperature)) or distance1 > distance2:
            itinerarytoreturn = itinerary_copy.copy()

        reset = True
        resetthresh = 0.04 # variable determining the time to wait before resetting
        # reset only if there is many perturbations without finding an improvement 
        if(reset and (time - minidx) > (maxitin * resetthresh)):
            itinerarytoreturn = minitinerary
            minidx = time

        if(calculate_distance(gen_lines(cities,itinerarytoreturn)) < mindistance):
            mindistance = calculate_distance(gen_lines(cities,itinerary_copy))
            minitinerary = itinerarytoreturn
            minidx = time

        if(abs(time - maxitin) <= 1):
            itinerarytoreturn = minitinerary.copy()

    else:
        itinerarytoreturn = itinerary.copy()

    return(itinerarytoreturn)

random_seed = 1729
np.random.seed(random_seed)

# Randomly generate map of N cities
N = 40
x = np.random.rand(N)
y = np.random.rand(N)

points = zip(x,y)
cities = list(points)

# Random itinerary
itinerary = list(range(N))
dist = calculate_distance(gen_lines(cities, itinerary)) 
plot_itinerary(cities,itinerary,'TSP - Random Itinerary','figure1',dist)

# Nearest neighbor method
itinerary_nn = nearest_neigbor_search(cities,N)
dist = calculate_distance(gen_lines(cities, itinerary_nn))  
plot_itinerary(cities,nearest_neigbor_search(cities,N),'TSP - Nearest Neighbor','figure2',dist)

# Upgrade nearest neighbor metod with perturb method
itinerary_ps = itinerary_nn
for n in range(0,len(itinerary) * 10000):
    itinerary_ps = perturb_search(cities,itinerary_ps)
dist = calculate_distance(gen_lines(cities,itinerary_ps)) # perturb search
plot_itinerary(cities,itinerary_ps,'TSP - Nearest Neighbor & Perturb Search','figure3',dist)

# Simulated annealing (perturb search method with the temperature function)
itinerary_sa = itinerary.copy()
for n in range(0,len(itinerary) * 20000):
    itinerary_sa = simulated_annealing_v1(cities,itinerary_sa,n)
dist = calculate_distance(gen_lines(cities, itinerary_sa))
plot_itinerary(cities,itinerary_sa,'TSP - Simulated Annealing v1','figure4',dist)

# Modified simulated annealing (different perturbing methods & avoid major setbacks)
itinerary_sa2 = itinerary.copy()
for n in range(0,len(itinerary) * 20000):
    itinerary_sa2 = simulated_annealing_v2(cities,itinerary_sa2,n)
dist = calculate_distance(gen_lines(cities, itinerary_sa2))
plot_itinerary(cities,itinerary_sa2,'TSP - Simulated Annealing v2','figure5', dist)

# Modified simulated annealing (ability to reset the itinerary to the previous best)
itinerary_sa3 = itinerary.copy()
mindistance = calculate_distance(gen_lines(cities,itinerary))
minitinerary = itinerary
minidx = 0
maxitin = len(itinerary) * 20000
for n in range(0,maxitin):
    itinerary_sa3 = simulated_annealing_v3(cities,itinerary_sa3,n, maxitin)
dist = calculate_distance(gen_lines(cities,itinerary_sa3))
plot_itinerary(cities,itinerary_sa3,'TSP - Simulated Annealing v3','figure6',dist)