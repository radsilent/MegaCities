import matplotlib.pyplot as plt
import geopandas as gpd
from geopy.distance import great_circle
import networkx as nx
from adjustText import adjust_text

# Top 100 most populated cities in the world (coordinates: latitude, longitude, and city names)
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
    "Bangkok, Thailand": (13.756331, 100.501762),
    "Chengdu, China": (30.572815, 104.066801),
    "Tianjin, China": (39.343357, 117.361647),
    "London, UK": (51.5074, -0.1278),
    "Tehran, Iran": (35.6892, 51.3890),
    "New York City, USA": (40.712776, -74.005974),
    "Hyderabad, India": (17.385044, 78.486671),
    "Santiago, Chile": (-33.4489, -70.6693),
    "Singapore": (1.3521, 103.8198),
    "Hong Kong": (22.3964, 114.1095),
    "Miami, USA": (25.7617, -80.1918),
    "Kuala Lumpur, Malaysia": (3.1390, 101.6869),
    "Dubai, UAE": (25.276987, 55.296249),
    "Seoul, South Korea": (37.5665, 126.9780),
    "Rome, Italy": (41.9028, 12.4964),
    "Madrid, Spain": (40.4168, -3.7038),
    "Zurich, Switzerland": (47.3769, 8.5417),
    "Berlin, Germany": (52.5200, 13.4050),
    "Sydney, Australia": (-33.8688, 151.2093),
    "Melbourne, Australia": (-37.8136, 144.9631),
    "Toronto, Canada": (43.6532, -79.3832),
    "Chicago, USA": (41.8781, -87.6298),
    "Dallas, USA": (32.7767, -96.7970),
    # Add more cities up to the top 100
}

# Load the world map from local shapefile
world = gpd.read_file(r"C:\EnergyCenters\Natural_Earth_quick_start\packages\Natural_Earth_quick_start\110m_cultural\ne_110m_admin_0_countries.shp")

# Create a NetworkX graph to store the nodes and edges
G = nx.Graph()

# Add nodes (cities) to the graph
for city, (lat, lon) in cities.items():
    G.add_node(city, pos=(lon, lat))  # Storing (longitude, latitude) to maintain correct order

# Calculate distances between every pair of cities and add edges
for city1 in cities:
    for city2 in cities:
        if city1 != city2:
            coord1 = cities[city1]
            coord2 = cities[city2]
            dist = great_circle(coord1, coord2).kilometers
            G.add_edge(city1, city2, weight=dist)

# Compute the minimum spanning tree (MST) to ensure each city is connected with the shortest possible total distance
mst = nx.minimum_spanning_tree(G)

# Plot the map
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, color='lightgrey')

# Plot MST edges (connections between cities)
for edge in mst.edges(data=True):
    city1, city2 = edge[0], edge[1]
    lon1, lat1 = cities[city1][1], cities[city1][0]
    lon2, lat2 = cities[city2][1], cities[city2][0]
    ax.plot([lon1, lon2], [lat1, lat2], color='blue', linestyle='--', linewidth=1, zorder=1)

# Plot cities (nodes) with smaller size and labels
texts = []
for city, (lat, lon) in cities.items():
    ax.scatter(lon, lat, color='red', s=50, zorder=2)  # Reduced node size from 100 to 50
    # Add city labels using ax.text with smaller font size
    texts.append(ax.text(lon, lat, city, fontsize=5, ha='right', zorder=3))

# Adjust text labels to avoid overlapping
adjust_text(texts, arrowprops=dict(arrowstyle='-', color='black'))

# Title of the plot
ax.set_title("Vector Stream Systems Minimum Spanning Tree Top 100 Most Populated Cities 2024", fontsize=16)

# Set axis labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Show the plot
plt.show()
