from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from backend.routing.router import get_multimodal_route
from backend.routing.multimodal_graph import MultimodalGraphBuilder

app = FastAPI()

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# North, South, East, West (covers most of Amsterdam)
graph_builder = MultimodalGraphBuilder((52.430, 52.320, 4.990, 4.730))
G = graph_builder.build()

@app.get("/route")
def get_route(
    start_lat: float = Query(...),
    start_lon: float = Query(...),
    end_lat: float = Query(...),
    end_lon: float = Query(...)
):
    return get_multimodal_route(G, start_lat, start_lon, end_lat, end_lon) 