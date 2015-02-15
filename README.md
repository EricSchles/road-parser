# road-parser
Parses WKT csv files generated from subsets of the data.vic.gov.au road network shapefile into a networkx graph.


#### To run 

```python roadroad_networkx.py INPUT_FILE DICT_FILE CREATE_FLAG``` 

###### Eg.  

```python roadroad_networkx.py roads.csv paths.dict TRUE```

Then 

```python roadroad_networkx.py roads.csv paths.dict FALSE```

#### Flags

```CREATE_FLAG``` can be ```TRUE``` or ```_```

If ```CREATE_FLAG``` is  ```TRUE``` a shelve dictionary will be created at the path ```DICT_FILE``` contianing every shortest path pair of graph.

Else the dictionary will be loaded in from the path ```DICT_FILE``` to be used for shortest path tests.

#### Other

Also contains a method for drawing graph to screen, currently unused. 
