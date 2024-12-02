# Data Division
To ensure proper utilization of the training and evaluation sets during cross-validation, the data is divided into four stratified partitions. One partition is designated for evaluation, while the remaining three are used for training. For simplicity and consistency, the subsets are organized into files named testX.txt and trainX.txt, where X can be 1, 2, 3, or 4.

For instance, if test1.txt is used for evaluation, then train1.txt should be used for training. The file test1.txt contains data from one partition, while train1.txt includes the combined data from the other three partitions.
