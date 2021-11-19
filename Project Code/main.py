# Abraham Meza, Harrison Hong, Alexander Mathew #
# CPE 400.1001 - Semester Project - (6) Dynamic Faulty Network #
# May 5, 2021 #

# Header/Library File(s) #

# Default Library: libraries integrated in Pip3 #
from itertools import combinations, groupby
import string
import random
import sys
import time
import math
import queue

# Required Library: libraries that need to be manually installed #

import networkx as nx # Network Library : allows for simulated network using node data structure
import matplotlib.pyplot as plt # Graphical Library: allows for creating static, animated, and interactive visualizations (MATLAB Plotting)
import matplotlib.animation as ani # Graphical Library: allows for creating static, animated, and interactive visualizations (Live Animation)

# Global Variable: dictates # of network nodes, # of network faults, and sourceNode #

globalNode = 26 # recommended value between 10 and 26 (A-Z): able to do more nodes, but mapping labels will change from ASCII Uppercase to Uppercase w/ numbers (hard to track): able to do less nodes, but cannot exceed # of faults then # of nodes as it will erase entire network (caution)
globalFault = 3
sourceNode = 'A'

# Global Queue: utilized to record node attributes (i.e., node name, node edges, node weight, etc.) for manual manipulation : node recovery #

queueNode = queue.Queue() # node queue

weights = [] # array declaration/initialization: weight
failedNodes = [] # array declaration/initialization: failedNodes

# Function Protoypes/Defintions

def randomNetwork(nodes, prob): # generates a random undirected graph (Erdős-Rényi); however, assigns at least one random edge for each node as means to create a connected network

    Network = nx.MultiGraph() # MultiGraph(): create an empty graph with no nodes and no edges

    edges = combinations(range(nodes), 2) # combination of edges per node (combo between two nodes): want to set at least one edge for every node

    for i in range(nodes): # for loop: insert # multiple nodes based on globalNode value ()
        Network.add_node(i, pos = (random.randint(1, nodes * 10), random.randint(1, nodes * 10))) # add_node(): insert one node at a time based on i iteration; assign random node position (1 - (node * 10): made it node * 10 to ensure no overlapping nodes (readability))
    
    # Network.add_nodes_from(range(nodes)) # add_nodes_from(): add multiple nodes (iterable): 0 - (globaNode - 1) = globalNode number of nodes

    if prob <= 0: # if node probability is less than 0 (0%), then return empty network (nothing more to be done)
        return Network
    if prob >= 1: # if node probability is greater than 1 (%100), then return completed network using empty network (nothing more to be done)
        return nx.complete_graph(nodes, create_using = Network)

    for _, node_edges in groupby(edges, key = lambda x: x[0]): # node pairing (edges)
        node_edges = list(node_edges) # list of possible edge combinations

        random_edge = random.choice(node_edges) # choose a random edge from list of possible edge combinations

        Network.add_edge(*random_edge, weight = (random.randint(1,10))) # add_edge(): add random edge combination to the graph

        for e in node_edges: 
            if random.random() < prob:
                Network.add_edge(*e, weight = (random.randint(1,10)))

    # After nodes and edges have been finalized, relabel nodes to reflect alphabetical symbols instead of numbers (ints)

    mapping = dict(zip(Network, string.ascii_uppercase)) # assign mapping to specified dictionary: ascii_uppercase (A - Z)

    Network = nx.relabel_nodes(Network, mapping) # relabel_nodes(): relabel nodes in a given node map based on given dictionary

    if sourceNode not in list(Network.nodes): # if statement (error handling): if source node is not in the original network router list, then mesh network cannot exist (exit program w/ error message)
        print("\nSource Node ['" + str(sourceNode) + "'] is not inside the Mesh Network. Simulation is offline. Please try again or reassign sourceNode value.\n") # print error message (Invalid Simulation)
        sys.exit() # exit program (sys library)

    return Network # return Network Node Map

