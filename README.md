# AI-Powered Multimodal Smart City Routing System

## Overview
This project is a full-stack multimodal routing system that allows users to select two points on a city map and calculates the fastest route using walking, biking, and car modes. The route is displayed on a map with colored segments per mode, and total travel time and cost are shown.

## Features
- Select start and end points on a map
- Fastest route calculation using walking, biking, and car
- Colored route segments by mode (walk: yellow, bike: orange, car: blue)
- Total time and cost display
- Real-world map data from OpenStreetMap
- Modular backend for future reinforcement learning integration

## Backend (Python/FastAPI)
### Setup
1. `cd backend`
2. (Optional) Create a virtual environment
3. `pip install -r requirements.txt`
4. `uvicorn main:app --reload`

The backend will download OSM data for Dhaka, Bangladesh by default. You can change the city in `main.py`.

## Frontend (Leaflet/JS/HTML/CSS)
### Setup
1. Open `frontend/index.html` in your browser
2. Ensure the backend is running and accessible at the same host/port

## Usage
- Click once on the map to set the start point
- Click again to set the end point
- The fastest multimodal route will be displayed with colored segments
- Total time and cost will appear in the info box

## File Structure
See the project prompt for a detailed breakdown.

## Future Features
- Reinforcement learning for route optimization
- Traffic-aware edge weights
- Real-time GPS tracking
- Personalized recommendations 