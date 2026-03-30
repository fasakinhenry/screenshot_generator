def running_sum(nums):
    """
    Calculate the running sum of a list of numbers.
    
    Args:
        nums: List of integers
        
    Returns:
        List with running sum at each index
    """
    result = []
    total = 0
    for num in nums:
        total += num
        result.append(total)
    return result


# Example usage
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    print(running_sum(numbers))  # Output: [1, 3, 6, 10, 15]