def faultyNetwork(nodes): # generates a random sample of faulty nodes and removes nodes from the network. Automatically deletes and deallocates edges from deleted nodes. Returns modified network for future display.
    network_nodes = list(Network.nodes) # records the list of current nodes in the network
    network_edges = list(Network.edges(data = False)) # records the list of current edges w/ edge data (i.e., weights, etc.) in the network

    sampleNodes = (random.randint(1, math.floor(nodes / 4))) # generates a random sample integer for potentially faulty nodes (don't want to delete more than a fourth of the nodes initially (nodes / 4)); code automatically rounds down to the nearest integer if randVal is a float (/ 4) as you cannot have part of a network (safer to round down)
    sampleEdges = (random.randint(1, math.floor(Network.number_of_nodes() / 4))) # generates a random sample integer for potentially faulty edges (don't want to delete more than a fourth of the edges initially (edges / 4)): code automatically rounds down to the nearest integer if randVal is a float (/ 4) as you cannot have part of an edge (safer to round down)

    faultyNodes = random.sample(network_nodes, sampleNodes) # chooses sample based on # number of faulty nodes, and randomly chooses nodes to delete from the network
    faultyEdges = random.sample(network_edges, sampleEdges) # chooses sample based on # number of faulty edges, and randomly chooses edges to delete from the network

    if sourceNode in faultyNodes: # if statement: if source node fails, then entire network is offline (exit program to simulate shutdown); however, if path fails, do nothing because the network still exists if sourceNode is active
        print("\nSource Node ['" + str(sourceNode) + "'] has unexpectedly shutdown. Mesh Network is offline. We apologize for the inconvenience.\n") # print error message (Mesh Network Offline)
        sys.exit() # exit program (sys library)

    print("\nThere has been a fault in node(s): " + str(faultyNodes) + "! Removing faulty networks immediately!\n") # alert message: indicates which faulty nodes are being removed from the network
    print("\nThere has been a fault in edge(s): " + str(faultyEdges) + "! Removing faulty edges immediately!\n") # alert message: indicates which faulty nodes are being removed from the network

    Network.remove_nodes_from(faultyNodes) # removes faultyNodes from the network
    Network.remove_edges_from(faultyEdges) # removes faultyEdges from the network

    queueNode.put(faultyNodes) # insert list of removed faulty nodes into node queue

    return Network # update network structure

def displayNetwork(): # generates an image of the current state of the network w/ node and edge labeling (formatting)
    # Statistical Print Statements #

    print("\n/////////////////////////////////\n" # Label Design
        "/////  Network Information  /////\n"
        "/////////////////////////////////\n")

    # Node Statistics #

    print("Number of nodes: " + str(Network.number_of_nodes()) + "\n") # prints total number of nodes in the network
    print("Online Network Nodes: " + str(list(Network.nodes)) + "\n\n") # prints current nodes in the network

    # Edge Statistics #
    
    weights.append(str(Network.edges(data = True)))
    print("Number of edges: " + str(Network.number_of_edges()) + "\n") # prints total number of edges in the network
    print("Current Edge Pairings: " + str(Network.edges(data = True)) + "\n") # prints current edge pairings w/ corresponding edge data (i.e., weights, etc.) in the network

    print("/////////////////////////////////////////////////////\n" # Label Design
        "/////  Dijkstra's Algorithm w/ Online Networks  /////\n"
        "/////////////////////////////////////////////////////\n")

    dijkstraAlgorithm() # dijkstraAlgorithm(): shortest paths between nodes in a graph

    print("\n\n* Creating network interface *\n")
    print("* Network interface has been downloaded for your convenience *\n")

    plt.figure(figsize = (10,7)) # create new figure (plot size (l x w) measured in inches)

    # Variable Declaration / Initialization #

    pos = nx.get_node_attributes(Network,'pos') # get_node_attributes(pos): gets node position information for nx.draw function parameters

    labels = nx.get_edge_attributes(Network, 'weight') # get_edge_attribues(weight): gets edge weight information for nx.draw function parameters
    labels = convertTuple(labels) # covertTuple(): adjusts weight label formattting to only display weight "#", not "{weight: #}""

    # List Declaration / Initialization : used to highlight unreachable nodes #

    List = nx.descendants(Network, sourceNode) # descendants(): returns a set of all nodes reachable from source node in the network
    List.add(sourceNode) # descendants() does not include source node as reachable; make sure to add source node back into the set

    nx.draw(Network, pos, node_color='cyan', # draw graph: node color: light blue, node labels: on, node size: 1000 (visibility)
        with_labels = True, 
        node_size = 1000)

    for node in Network.nodes(): # for loop: navigate through each node in the network
        if Network.has_node(node): # if statement: if the node is online (available) in the network -> evaluate if reachable
            if node is sourceNode: # if node is sourceNode: change node color to yellow to signify source node (head of the network)
                nx.draw_networkx_nodes(Network, pos, node, node_color = "yellow", # change source node color to yellow
                    node_size = 1000)
        
            if node in failedNodes: # if node is in the network and failed nodes list, then scenario indicates node recovery -> change node color to lime to signify node recovery
                nx.draw_networkx_nodes(Network, pos, nodelist = node, node_color = "lime", # change unreachable node color to red
                    node_size = 1000)
            
            if node not in List: # if node is not reachable: change node color to red to signify inaccessibility
                nx.draw_networkx_nodes(Network, pos, nodelist = node, node_color = "red", # change unreachable node color to red
                    node_size = 1000)

    nx.draw_networkx_edge_labels(Network, pos, labels, font_weight = 'heavy') # draw edge labels

