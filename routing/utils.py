import networkx as nx
from geopy.distance import geodesic

def nearest_node(G, lat, lon):
    min_dist = float('inf')
    nearest = None
    for n, data in G.nodes(data=True):
        node_lat, node_lon = data.get('y'), data.get('x')
        if node_lat is None or node_lon is None:
            continue
        dist = geodesic((lat, lon), (node_lat, node_lon)).meters
        if dist < min_dist:
            min_dist = dist
            nearest = n
    print(f"Requested: ({lat}, {lon}), Nearest: {G.nodes[nearest]['y']}, {G.nodes[nearest]['x']}")
    return nearest

def calc_cost(mode, time):
    if mode == 'car':
        return 20  # flat rate per car trip
    return 0 