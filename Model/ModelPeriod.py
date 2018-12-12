from enum import Enum

class ModelPeriod(Enum):
    annual = 1
    quarterly = 4


#print(repr(ModelPeriod.monthly)) # gets <ModelPeriod.monthly: 12>
#print ModelPeriod.monthly.name # gets monthly
#print ModelPeriod.quarterly.value # gets 4
#print ModelPeriod.annually # gets ModelPeriod.annually
