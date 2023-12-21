import sys
import graphviz
import numpy as np

LOW_PULSE = 0
HIGH_PULSE = 1

class Module:
    def __init__(self, name, destinations):
        self.name = name
        self.destinations = destinations.copy()
        self.inputs = {}

    def receive_pulse(self, origin, pulse):
        return []

    # needs to be called after initialization
    def add_inputs(self, inputs):
        for input in inputs:
            self.inputs[input] = LOW_PULSE

    def send_pulse(self, pulse):
        pulses_sent = []
        for destination in self.destinations:
            pulses_sent.append((self.name, pulse, destination))
            # print(self.name, f"-{pulse}->", destination)
        return pulses_sent


class Broadcaster(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)

    def receive_pulse(self, origin, pulse):
        return self.send_pulse(pulse)


class FlipFlop(Module):
    def __init__(self, name, destinations):
        self.state = False
        super().__init__(name, destinations)

    def receive_pulse(self, origin, pulse):
        if pulse == LOW_PULSE:
            self.state = not self.state

            if self.state:
                return self.send_pulse(HIGH_PULSE)
            
            return self.send_pulse(LOW_PULSE)
        
        return []


class Conjunction(Module):
    def __init__(self, name, destinations):
        super().__init__(name, destinations)

    def receive_pulse(self, origin, pulse):
        self.inputs[origin] = pulse

        if all([input == HIGH_PULSE for input in self.inputs.values()]):
            return self.send_pulse(LOW_PULSE)
        
        return self.send_pulse(HIGH_PULSE)


class Solver:
    def __init__(self, file_path = "test.txt"):
        # read input file
        with open(file_path) as f:
            self.lines = f.readlines()

        self.modules = {}
        self.inputs = {}
        for line in self.lines:
            [name, destinations] = map(lambda x: x.strip(), line.split("->"))
            destinations = list(map(lambda x: x.strip(), destinations.split(",")))

            if name == 'broadcaster':
                # create broadcaster
                module = Broadcaster(name, destinations)
            elif name[0] == '%':
                # create flip flop
                name = name[1:]
                module = FlipFlop(name, destinations)
            else:
                # create conjunction
                name = name[1:]
                module = Conjunction(name, destinations)

            # add module to module list
            self.modules[name] = module
    
            # add destinations to input list
            # add module to destinations' input list
            for destination in destinations:
                if destination not in self.inputs:
                    self.inputs[destination] = []
                self.inputs[destination].append(name)

        # add inputs to modules
        for module, inputs in self.inputs.items():
            if module in self.modules:
                self.modules[module].add_inputs(inputs)

        self.high = 0
        self.low = 0
        self.rx = False
        
    # creates a graph of the circuit
    # red nodes are flip flops
    # blue nodes are conjunctions
    def graph(self):
        dot = graphviz.Digraph(comment='Graph')
        
        dot.node('broadcaster', 'broadcaster')
        # get modules from self.inputs instead of self.modules
        # because we are sure all of them are here
        # (rx is not in self.modules because it is not in the original module list)
        for module in self.inputs:
            if module in self.modules:
                color = 'red' if isinstance(self.modules[module], FlipFlop) else 'blue'
                dot.node(module, module, color=color, style='filled')
            else:
                dot.node(module, module)

        for module_name, module in self.modules.items():
            for destination in module.destinations:
                dot.edge(module_name, destination)

        dot.render('graph.gv', view=False)

    # sends low pulse to broadcaster
    def press_button(self):
        pulses = [(None, LOW_PULSE, 'broadcaster')]

        # pulses is a queue of (pulse, destination) to be processed
        for origin, pulse, module in pulses:
            if pulse == LOW_PULSE:
                self.low += 1
            else:
                self.high += 1

            # check if module exists
            if module in self.modules:
                # processs pulse in module and add new pulses to queue
                pulses += self.modules[module].receive_pulse(origin, pulse)

    def part1(self):
        for i in range(1000):
            self.press_button()
        return self.low * self.high

    # The broadcast module is connected to 4 flip-flops (branches)
    # To solve the puzzle we need to find a number in every branch — frequency of the counter
    # When all frequencies are found we calulcate the LCM
    # explained here how to get the frequency : https://www.reddit.com/r/adventofcode/comments/18mz6iy/2023_day_20_part_2_on_how_binary_counter_works/
    def part2(self):
        self.graph()
        
        binaries = [0b111100001011,
                    0b111110111011,
                    0b111100000111,
                    0b111110100011]

        return np.lcm.reduce(binaries)
    

if __name__ == '__main__':
    if len(sys.argv) > 2 and 1 <= int(sys.argv[1]) <= 2:

        if sys.argv[2] == 'test':
            solver = Solver("test.txt")
        elif sys.argv[2] == 'test2':
            solver = Solver("test2.txt")
        elif sys.argv[2] == '1':
            solver = Solver("input1.txt")
        elif sys.argv[2] == '2':
            solver = Solver("input2.txt")

        if sys.argv[1] == '1':
            print(solver.part1())
        else:
            print(solver.part2())
    else:
        print("Usage: python3 solver.py [1 / 2] [test / test2 / 1 / 2]")
        print("Filenames: test.txt\n\t   test2.txt\n\t   input1.txt\n\t   input2.txt")