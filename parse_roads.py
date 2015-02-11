import sys

points = []
pairs = []
links = {}

input_path = sys.argv[1]
output_path = sys.argv[2]
ignore_one_way = (sys.argv[3] == 'true')

with open(input_path) as f:
  for line in f:
    direction = line[1]
    line_points = line.strip()[13:-1].split(',')
    points += line_points
    #GET LINKS
    for i in range(len(line_points)-1):
      pairs.append([line_points[i], line_points[i+1]])
      #TWO WAY STREET
      if (direction == 'B' or ignore_one_way):
        pairs.append([line_points[i+1], line_points[i]])

points = list(set(points))
for point in points:
  point_links = []
  for pair in pairs:
    if (pair[0] == point):
      point_links.append(pair[1])
  links[point] = point_links

with open(output_path, 'a') as f:
  for point in points:
    f.write(point + '\n')
    f.write(str(links[point])+'\n')
