class CircularBuffer:
    """
    Fixed-size circular buffer implementation.

    Stores elements in a ring structure where new insertions
    overwrite the oldest elements when capacity is reached.

    Provides O(1) insertion and O(1) access to first/last elements.
    """

    def __init__(self, size: int):
        """
        Initialize the circular buffer.

        Args:
            size (int): Maximum number of elements the buffer can store.
        """
        # Pre-allocate fixed-size storage to ensure O(1) behavior
        self.buffer = [None] * size

        # Maximum capacity of the buffer
        self.size = size

        # Index of the next insertion position (wraps around)
        self.index = 0

        # Number of valid elements currently stored
        self.count = 0

    def push(self, value):
        """
        Insert a new value into the buffer.
        If the buffer is full, the oldest value is overwritten.
        """
        # Store value at current write position
        self.buffer[self.index] = value

        # Advance index with circular wrap-around
        self.index = (self.index + 1) % self.size

        # Increase count up to maximum capacity
        self.count = min(self.count + 1, self.size)

    def first(self):
        """
        Return the oldest element in the buffer (None if buffer is empty).
        """
        if self.count == 0:
            return None

        # Oldest element is 'count' positions behind current index
        return self.buffer[(self.index - self.count) % self.size]

    def last(self):
        """
        Return the most recently inserted element (None if buffer is empty).
        """
        if self.count == 0:
            return None

        # Last element is just before the current insertion index
        return self.buffer[(self.index - 1) % self.size]