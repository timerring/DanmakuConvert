# Copyright (c) 2025 DanmakuConvert


class DanmakuArray:
    def __init__(self, solution_x=1920, solution_y=1080, font_size=38):
        """
        Args:
            solution_x (int): resolution_x
            solution_y (int): resolution_y
            font_size (int): font_size
        """
        self.solution_x = solution_x
        self.solution_y = solution_y
        self.font_size = font_size
        self.rows = int(solution_y / font_size)
        self.time_length_array = [[-1, 0] for _ in range(self.rows)]

    def set_time_length(self, row, time, length):
        """Set time and length for a row"""
        if 0 <= row < self.rows:
            self.time_length_array[row] = [time, length]
        else:
            raise IndexError("Array index out of range")

    def get_time(self, row):
        """Get time for a row"""
        if 0 <= row < self.rows:
            return self.time_length_array[row][0]
        else:
            raise IndexError("Array index out of range")

    def get_length(self, row):
        """Get length for a row"""
        if 0 <= row < self.rows:
            return self.time_length_array[row][1]
        else:
            raise IndexError("Array index out of range")
