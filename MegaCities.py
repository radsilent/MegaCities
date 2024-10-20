import matplotlib.pyplot as plt
import geopandas as gpd
from geopy.distance import great_circle
import networkx as nx
from adjustText import adjust_text

# Top 30 most populated cities in the world (coordinates: latitude, longitude, and city names)
cities = {
    "Tokyo, Japan": (35.682839, 139.759455),
    "Delhi, India": (28.704060, 77.102493),
    "Shanghai, China": (31.230391, 121.473701),
    "São Paulo, Brazil": (-23.550520, -46.633308),
    "Mexico City, Mexico": (19.432608, -99.133209),
    "Cairo, Egypt": (30.044420, 31.235712),
    "Dhaka, Bangladesh": (23.810331, 90.412521),
    "Mumbai, India": (19.075984, 72.877656),
    "Beijing, China": (39.904202, 116.407394),
    "Osaka, Japan": (34.693738, 135.502165),
    "Karachi, Pakistan": (24.860735, 67.001137),
    "Chongqing, China": (29.431586, 106.912251),
    "Istanbul, Turkey": (41.008238, 28.978359),
    "Buenos Aires, Argentina": (-34.603722, -58.381592),
    "Kolkata, India": (22.572646, 88.363895),
    "Kinshasa, DR Congo": (-4.441931, 15.266293),
    "Lagos, Nigeria": (6.524379, 3.379206),
    "Manila, Philippines": (14.599512, 120.984222),
    "Rio de Janeiro, Brazil": (-22.906847, -43.172896),
    "Guangzhou, China": (23.129110, 113.264385),
    "Los Angeles, USA": (34.052235, -118.243683),
    "Moscow, Russia": (55.755825, 37.617298),
    "Shenzhen, China": (22.543096, 114.057865),
    "Lahore, Pakistan": (31.549722, 74.343611),
    "Bangalore, India": (12.971599, 77.594566),
    "Paris, France": (48.856613, 2.352222),
    "Bogotá, Colombia": (4.7110, -74.0721),
    "Jakarta, Indonesia": (-6.208763, 106.845599),
    "Lima, Peru": (-12.046374, -77.042793),
    "Bangkok, Thailand": (13.756331, 100.501762)
}

# Load the world map from local shapefile

world = gpd.read_file(r"C:\EnergyCenters\Natural_Earth_quick_start\packages\Natural_Earth_quick_start\110m_cultural\ne_110m_admin_0_countries.shp")

# Create a NetworkX graph to store the nodes and edges
G = nx.Graph()

# Add nodes (cities) to the graph
for city, (lat, lon) in cities.items():
    G.add_node(city, pos=(lon, lat))  # Storing (longitude, latitude) to maintain correct order

# Connect each city to its three nearest neighbors based on distance
nodes = list(G.nodes)
for node1 in nodes:
    distances = []
    for node2 in nodes:
        if node1 != node2:
            coord1 = (cities[node1][0], cities[node1][1])
            coord2 = (cities[node2][0], cities[node2][1])
            dist = great_circle(coord1, coord2).kilometers
            distances.append((node2, dist))
    
    # Sort by distance and connect to three nearest cities
    distances = sorted(distances, key=lambda x: x[1])[:3]
    for neighbor, dist in distances:
        G.add_edge(node1, neighbor, weight=dist)

# Ensure the graph is fully connected by adding a minimum spanning tree
mst = nx.minimum_spanning_tree(G)
for edge in mst.edges(data=True):
    G.add_edge(edge[0], edge[1], weight=edge[2]['weight'])

# Plot the map
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, color='lightgrey')

# Plot connections between cities (edges)
for edge in G.edges(data=True):
    node1, node2 = edge[0], edge[1]
    lon1, lat1 = cities[node1][1], cities[node1][0]  # Correcting the order: lon, lat
    lon2, lat2 = cities[node2][1], cities[node2][0]  # Correcting the order: lon, lat
    ax.plot([lon1, lon2], [lat1, lat2], color='blue', linestyle='--', linewidth=1, zorder=1)

# Plot cities (nodes) and labels
texts = []
for city, (lat, lon) in cities.items():
    ax.scatter(lon, lat, color='red', s=100, zorder=2)
    # Add city labels using ax.text
    texts.append(ax.text(lon, lat, city, fontsize=9, ha='right', zorder=3))

# Adjust text labels to avoid overlapping
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black'))

# Title of the plot
ax.set_title("Top 30 Most Populated Cities and Connections", fontsize=16)

# Set axis labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Show the plot
plt.show()
