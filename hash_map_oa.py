# Name: Steven Bertolucci
# OSU Email: bertolus@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6: HashMap (Portfolio Assignment)
# Due Date: March 17, 2023
# Description:
#       --------------------------------------------------------------
#           In this file, I am implementing a hash table using
#           a dynamic array to store my hash table and implement
#           open addressing with Quadratic Probing for collision
#           resolution. Chains of key/value pairs must be stored
#           in a dynamic array.
#       --------------------------------------------------------------

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map. If the
        given key already exists in hash map, its associated value must
        be replaced with a new value. Double the table size if the load
        factor is greater than 0.5.
        """
        # Check to make sure load factor is less than 0.5.
        # If greater than 0.5, double the capacity of the table
        if self.table_load() > 0.5:
            # Double the old capacity
            new_capacity = self._capacity * 2
            self.resize_table(new_capacity)

        # Computes an index in the next two lines
        hash = self._hash_function(key)
        index = hash % self._capacity
        # Initialize newIndex for Quadratic probing aka moving/dynamic index
        newIndex = index
        # Initialize j to 1 for Quadratic probing
        j = 1
        # For inserting hash k/v entries
        hashKV = HashEntry(key, value)

        # If the bucket/index is empty, add the key to this index
        if self._buckets[index] is None:
            self._buckets.set_at_index(index, hashKV)
            self._size += 1

        # If the index is not empty, find the next index
        while self._buckets[newIndex] is not None:
            # Check if the new dynamic array has matching key
            if self._buckets[newIndex].key == key:
                # Check if the element is not a tombstone, insert it
                # and increase size
                if self._buckets[newIndex].is_tombstone:
                    # Insert the key value
                    self._buckets.set_at_index(newIndex, hashKV)
                    self._size += 1
                #  If the value is a tombstone, replace it
                if not self._buckets[newIndex].is_tombstone:
                    self._buckets.set_at_index(newIndex, hashKV)
                return
            # Quadratic probing to find next index
            newIndex = (index + j**2) % self._capacity
            j += 1

        # Insert the key value at the next index
        self._buckets.set_at_index(newIndex, hashKV)
        self._size += 1

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor
        """
        load_factor = self._size / self._buckets.length()
        return load_factor

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.
        """
        # Initialize numOfBuckets to keep count of buckets that are empty
        numOfBuckets = 0
        # Iterate through the buckets and check to see if it's empty and not
        # tombstone
        for buckets in range(self._capacity):
            # If the bucket is empty, increment numOfBuckets
            if self._buckets[buckets] is None or self._buckets[buckets].is_tombstone:
                numOfBuckets = numOfBuckets + 1
        return numOfBuckets

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All
        existing key/value pairs must remain in the new hash map, and all
        hash table links must be rehashed. First check that new_capacity
        is not less than the current number of elements in the hash map;
        if so, the method does nothing. If new_capacity is valid, make sure
        it is a prime number; if not, change it to the next highest prime
        number. You may use the methods _is_prime() and _next_prime() from the
        skeleton code.
        """
        # validate new capacity is not less than the current number of elements
        # in the hash map. If so, then do nothing
        if new_capacity <= self._size:
            return

        # Now check to see if new_capacity is a prime number.
        # If not, change it to the next highest prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Create a new hashmap for storing new values
        newHashMap = HashMap(new_capacity, self._hash_function)

        # Iterate through the array
        for buckets in self:
            newHashMap.put(buckets.key, buckets.value)

        # # Update the capacity to new_capacity
        # self._capacity = new_capacity
        # # Initialize a new Dynamic Array object
        # self._buckets = DynamicArray()
        #
        # # Iterate through the buckets and append it to the new DA object
        # for buckets in range(newHashMap._capacity):
        #     self._buckets.append(None)

        # Update the values
        self._capacity, self._buckets, self._size = newHashMap._capacity, newHashMap._buckets, newHashMap._size

    def get(self, key: str) -> object:
        """
        This method returns the value associated with the given key.
        If the key is not in the hashmap, the method returns None.
        """

        # If the key is not in the hash map, returns None
        if not self.contains_key(key):
            return None
        else:
            # Iterate through the buckets/array and see if it exists
            for buckets in self:
                    if buckets.key == key and not buckets.is_tombstone:
                        return buckets.value


    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, otherwise
        it returns False. An empty hash map does not contain any keys.
        """
        # Computes an index in the next two lines
        # hash = self._hash_function(key)
        # index = hash % self._capacity

        # Iterate through the buckets/array
        for buckets in self:
            # Does it match and is it not a tombstone?
            if buckets.key == key and not buckets.is_tombstone:
                return True
        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the
        hash map. If the key is not in the hash map, the method does nothing
        (No exception needs to be raised)
        """

        # Check to see if the key is not in the hashmap
        if not self.contains_key(key):
            return
        else:
            # Iterate through the buckets and see if the key matches
            # And is a tombstone
            for buckets in self:
                if buckets.key == key and not buckets.is_tombstone:
                    # Set is_tombstone to true when "removing"
                    buckets.is_tombstone = True
                    self._size = self._size - 1

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not
        change the underlying hash table capacity.
        """

        # Set the number of elements to 0
        self._size = 0
        # Set the number of buckets to 0
        # self._capacity = 0
        # Create a new empty dynamic array object
        self._buckets = DynamicArray()

        # Iterate through the array and clear it
        for buckets in range(self._capacity):
            self._buckets.append(None)

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains
        a tuple of a key/value pair stored in the hash map. The order of
        the keys in the dynamic array does not matter.
        """
        dynamicArray = DynamicArray()

        for nodes in self:
            # Iterate through the linked list and search for that key
            for buckets in self:
                # Copy the values of key and value
                key, value = buckets.key, buckets.value
                # Assign key and values as tuple
                kv = (key, value)
                # Assign the tuples to the end of the Dynamic Array
                dynamicArray.append(kv)

        return dynamicArray

    def __iter__(self):
        """
        This method enables the hash map to iterate across itself.
        Implement this method in a similar way to the example in the
        Exploration: Encapsulation and Iterators
        """
        # Same code from the Exploration: Encapsulation and Iterators
        self.index = 0
        return self

    def __next__(self):
        """
        This method will return the next item in the hash map, based on the
        current location of the iterator. Implement this method in a similar
        way to the example in the Exploration: Encapsulation and Iterators.
        You will need to only iterate over active items.
        """
        # Similar code from the Exploration: Encapsulation and Iterators
        # Only difference is that I had to search for tombstone as well
        try:
            # Initialize value
            value = None
            # Iterate to the next index to see if it's empty or is a tombstone
            while value is None or value.is_tombstone is True:
                # Get the value of that index
                value = self._buckets[self.index]
                self.index = self.index + 1
        except DynamicArrayException:
            raise StopIteration
        return value

    # ------------------- BASIC TESTING ---------------------------------------- #


if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)