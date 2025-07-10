import networkx as nx
from backend.routing.utils import nearest_node, calc_cost
from backend.routing.multimodal_graph import MultimodalGraphBuilder

def get_multimodal_route(G, start_lat, start_lon, end_lat, end_lon):
    start = nearest_node(G, start_lat, start_lon)
    end = nearest_node(G, end_lat, end_lon)
    path = nx.shortest_path(G, start, end, weight='time')
    segments = []
    total_time = 0
    total_cost = 0
    current_mode = None
    current_coords = []
    current_time = 0
    current_cost = 0
    for i in range(len(path)-1):
        u, v = path[i], path[i+1]
        edge = G[u][v][0] if isinstance(G[u][v], dict) else G[u][v]
        mode = edge.get('mode', 'walk')
        time = edge.get('time', 1)
        node_data = G.nodes[u]
        coord = [node_data['y'], node_data['x']]
        if current_mode is None:
            current_mode = mode
        if mode != current_mode:
            segments.append({
                'mode': current_mode,
                'coords': current_coords,
                'time': current_time,
                'cost': current_cost
            })
            current_mode = mode
            current_coords = []
            current_time = 0
            current_cost = 0
        current_coords.append(coord)
        current_time += time
        current_cost += calc_cost(mode, time)
        total_time += time
        total_cost += calc_cost(mode, time)
    # Add last segment
    if current_coords:
        segments.append({
            'mode': current_mode,
            'coords': current_coords,
            'time': current_time,
            'cost': current_cost
        })
    return {
        'total_time': int(total_time),
        'total_cost': int(total_cost),
        'segments': segments
    } 