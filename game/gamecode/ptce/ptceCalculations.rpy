init -1 python:

    class LinearCalculation:
        def __init__(self, x=0, flatMultiplier=1, flatBonus=0):
            self.x = x
            self.flatMultiplier = flatMultiplier
            self.flatBonus = flatBonus
        
        def calculate(self):
            return self.flatMultiplier * self.x + self.flatBonus

        def __str__(self):
            return "<{1}*{0} + {2}>".format(self.x, self.flatMultiplier, self.flatBonus)
        
    class QuadraticCalculation:
        def __init__(self, x=0, quadraticMultiplier=1, flatMultiplier=0, flatBonus=0):
            self.x = x
            self.flatMultiplier = flatMultiplier
            self.flatBonus = flatBonus
            self.quadraticMultiplier = quadraticMultiplier
        
        def calculate(self):
            return self.quadraticMultiplier * math.pow(x, 2) + self.flatMultiplier * self.x + self.flatBonus

        def __str__(self):
            return "<{1}*{0}² + {2}*{0} + {3}>".format(self.x, self.quadraticMultiplier, self.flatMultiplier, self.flatBonus)
    
    class RootCalculation:
        def __init__(self, x=0, rootMultiplier=1, flatMultiplier=0, flatBonus=0):
            self.x = x
            self.flatMultiplier = flatMultiplier
            self.flatBonus = flatBonus
            self.rootMultiplier = rootMultiplier
        
        def calculate(self):
            return self.rootMultiplier * math.sqrt(x) + self.flatMultiplier * self.x + self.flatBonus

        def __str__(self):
            return "<{1}*√{0} + {2}*{0} + {3}>".format(self.x, self.rootMultiplier, self.flatMultiplier, self.flatBonus)
    
    class InverseQuadraticCalculation:
        def __init__(self, x=0, quadraticMultiplier=1, flatMultiplier=0, flatBonus=0, dividend=1, flatOverallBonus=0):
            self.x = x
            self.flatMultiplier = flatMultiplier
            self.flatBonus = flatBonus
            self.quadraticMultiplier = quadraticMultiplier
            self.dividend = dividend
            self.flatOverallBonus = flatOverallBonus
        
        def calculate(self):
            return self.dividend / (self.quadraticMultiplier * math.pow(x, 2) + self.flatMultiplier * self.x + self.flatBonus) + self.flatOverallBonus

        def __str__(self):
            return "<{4} / ({1}*{0}² + {2}*{0} + {3}) + {5}>".format(self.x, self.quadraticMultiplier, self.flatMultiplier, self.flatBonus, self.dividend, self.flatOverallBonus)
    
    class InverseRootCalculation:
        def __init__(self, x=0, rootMultiplier=1, flatMultiplier=0, flatBonus=0, dividend=1, flatOverallBonus=0):
            self.x = x
            self.flatMultiplier = flatMultiplier
            self.flatBonus = flatBonus
            self.rootMultiplier = rootMultiplier
            self.dividend = dividend
            self.flatOverallBonus = flatOverallBonus
        
        def calculate(self):
            return self.dividend / (self.rootMultiplier * math.sqrt(x) + self.flatMultiplier * self.x + self.flatBonus) + self.flatOverallBonus

        def __str__(self):
            return "<{4} / ({1}*√{0} + {2}*{0} + {3}) + {5}>".format(self.x, self.quadraticMultiplier, self.flatMultiplier, self.flatBonus, self.dividend, self.flatOverallBonus)
    
    class RandomCalculation:
        def __init__(self, rngType, minimum=0, maximum=1):
            self.rngType = rngType
            self.minimum = minimum
            self.maximum = maximum
        
        def calculate(self):
            if self.rngType == "integer":
                return renpy.random.randint(self.minimum, self.maximum)
            
            return renpy.random.random() * (self.maximum - self.minimum) + self.minimum
        
        def __str__(self):
            return "<{0} between ({1}..{2})".format(self.rngType, self.minimum, self.maximum)
    
    def getCalculationForTarget(calculation, target):
        if "rngType" in calculation.keys():
            return getCalculationForValue(calculation, 0)
        
        stat = target.stats.__dict__.get(calculation.get("stat"))
        return getCalculationForValue(calculation, stat)

    
    def getCalculationForValue(calculation, value):
        if "rngType" in calculation.keys():
            return RandomCalculation(calculation.get("rngType"), calculation.get("minimum"), calculation.get("maximum"))

        if calculation.get("calculationType") == "linear":
            return LinearCalculation(value, calculation.get("flatMultiplier"), calculation.get("flatBonus"))
        
        if calculation.get("calculationType") == "quadratic":
            return QuadraticCalculation(value, calculation.get("quadraticMultiplier"), calculation.get("flatMultiplier"), calculation.get("flatBonus"))
        
        if calculation.get("calculationType") == "squareRoot":
            return RootCalculation(value, calculation.get("rootMultiplier"), calculation.get("flatMultiplier"), calculation.get("flatBonus"))
        
        if calculation.get("calculationType") == "inverseQuadratic":
            return InverseQuadraticCalculation(value, calculation.get("quadraticMultiplier"), calculation.get("flatMultiplier"), calculation.get("flatBonus"), calculation.get("dividend"), calculation.get("flatOverallBonus"))
        
        if calculation.get("calculationType") == "inverseSquareRoot":
            return InverseRootCalculation(value, calculation.get("rootMultiplier"), calculation.get("flatMultiplier"), calculation.get("flatBonus"),  calculation.get("dividend"), calculation.get("flatOverallBonus"))
        
        raise Exception("Can't determine calculation type for calculation '{0}'".format(calculation))
    
    def getAllCalculationsForTarget(calculations, target):
        return map(lambda calc: getCalculationForTarget(calc, target), calculations)
    
    def calculateAll(calculations, target):
        return sum(map(lambda calc: calc.calculate(), getAllCalculationsForTarget(calculations, target)))