def dijkstraAlgorithm(): # algorithm for finding the shortest paths between nodes in a graph: illustrates most optimal path/cost for each node from the source node

    List = nx.descendants(Network, sourceNode) # descendants(): returns a set of all nodes reachable from source node in the network
    List.add(sourceNode) # descendants() does not include source node as reachable; make sure to add source node back into the set

    for node in Network.nodes(): # for loop: navigate through each node in the network
        if Network.has_node(node): # if statement: if the node is online (available) in the network -> produce dijkstra evaluation
            if node in List: # if node is reachable: produce optimalCost and optimalPath from source node
                optimalCost = nx.dijkstra_path_length(Network, sourceNode, node, weight = 'weight') # optimalCost from source noce
                optimalPath = nx.dijkstra_path(Network, sourceNode, node, weight = 'weight') # optimalPath from source node
                print(str(sourceNode) + " to " + str(node) + " (path cost = " + str(optimalCost) + "): " + str(optimalPath) + "") # print statement
            else: # if node unreachable: print unreachable statement
                print(str(sourceNode) + " to " + str(node) + " (path cost = unavailable): Node " + str(node) + " is unreachable.") # print statement

def convertTuple(tup): # converts 3 Tuple to 2 Tuple for labeling purposes: remove last value
    
    dictionary = {} # variable declaration/initialization: dictionary keys

    for x, y in tup.items(): # for loop: for each item in the key, update the string
        dictionary.update({(x[0], x[1]): y}) # updates tuple text

    tup = dictionary # assign dictionary keys to new tuple

    return tup # return updated string

# MAIN PROGRAM #

# Variable Declaration / Initialization #

nodes = globalNode # number of nodes in the network (assigned by global variable)

totalFaults = globalFault # number of faults that will occur in tthe network (assigned by global variable)

probability = 0.1 # node probability (0 - 1)

counter = 1 # counter variable (used to name files)

# Generate Random Network #

if nodes < 1: # if statement (error handling): if the user assigns globalNode <= 0, system cannot simulate a mesh network as the network is empty; therefore, end program with error message.
    print("\nATTENTION: Mesh Network is offline.\n") # print error message (Mesh Network Offline)
    print("Cannot simulate an active network with no available routers. Please reassign globalNode value and try again. \n") # print error message (empty network)
    sys.exit() # exit program (sys library)

print("\n//////////////////////////////\n" # Label Design
        "/////  Original Network  /////\n"
        "//////////////////////////////\n")

if not sourceNode: # if statement (error handling): if the user does not assign a sourceNode, system will randomly assign one based on ascii_uppercase dictionary
    print("\nATTENTION: No predetermined source node available -> Assigning random source node to the mesh network\n") # print error message (Mesh Network Offline)
    
    sourceNode = random.choice(string.ascii_uppercase) # assign random source node using ASCII Uppercase library (A-Z)

print("\nThe mesh network source node is ['" + str(sourceNode) + "'].\n") # print statement: display current network source node

Network = randomNetwork(nodes, probability) # create random simulated network
displayNetwork() # displayNetwork(): show current state of network diagram
plt.savefig('Original Network.png') # save current figure/plot to current directory
plt.show() # show current figure/plot (opens new window)

# Generate Faulty Network: creates both node/link faults for every iteration of network loss (# will vary based on rand()) #

