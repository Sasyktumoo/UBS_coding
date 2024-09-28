def find_corrections(dictionary, mistypes):
    # Preprocess dictionary
    correction_map = {}
    
    for word in dictionary:
        for i in range(len(word)):
            # Generate mistyped version by changing each letter
            for c in range(ord('a'), ord('z') + 1):
                if chr(c) != word[i]:
                    mistyped = word[:i] + chr(c) + word[i+1:]
                    correction_map[mistyped] = word
    
    # Find corrections
    corrections = []
    for mistyped in mistypes:
        if mistyped in correction_map:
            corrections.append(correction_map[mistyped])
    
    return corrections

# Example usage
dictionary = ["purple", "rocket", "silver", "gadget", "window", "dragon"]
mistypes = ["purqle", "gadgat", "socket", "salver"]

corrections = find_corrections(dictionary, mistypes)
print(corrections)