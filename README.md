# road-parser
Parses WKT csv files generated from subsets of the data.vic.gov.au road network shapefile into a networkx graph.


#### To run 

```python roadroad_networkx.py -p PICKLE_PATH [-c CSV_PATH]``` 

###### Eg.  

```python roadroad_networkx.py -p graph.pickle -c roads.csv```

Then 

```python roadroad_networkx.py -p graph.pickle```

#### Flags

If ```-c CSV_PATH``` is given then the csv file will be read, and a graph generated and pickled to ```PICKLE_PATH```. 

Else the graph will be loaded from ```PICKLE_PATH``` and a sample path found and printed.

#### Other

Also contains a method for drawing graph to screen, currently unused. 
