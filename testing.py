def find_combinations(names_numbers, target_sum, partial=[], start=0):
    result = []
    
    # Check if the partial sum equals the target sum
    if sum(names_numbers[name] for name in partial) >= target_sum:
        result.append(partial[:])
    
    # Base case: If the partial sum exceeds the target sum or the list is empty, return
    if sum(names_numbers[name] for name in partial) >= target_sum or start == len(names_numbers):
        return result
    
    # Recursively find combinations including and excluding the current number
    for i in range(start, len(names_numbers)):
        name = list(names_numbers.keys())[i]
        result.extend(find_combinations(names_numbers, target_sum, partial + [name], i + 1))
    
    return result

# Example usage
names_numbers = {'Alice': 2, 'Bob': 3, 'Charlie': 6, 'David': 7, 'Eve': 8}
target_sum = 10
combinations = find_combinations(names_numbers, target_sum)
print("Combinations that meet or exceed the target sum:", combinations)