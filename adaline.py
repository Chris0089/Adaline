import random
import csv

INPUTFILE = 'input-values.txt'
DESIREDFILE = 'desired-values.txt'
ETA = 0.1
BOTTOM_LIMIT = -1
TOP_LIMIT = 1


class DataAccessObject:
    inputData = []
    desiredOutput = []

    def __init__(self):
        self.get_data()

    def get_data(self):
        file = open(INPUTFILE, "r")
        # next(file)
        for line in file:
            fields = line.split(" ")
            size = len(fields)
            if not self.inputData:
                for value in range(0, size):
                    self.inputData.append([])
            for value in range(0, size):
                self.inputData[value].append(float(fields[value]))
        file = open(DESIREDFILE, "r")
        # next(file)
        for line in file:
            fields = line.split(" ")
            size = len(fields)
            if not self.desiredOutput:
                for value in range(0, size):
                    self.desiredOutput.append([])
            for value in range(0, size):
                self.desiredOutput[value].append(float(fields[value]))


class Perceptron(DataAccessObject):
    inputData = []
    inputQuantity = None
    inputSize = None
    weightData = []
    threshold = []  # bias
    output = []
    desiredOutput = []
    desiredColumns = None
    desiredRows = None
    v = []
    summation = []
    iteration = 0

    def __init__(self):
        self.inputData = DataAccessObject.inputData.copy()
        self.desiredOutput = DataAccessObject.desiredOutput.copy()
        self.inputQuantity = len(self.inputData)
        self.inputSize = len(self.inputData[0])
        self.desiredColumns=len(self.desiredOutput)
        self.desiredRows = len(self.desiredOutput[0])
        self.generate_random_values()
        self.main_algorithm()

    def generate_random_values(self):
        for column in range(0, self.desiredColumns):
            self.weightData.append([])
            self.threshold.append([])
            for value in range(0, self.inputQuantity):
                self.weightData[column].append([])
            for value in range(0, self.inputQuantity):
                for inputSize in range(0, self.inputSize):
                    self.weightData[column][value].append(random.uniform(BOTTOM_LIMIT, TOP_LIMIT))
            for size in range(0, self.inputSize):
                self.threshold[column].append(random.uniform(BOTTOM_LIMIT, TOP_LIMIT))

    def calculate_output(self):
        self.output = []
        self.summation = []
        self.v = []
        for column in range(0, self.desiredColumns):
            self.output.append([])
            self.summation.append([])
            self.v.append([])
            for row in range(0, self.inputSize):
                self.summation[column].append(0)
                self.v[column].append(0)
                for columnInput in range(0,self.inputQuantity):
                    self.summation[column][row] += \
                        self.inputData[columnInput][row] * self.weightData[column][columnInput][row]
                self.v[column][row] = self.summation[column][row] + self.threshold[column][row] #changed, summed bias
                self.output[column].append(self.activation_function(self.v[column][row]))
        self.iteration += 1

    def activation_function(self, value):
        if value <= 0:
            return 0.0
        else:
            return 1.0

    def is_the_desired_output(self):
        if self.output == self.desiredOutput:
            return True
        else:
            return False

    def training(self):
        for column in range(0, self.desiredColumns):
            for row in range(0,self.inputSize):
                if self.desiredOutput[column][row] != self.output[column][row]:
                    error = self.desiredOutput[column][row] - self.output[column][row]
                    self.threshold[column][row] = self.threshold[column][row] + (ETA * error)
                    for columnInput in range(0, self.inputQuantity):
                        self.weightData[column][columnInput][row] = self.weightData[column][columnInput][row] +\
                                                       (ETA * error * self.inputData[columnInput][row])

    def main_algorithm(self):
        self.calculate_output()
        self.print_data()
        while not self.is_the_desired_output():
            print(self.iteration)
            self.training()
            self.calculate_output()
            self.print_data()
        print("Finished")

    def print_data(self):
        print("Iteraciones = " + str(self.iteration))
        print("ETA = " + str(ETA))
        print("Salida deseada:")
        print(self.desiredOutput)
        print("Salidas:")
        print(self.output)


dao = DataAccessObject()
perceptron = Perceptron()

