## Project Razor
A branch and bound algorithm for the scheduling problem with a single machine, with minimum weighted sum of weighted completion times required and release dates constraints. 

### Usage 
This simple application has been developed using Python 3.x. To start the execution, use the following command:
```
python3 main.py sample.csv
```

### Input CSV format
The sample CSV file must be formatted as per te following example:
```
id,release,processing,weight
1,0,7,5,35
2,1,4,2,8
3,3,5,2,10
4,8,3,6,18
5,8,8,1,8
...
```

#### References
Plese refer to the documentation under `references.pdf` - this work was realized following the well written papers of Hariri, Potts and Posner.