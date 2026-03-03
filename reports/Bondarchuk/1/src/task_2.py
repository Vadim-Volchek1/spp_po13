"""1.2)"""

if __name__ == '__main__':
    m = int(input("m:"))
    n = int(input("n:"))
    nums1=[]
    nums2=[]

    for i in range(m):
        nums1.append(i)
    for i in range(n):
        nums1.append(0)
    print("nums1",nums1)
    for i in range(n):
        nums2.append(i)
    print("nums2",nums2)

    for i in range(n):
        nums1[m+i]=nums2[i]
    nums1.sort()
    print("sorted:",nums1)
