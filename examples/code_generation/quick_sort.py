"""
快速排序算法示例
Quick Sort Algorithm Example

使用衍智体生成的快速排序实现
"""

from typing import List


def quick_sort(arr: List[int]) -> List[int]:
    """
    快速排序实现
    
    参数:
        arr: 待排序的整数列表
        
    返回:
        排序后的整数列表
        
    时间复杂度: O(n log n) 平均情况
    空间复杂度: O(log n)
    """
    # 基础情况：空列表或单元素列表已有序
    if len(arr) <= 1:
        return arr
    
    # 选择基准值 (这里选择中间元素)
    pivot = arr[len(arr) // 2]
    
    # 分割成三个部分
    left = [x for x in arr if x < pivot]      # 小于基准值的元素
    middle = [x for x in arr if x == pivot]   # 等于基准值的元素
    right = [x for x in arr if x > pivot]     # 大于基准值的元素
    
    # 递归排序左右部分，然后合并
    return quick_sort(left) + middle + quick_sort(right)


def quick_sort_inplace(arr: List[int], low: int = 0, high: int = None) -> None:
    """
    快速排序 - 原地版本 (节省空间)
    
    参数:
        arr: 待排序的整数列表
        low: 起始索引
        high: 结束索引
        
    时间复杂度: O(n log n) 平均情况
    空间复杂度: O(1) 额外空间
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        # 分区操作
        pivot_index = partition(arr, low, high)
        
        # 递归排序左右子数组
        quick_sort_inplace(arr, low, pivot_index - 1)
        quick_sort_inplace(arr, pivot_index + 1, high)


def partition(arr: List[int], low: int, high: int) -> int:
    """
    分区函数 - 将数组分为小于和大于基准值的两部分
    
    参数:
        arr: 待分区数组
        low: 起始索引
        high: 结束索引
        
    返回:
        基准值的最终位置索引
    """
    # 选择最右边元素作为基准值
    pivot = arr[high]
    i = low - 1  # i 是小于 pivot 的区域的最后一个索引
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            # 交换 arr[i] 和 arr[j]
            arr[i], arr[j] = arr[j], arr[i]
    
    # 将基准值放到正确位置
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def test_quick_sort():
    """测试快速排序函数"""
    # 测试用例 1: 普通数组
    arr1 = [64, 34, 25, 12, 22, 11, 90]
    result1 = quick_sort(arr1)
    print(f"原数组：{arr1}")
    print(f"排序后：{result1}")
    assert result1 == [11, 12, 22, 25, 34, 64, 90]
    
    # 测试用例 2: 包含重复元素
    arr2 = [5, 2, 8, 2, 9, 1, 5, 5]
    result2 = quick_sort(arr2)
    print(f"\n原数组：{arr2}")
    print(f"排序后：{result2}")
    assert result2 == [1, 2, 2, 5, 5, 5, 8, 9]
    
    # 测试用例 3: 已排序数组
    arr3 = [1, 2, 3, 4, 5]
    result3 = quick_sort(arr3)
    print(f"\n原数组：{arr3}")
    print(f"排序后：{result3}")
    assert result3 == [1, 2, 3, 4, 5]
    
    # 测试用例 4: 空数组
    arr4 = []
    result4 = quick_sort(arr4)
    print(f"\n原数组：{arr4}")
    print(f"排序后：{result4}")
    assert result4 == []
    
    # 测试用例 5: 单元素数组
    arr5 = [42]
    result5 = quick_sort(arr5)
    print(f"\n原数组：{arr5}")
    print(f"排序后：{result5}")
    assert result5 == [42]
    
    print("\n✅ 所有测试通过!")


if __name__ == "__main__":
    # 运行测试
    test_quick_sort()
    
    # 性能对比示例
    import time
    
    # 生成大数组测试性能
    import random
    large_arr = [random.randint(1, 10000) for _ in range(1000)]
    
    start_time = time.time()
    quick_sort(large_arr)
    end_time = time.time()
    
    print(f"\n性能测试:")
    print(f"数组大小：{len(large_arr)}")
    print(f"排序时间：{(end_time - start_time) * 1000:.2f} 毫秒")
