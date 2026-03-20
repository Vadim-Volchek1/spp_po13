"""
Module for IntegerSet operations.
"""


class IntegerSet:
    """A collection of unique integers with basic set operations."""

    def __init__(self, initial_elements=None):
        """Initialize the set with unique elements from the provided list."""
        if initial_elements is None:
            self.elements = []
        else:
            seen = set()
            self.elements = [x for x in initial_elements if not (x in seen or seen.add(x))]

    def add(self, element):
        """Add an integer to the set if it is not already present."""
        if element not in self.elements:
            self.elements.append(element)

    def remove(self, element):
        """Remove an integer from the set if it exists."""
        if element in self.elements:
            self.elements.remove(element)

    def contains(self, element):
        """Check if an integer exists in the set."""
        return element in self.elements

    def intersection(self, other):
        """Return a new IntegerSet containing common elements."""
        if not isinstance(other, IntegerSet):
            raise TypeError("Can only intersect with another IntegerSet")
        common = [x for x in self.elements if x in other.elements]
        return IntegerSet(common)

    def __str__(self):
        """Return a string representation of the set."""
        if not self.elements:
            return "{}"
        sorted_elements = ", ".join(map(str, sorted(self.elements)))
        return "{" + sorted_elements + "}"

    def __eq__(self, other):
        """Compare two sets for equality based on their elements."""
        if not isinstance(other, IntegerSet):
            return False
        return sorted(self.elements) == sorted(other.elements)


def main():
    """Main execution block for interacting with IntegerSet."""
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

    except ValueError:
        # Fixed W0718 and W0612 by removing 'as e' and catching specific error
        print("Error: invalid input (expected integer(s))")
    except EOFError:
        print("\nInput interrupted.")
    except TypeError as error:
        # Catching specific TypeError for intersection
        print(f"Type error: {error}")


if __name__ == "__main__":
    main()
