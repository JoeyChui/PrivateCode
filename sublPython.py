def findMedianSortedArrays(nums1, nums2):
    len1, len2 = len(nums1), len(nums2)
    index = (len1 + len2) // 2 + 1  # 第index个数为 奇数时 的中位数
    n, n1, n2 = 0, 0, 0
    i, j = 0, 0
    while True:
        if nums1[i] < nums2[j]:
            if i < len1 - 1:
                i += 1
                n = nums1[i]
            else:
                j += 1
                n = nums2[j]
        else:
            if j < len2 - 1:
                j += 1
                n = nums2[j]
            else:
                i += 1
                n = nums1[i]

        if i + j + 1 == index - 1:
            n1 = n
        if i + j + 2 == index:
            n2 = n
            break
    print(i, j, n1, n2, n)
    if (len1 + len2) % 2 == 0:
        return (n1 + n2) / 2
    else:
        return float(n2)

ans = findMedianSortedArrays([1, 2], [3, 4])
print(ans)