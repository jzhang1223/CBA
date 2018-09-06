from enum import Enum

class ModelPeriod(Enum):
    monthly = 12
    quarterly = 4
    annually = 1

print(repr(ModelPeriod.monthly)) # gets <ModelPeriod.monthly: 12>
print ModelPeriod.monthly.name # gets monthly
print ModelPeriod.quarterly.value # gets 4
print ModelPeriod.annually # gets ModelPeriod.annually