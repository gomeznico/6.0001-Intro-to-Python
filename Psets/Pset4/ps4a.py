# Problem Set 4A
# Name: Nico Gomez
# Collaborators:
# Time Spent: 20 min

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''


    output = []

    ## Base Case
    if len(sequence) == 2:
        output.append(sequence)
        output.append(sequence[1] + sequence[0])
        return output

    ## Recursive Case
    for i in range(len(sequence)):
        first_letter = sequence[i]
        remaining_seq = sequence[0:i] + sequence[i+1:len(sequence)]
        other_permutations = get_permutations(remaining_seq)
        for permutation in other_permutations:
            output.append(first_letter + permutation)

    return output

if __name__ == '__main__':
    # EXAMPLE
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:  ', get_permutations(example_input))
    print('============================================================')

    example_input = '123'
    print('Input:', example_input)
    print('Expected Output:', ['123', '132', '213', '231', '312', '321'])
    print('Actual Output:  ', get_permutations(example_input))
    print('============================================================')


    example_input = 'AB'
    print('Input:', example_input)
    print('Expected Output:', ['AB', 'BA'])
    print('Actual Output:  ', get_permutations(example_input))
    print('============================================================')

    example_input = '1234'
    example_output = [
    '1234',
    '1243',
    '1324',
    '1342',
    '1423',
    '1432',
    '2134',
    '2143',
    '2314',
    '2341',
    '2413',
    '2431',
    '3124',
    '3142',
    '3214',
    '3241',
    '3412',
    '3421',
    '4123',
    '4132',
    '4213',
    '4231',
    '4312',
    '4321',
    ]
    print('Input:', example_input)
    print('IT IS:', example_output == get_permutations(example_input), ':THAT OUTPUT IS WHATS EXPECTED')




