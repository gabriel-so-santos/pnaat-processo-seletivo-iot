class CircularBuffer:
    def __init__(self, size):
        # Pre-allocate a fixed-size list to avoid dynamic resizing
        # Ensures O(1) insertion and predictable memory usage
        self.buffer = [None] * size

        # Maximum number of elements the buffer can hold
        self.size = size

        # Points to the next position to be written
        # Wraps around using modulo arithmetic
        self.index = 0

        # Tracks how many valid elements are currently stored
        # Never exceeds 'size'
        self.count = 0

    def push(self, value):
        # Insert the new value at the current index
        # If the buffer is full, this overwrites the oldest element
        self.buffer[self.index] = value

        # Move index forward and wrap around if needed
        self.index = (self.index + 1) % self.size

        # Increase count until it reaches the maximum size
        self.count = min(self.count + 1, self.size)

    def first(self):
        # Return the oldest element in the buffer
        # If empty, return None
        if self.count == 0:
            return None

        # The oldest element is located 'count' steps behind the current index
        # Use modulo to correctly wrap around the buffer
        return self.buffer[(self.index - self.count) % self.size]

    def last(self):
        # Return the most recently inserted element
        # If empty, return None
        if self.count == 0:
            return None

        # The last inserted element is one position behind the current index
        # (since index always points to the next write position)
        return self.buffer[(self.index - 1) % self.size]