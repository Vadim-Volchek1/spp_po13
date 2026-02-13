def find_outlier_median(seq):
    seq_sorted = sorted(seq)
    median = seq_sorted[len(seq)//2]   
    outlier = max(seq, key=lambda x: abs(x - median))
    return outlier
numbers = list(map(int, input("Enter array: ").split()))
print("Array:", numbers)
print("Outlier:", find_outlier_median(numbers))
