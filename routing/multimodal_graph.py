import osmnx as ox
import networkx as nx
from shapely.geometry import Point
from geopy.distance import geodesic

class MultimodalGraphBuilder:
    def __init__(self, place_or_bbox, walk_speed=5, bike_speed=15, car_speed=40):
        self.place_or_bbox = place_or_bbox
        self.walk_speed = walk_speed
        self.bike_speed = bike_speed
        self.car_speed = car_speed
        self.graph = None

    def build(self):
        if isinstance(self.place_or_bbox, tuple):
            north, south, east, west = self.place_or_bbox
            walk = ox.graph_from_bbox(
                north=north,
                south=south,
                east=east,
                west=west,
                network_type='walk'
            )
            bike = ox.graph_from_bbox(
                north=north,
                south=south,
                east=east,
                west=west,
                network_type='bike'
            )
            car = ox.graph_from_bbox(
                north=north,
                south=south,
                east=east,
                west=west,
                network_type='drive'
            )
        else:
            walk = ox.graph_from_place(self.place_or_bbox, network_type='walk')
            bike = ox.graph_from_place(self.place_or_bbox, network_type='bike')
            car = ox.graph_from_place(self.place_or_bbox, network_type='drive')

        # Relabel nodes to keep them unique per mode
        walk = nx.relabel_nodes(walk, lambda n: f"{n}_walk")
        bike = nx.relabel_nodes(bike, lambda n: f"{n}_bike")
        car = nx.relabel_nodes(car, lambda n: f"{n}_car")

        # Add mode attribute to edges
        for G, mode, speed in [(walk, 'walk', self.walk_speed), (bike, 'bike', self.bike_speed), (car, 'car', self.car_speed)]:
            for u, v, data in G.edges(data=True):
                data['mode'] = mode
                # Calculate time in minutes
                if 'length' in data:
                    data['time'] = data['length'] / 1000 / speed * 60
                else:
                    data['time'] = 1  # fallback

        # Merge graphs
        G = nx.compose_all([walk, bike, car])

        # Add interlayer transfer edges (within 10m)
        self._add_interlayer_edges(G, walk, bike, car)
        self.graph = G
        return G

    def _add_interlayer_edges(self, G, walk, bike, car):
        # Build lookup for node positions
        node_pos = {}
        for mode_graph, suffix in [(walk, '_walk'), (bike, '_bike'), (car, '_car')]:
            for n, data in mode_graph.nodes(data=True):
                node_pos[n] = (data['y'], data['x'])
        # For each pair of modes, add transfer edges if nodes are within 10m
        for n1, pos1 in node_pos.items():
            for n2, pos2 in node_pos.items():
                if n1 == n2:
                    continue
                if n1.split('_')[0] == n2.split('_')[0]:
                    continue  # same OSM node, different mode
                if geodesic(pos1, pos2).meters <= 10:
                    G.add_edge(n1, n2, weight=1, time=1, mode='transfer') 