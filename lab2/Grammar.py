class Grammar():
    def __init__(self,
                 VN=['S', 'D', 'R'],
                 VT=['a', 'b', 'c', 'd', 'f'],
                 P={
                    'S': ['aS', 'bD', 'fR'],
                    'D': ['cD', 'dR', 'd'],
                    'R': ['bR', 'f']
                }):
        self.VN = VN
        self.VT = VT
        self.P = P

    def print1(self):
        print(self.VN)
        print(self.VT)
        print(self.P)

    def classify(self):
        is_type_3 = True
        is_type_2 = True

        for left, productions in self.P.items():
            if len(left) != 1:
                # this violates rules for type 2 and 3 (only 1 non-terminal on the left)
                is_type_2 = False
                is_type_3 = False
                break

            for production in productions:
                if not production:
                    # empty production is fine for type 2 but not for 3
                    is_type_3 = False
                elif len(production) == 2 and production[1] in self.VN:
                    # A -> aB  -  this is okay for type 3
                    continue
                elif len(production) == 1 and production[0] in self.VT:
                    # A -> a  -  also okay for type 3
                    continue
                else:
                    # failing both of the previous 2 checks means this isn't a type 3 grammar
                    is_type_3 = False

        if is_type_3:
            return 3  # regular
        elif is_type_2:
            return 2  # context free grammar
        else:
            for left, productions in self.P.items():
                for production in productions:
                    if len(left) <= len(production):
                        pass
                    else:
                        return 0 # recursively enumerable grammar
            return 1  # context sensivive grammar

