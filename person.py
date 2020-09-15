from poisson_randomizer import PoissonRandomizer
import numpy as np


class Person:
    """Person object.
    """

    def __init__(self, deseaseStage, pSymptomatic, tSymptomatic, tRecovery):
        self.PoissonRandomizer = PoissonRandomizer()
        self.PSymptomatic = pSymptomatic
        self.TSymptomatic = tSymptomatic
        self.TRecovery = tRecovery

        self.Stage = deseaseStage
        if deseaseStage == "I":
            self.Infect(0)

        self.IsInfective = False
        self.IsSymptomatic = False
        self.ShouldQueue = False
        self.IsQueued = False
        self.IsIsolated = False

    def Advance(self, t):
        if self.Stage == "I":
            if (not self.IsInfective) and t >= self.InfectiveAt:
                self.IsInfective = True
            if self.WillShowSymptomps and (not self.IsSymptomatic) and t >= self.SymptomaticAt:
                self.IsSymptomatic = True
                self.WillShowSymptomps = None
                if (not self.ShouldQueue):
                    (self.ShouldQueue) = True
            if t >= self.RecoverAt:
                self.Recover(t)

    def Infect(self, t):
        self.Stage = "I"
        self.InfectiveAt = t+0
        self.RecoverAt = t+self.PoissonRandomizer.fromMean(self.TRecovery)

        self.WillShowSymptomps = np.random.rand() <= self.PSymptomatic
        if self.WillShowSymptomps:
            self.SymptomaticAt = t + \
                self.PoissonRandomizer.fromMean(self.TSymptomatic)

    def Queue(self, t):
        self.ShouldQueue = False
        self.IsQueued = True
        self.QueuedAt = t

    def Recover(self, t):
        self.Stage = "R"
        self.IsInfective = None
        self.IsSymptomatic = None
        self.IsQueued = None
        self.IsIsolated = None

    def Test(self, t):
        if self.Stage == "I":
            # TODO: Delay with time to get result
            self.IsInfective = False  # Can't infect since isolated
            self.IsQueued = False
            self.IsIsolated = True