if totalFaults > 0: # if statement (error handling): only simulate a faulty network if the user indicates a total number of faults. If user assignments totalFaults <= 0, then display original network and end simulation. 

    print("\n////////////////////////////\n" # Label Design
            "/////  Faulty Network  /////\n"
            "////////////////////////////\n")

    print("ATTENTION: POWER OUTAGE INCOMING. SOME NETWORKS HAVE GONE OFFLINE. SOME NETWORKS MAY FAIL INTERMITTENTLY!\n") # print statement: intro to faulty network (some networks immediately offline: others intermittenly turn off (globalFault - 1))

    while totalFaults is not 0: # while loop: while scenario still has faults (pre-determined by user utilizing the simulator)

        Network = faultyNetwork(nodes) # create a faulty network by removing a random sample of nodes from the network
        displayNetwork() # displayNetwork(): show current state of network diagram
        plt.savefig('Faulty Network_' + str(counter) + '.png') # save current figure/plot to current directory
        plt.show() # show current figure/plot (opens new window)

        seconds = random.randint(1,15) # RNG Generator: seconds that the system will take to update network diagram (used to replicate real-time taken for a node to fail)

        if totalFaults is not 1:
            print("-----------------------------------------------------------------------------------------\n") # print statement (formatting)

            print("ATTENTION: MORE NETWORKS FAILING. NETWORK INTERFACE WILL BE UPDATED IN " + str(seconds) + " SECONDS.\n") # print statement: Intermittent Network Failure Prompt

            time.sleep(seconds) # system sleep (replicates time it takes for node to shutdown)

        counter = counter + 1 # counter increment

        totalFaults = totalFaults - 1 # variable (totalFaults) decrement

    # Generate Node Recovery: program generates a nodal recovery scenario by re-inserting some faulty networks from the first set using a multidimensional queue (i.e., node, edges, weight, etc.) [real world application] #

    print("\n///////////////////////////\n" # Label Design
            "/////  Node Recovery  /////\n"
            "///////////////////////////\n")

    print("ATTENTION: POWER RESTORING. SOME NETWORKS ARE BACK ONLINE!\n\n") # print statement: intro to nodal recovery: power restoration (initial faulty nodes are back online)
        
    failedNodes.append(queueNode.queue[0])

    # Organize Weights into List Data: formatting constraints #
    
    weight = weights[0]
    weight = str(weight)
    weight = weight.replace("0", '')
    weight = weight.replace("{", '')
    weight = weight.replace("}", '')
    weight = weight.replace("'weight'", '')
    weight = weight.replace("'", "")
    weight = weight.replace(",", '')
    weight = weight.replace("[", '')
    weight = weight.replace("]", '')
    weight = weight.replace(" ", '')
    weight = weight.replace("(", '')
    weight = weight.replace(":", '')
    weight = weight.split(")")

    # Organize Failed Node Weights #

    failedNodes = str(failedNodes)
    failedNodes = failedNodes.replace('[', '')
    failedNodes = failedNodes.replace(']', '')
    failedNodes = failedNodes.replace(',', '')
    failedNodes = failedNodes.replace("'", '')
    failedNodes = failedNodes.replace(' ', '')

    failedNodes = list(failedNodes) # list of failed nodes that were removed from the network
    existingNodes = list(Network.nodes) # list of current nodes inside the network (existing)

    # Nodal Recovery Algorithm: nested for loops to check if the failed node has edges to nodes that exist in the network -> reinsert node with corresponding edges using stored queue information #

    for i in range(len(failedNodes)):
        for l in range(len(existingNodes)):
            for j in range(len(weight)):
                if(failedNodes[i] in weight[j] and existingNodes[l] in weight[j]):
                    Network.add_node(failedNodes[i], pos = (random.randint(1, nodes * 10), random.randint(1, nodes * 10)))
                    Network.add_edge(failedNodes[i], existingNodes[l], weight = int(weight[j][2]))

    # Node Recovery Walkthrough (print statements) #
                
    print("List of failed nodes ready for node recovery:\n\n" + str(failedNodes) + "\n\n") # print statement: print list of failed nodes
    print("List of current nodes inside the network:\n\n" + str(existingNodes) + "\n\n") # print statement: print list of existing nodes
    print("List of current nodes inside the network after node recovery:\n\n" + str(Network.nodes) + "\n\n") # print statement: print list of combined lists (node recovery)
    print("List of current weighted edges for each node in the network:\n\n" + str(weight) + "\n") # print statement: print weighted edges for each node in the network

    displayNetwork() # displayNetwork(): show current state of network diagram
    plt.savefig('Nodal Recovery.png') # save current figure/plot to current directory
    plt.show() # show current figure/plot (opens new window)

    print("-----------------------------------------------------------------------------------------\n") # print statement (formatting)

    print("ATTENTION: REMAINING NETWORKS ARE NOW STABLE. THANK YOU FOR YOUR PATIENCE.\n\n") # print statement: Network Stability Prompt.

print("=== END OF SIMULATION === \n") # print statement: EOS Prompt
print("* all network diagrams have been saved to your directory *\n") # print statement: User File Prompt
