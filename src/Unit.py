class Unit:
    """
    fixed - value is chosen for the cell
    value - number in cell
    set_values - set of possible numbers to put in cell
    """
    def __init__(self, dim, value=0):
        self.fixed = False
        self.dimension = dim
        self.value = value
        self.set_values = []
        # if cell is not empty -> fix it
        if self.value != 0:
            self.fixed = True
            self.set_values = [self.value]
        else:
            self.set_values = [i for i in range(1, self.dimension**2 + 1)]
    # if there are only one possible value -> value in cell is vixed
    def is_cell_fixed(self):
        return self.fixed
    def can_be_fixed(self):
        return len(self.set_values) == 1 and not self.fixed
    def is_cell_incorrect(self):
        return self.impossible()

    def fix_cell(self, value):
        self.fixed = True
        self.set_values = [value]
        self.value = value

    def set_cell(self, value):
        if (value != 0):
            self.fixed = True
            self.fix_cell(value)
        else:
            self.fixed = False
            #self.set_values = [i for i in range(1, self.dimension ** 2 + 1)]
            self.value = value

    def drop_possible(self, value):
        if value in self.set_values:
            self.set_values.remove(value)
        # if len(self.set_values) == 1:
        #     self.fix_cell(self.set_values[0])

    # no values can be put in cell
    def impossible(self):
        return len(self.set_values) == 0
    # check if ve can put value in cell
    def possible(self, value):
        return value in self.set_values

    def get_possible_values(self):
        return self.set_values
