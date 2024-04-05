class Unit:
    """
    fixed - value is chosen for the cell
    value - number in cell
    set_values - set of possible numbers to put in cell
    """
    def __init__(self, value=0):
        self.fixed = False
        self.value = value
        self.set_values = []
        # if cell is not empty -> fix it
        if self.value != 0:
            self.set_values.append(value)
            self.fixed = True
        else:
            self.set_values = [i for i in range(1, 10)]
    # if there are only one possible value -> value in cell is vixed
    def check_fixed(self):
        self.fixed = len(self.set_values)
        return len(self.set_values) == 1

    def drop_possible(self, value):
        self.set_values.remove(value)
    # no values can be put in cell
    def impossible(self):
        return len(self.set_values) == 0
    # check if ve can put value in cell
    def possible(self, value):
        return value in self.set_values
