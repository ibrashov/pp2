def main():
    string = input("Write: ")
    upper_count = sum(1 for c in string if c.isupper())
    lower_count = sum(1 for c in string if c.islower())
    print("Lower:", lower_count)
    print("Upper:", upper_count)


if __name__ == "__main__":
    main()