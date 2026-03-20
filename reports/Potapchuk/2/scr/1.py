class IntegerSet:
    def __init__(self, initial_elements=None):
        if initial_elements is None:
            self.elements = []
        else:
            seen = set()
            self.elements = [
                x for x in initial_elements if not (x in seen or seen.add(x))
            ]

    def add(self, element):
        if element not in self.elements:
            self.elements.append(element)

    def remove(self, element):
        if element in self.elements:
            self.elements.remove(element)

    def contains(self, element):
        return element in self.elements

    def intersection(self, other):
        if not isinstance(other, IntegerSet):
            raise ValueError("Can only intersect with another IntegerSet")
        common = [x for x in self.elements if x in other.elements]
        return IntegerSet(common)

    def __str__(self):
        if not self.elements:
            return "{}"
        return "{" + ", ".join(map(str, sorted(self.elements))) + "}"

    def __eq__(self, other):
        if not isinstance(other, IntegerSet):
            return False
        return sorted(self.elements) == sorted(other.elements)


def main():
    try:
        n1 = int(input("Enter number of elements in first set: "))
        line1 = input("Enter elements of first set: ").strip()
        elems1 = list(map(int, line1.split()))[:n1]
        set1 = IntegerSet(elems1)

        n2 = int(input("Enter number of elements in second set: "))
        line2 = input("Enter elements of second set: ").strip()
        elems2 = list(map(int, line2.split()))[:n2]
        set2 = IntegerSet(elems2)

        print("First set:      ", set1)
        print("Second set:     ", set2)
        print("Intersection:   ", set1.intersection(set2))

        value = int(input("Enter value to check in first set: "))
        print(f"{value} in first set?   {set1.contains(value)}")

        add_val = int(input("Enter value to add to first set: "))
        set1.add(add_val)
        print("After adding:   ", set1)

        rem_val = int(input("Enter value to remove from first set: "))
        set1.remove(rem_val)
        print("After removing: ", set1)

        print("Sets are equal: ", set1 == set2)

    except ValueError as e:
        print("Error: invalid input (expected integer(s))")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
