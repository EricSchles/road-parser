points = []
pairs = []
links = {}

with open("input.txt") as f:
  for line in f:
    direction = line[1]
    line_points = line.strip()[13:-1].split(',')
    points += line_points
    #GET LINKS
    for i in range(len(line_points)-1):
      pairs.append([line_points[i], line_points[i+1]])
      #TWO WAY STREET
      if (direction == 'B'):
        pairs.append([line_points[i+1], line_points[i]])

points = list(set(points))
for point in points:
  point_links = []
  for pair in pairs:
    if (pair[0] == point):
      point_links.append(pair[1])
  links[point] = point_links

with open('output.txt', 'a') as f:
  for point in points:
    f.write(point + '\n')
    f.write(str(links[point])+'\n')
