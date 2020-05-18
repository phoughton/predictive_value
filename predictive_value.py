
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


class PVCalculator:

    def __init__(self, has_problem, the_sensitivity, the_specificity):
        self.has_problem = has_problem
        self.no_problem = 1 - has_problem
        self.sensitivity = the_sensitivity
        self.specificity = the_specificity

    def prob_has_problem_tests_positive(self):
        return self.has_problem*self.sensitivity

    def prob_has_problem_tests_negative(self):
        return self.has_problem*(1-self.sensitivity)

    def prob_no_problem_tests_positive(self):
        return self.no_problem*(1-self.specificity)

    def prob_no_problem_tests_negative(self):
        return self.no_problem*self.specificity

    def ppv(self):
        return self.prob_has_problem_tests_positive() / \
               (self.prob_has_problem_tests_positive() + self.prob_no_problem_tests_positive())

    def npv(self):
        return self.prob_no_problem_tests_negative() / \
               (self.prob_has_problem_tests_negative() + self.prob_no_problem_tests_negative())


def draw_graph(dataframe, metric_type, y_name):
    plt.figure()
    sns.set(font_scale=1.2)
    sns.set_style("whitegrid", {'axes.grid': False})
    sns.set_context("notebook", font_scale=1.2, rc={"lines.linewidth": 3})

    ax = sns.lineplot(x=dataframe[metric_type], y=dataframe[y_name])
    ax.set(xlabel=f"{metric_type.title()} (%)", ylabel=f"{y_name.title()} (%)")
    plt.ylim(0, 100)
    plt.xlim(0, 100)
    plt.savefig(f"{y_name.replace(' ', '_')}__vary_{metric_type.replace(' ', '_')}.svg",  format="svg")


prevalence = 0.05

pvs = pd.DataFrame()
specificity = 0.999
for sens_raw in range(1, 1001):
    sensitivity = (sens_raw * 0.001)
    ppv = PVCalculator(prevalence, sensitivity, specificity).ppv()
    npv = PVCalculator(prevalence, sensitivity, specificity).npv()
    row = pd.DataFrame({"sensitivity": [sensitivity*100], "Positive Predictive Value": [ppv*100], "Negative Predictive Value": [npv*100]})
    pvs = pvs.append(row, ignore_index=True)

draw_graph(pvs, "sensitivity", "Positive Predictive Value")
draw_graph(pvs, "sensitivity", "Negative Predictive Value")


pvs = pd.DataFrame()
sensitivity = 0.999
for spec_raw in range(1, 1001):
    specificity = (spec_raw * 0.001)
    ppv = PVCalculator(prevalence, sensitivity, specificity).ppv()
    npv = PVCalculator(prevalence, sensitivity, specificity).npv()
    row = pd.DataFrame({"specificity": [specificity*100], "Positive Predictive Value": [ppv*100], "Negative Predictive Value": [npv*100]})
    pvs = pvs.append(row, ignore_index=True)

draw_graph(pvs, "specificity", "Positive Predictive Value")
draw_graph(pvs, "specificity", "Negative Predictive Value")
