import numpy as np
import statsmodels.api as sm
from scipy.stats import bernoulli
from statsmodels.base.model import GenericLikelihoodModel
from matplotlib import pyplot as plt

# Define custom model
class CustomModel(GenericLikelihoodModel):
    
    def __init__(self, endog, exog, p0, **kwds):
        self.p0 = p0
        super().__init__(endog, exog, **kwds)
    
    def loglike(self, params):
        h = params[0]
        e = self.exog[:, 0]
        p_0 = self.p0(h, e)
        p_1 = 1 - p_0
        ll = self.endog * np.log(p_1) + (1 - self.endog) * np.log(p_0)
        return ll.sum()




def p0_custom(h, e):
    return 3 / 4 * np.exp(-(e / h)**2)


def estimador(amplitudes,resultados):
    exog = np.array(amplitudes).reshape(-1, 1)
    endog = resultados
    model = CustomModel(endog, exog, p0_custom)
    result = model.fit(start_params=np.array([1]))    
    #guardo la historia de cada iteración
    return result

