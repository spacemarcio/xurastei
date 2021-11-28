## Step-by-step to setup clusters

There `clustering.py` file runs a K-Means with locations data. You wont have any surprises, just have the data in the right places. So, setup database first.

## Give me details!

There is not much to talk about K-Means, but I make some pretty important transformations. The big one is to transform the number of places in rates. So instead of '5 green areas in CoolNeighbourhood' let's measure how much of the green areas in the whole city belong to a specific location ('1,25% of the green areas belong to green areas in CoolNeighbourhood', is this example). This makes the model features more stable at times. The days goes and city increase, so a big number in the past can be not so big in the future.