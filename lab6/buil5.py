
def all_true(t):
    return all(t)

if __name__ == "__main__":
    sample = (True, 1, "yes", [1], 3.14)
    print("Tuple:", sample)
    print("True:", all_true(sample))
