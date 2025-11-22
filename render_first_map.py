import folium
from folium import plugins

berlin_center = [52.5036504, 13.4447152]
mymap = folium.Map(location = berlin_center, zoom_start = 14)


point1 = [52.5163, 13.4050]
point1_name = "Brandenburg Gate"

point2 = [52.5219, 13.4132]
point2_name = "Alexa"

folium.Marker(location = point1,
              popup = point1_name
              ).add_to(mymap)

folium.Marker(location = point2,
              popup = point2_name
              ).add_to(mymap)

folium.PolyLine(
    locations=[point1,point2]
).add_to(mymap)

# plugins.AntPath(locations=[point1, point2]).add_to(mymap)

mymap.show_in_browser()