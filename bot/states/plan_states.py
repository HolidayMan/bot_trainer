from enum import Enum

class PlanStates(Enum):
    S_NEWCHOOSETYPE = "planstates.newchoosetype"
    S_NEWENTERTITLE = "planstates.newentertitle"
    S_EDITCHOOSETYPE = "planstates.editchoosetype"
    S_EDITCHOOSEPLAN = "planstates.editchooseplan"
    S_EDITPLAN = "planstate.editplan"