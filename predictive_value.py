
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

has_problem = 0.1
no_problem = 1-has_problem


def prob_has_problem_tests_positive():
    return has_problem*sensitivity


def prob_has_problem_tests_negative():
    return has_problem*(1-sensitivity)


def prob_no_problem_tests_positive():
    return no_problem*(1-specificity)


def prob_no_problem_tests_negative():
    return no_problem*specificity


ppvs = pd.DataFrame()
specificity = 0.99
sensitivity = 0.00
for sens_raw in range(1, 101):
    sensitivity = (sens_raw * 0.01)
    ppv = prob_has_problem_tests_positive() / (prob_has_problem_tests_positive() + prob_no_problem_tests_positive())
    row = pd.DataFrame({"sensitivity": [sensitivity*100], "ppv": [ppv*100]})
    ppvs = ppvs.append(row, ignore_index=True)
plt.figure()

ax = sns.lineplot(x=ppvs["sensitivity"], y=ppvs["ppv"])
ax.set(xlabel="Sensitivity (%)", ylabel="Positive Predictive Value (%)")
plt.savefig('vary_sensitivity.png')

print(ppvs.head(20))
print(ppvs.tail(20))

ppvs = pd.DataFrame()
specificity = 0.00
sensitivity = 0.99
for spec_raw in range(1, 101):
    specificity = (spec_raw * 0.01)

    ppv = prob_has_problem_tests_positive() / (prob_has_problem_tests_positive() + prob_no_problem_tests_positive())
    row = pd.DataFrame({"specificity": [specificity*100], "ppv": [ppv*100]})
    ppvs = ppvs.append(row, ignore_index=True)
plt.figure()

ax = sns.lineplot(x=ppvs["specificity"], y=ppvs["ppv"])
ax.set(xlabel="Specificity (%)", ylabel="Positive Predictive Value (%)")
plt.savefig('vary_specificity.png')

print(ppvs.head(20))
print(ppvs.tail(20))



#
# ax = ppvs.plot(x="ppv", y="sensitivity", legend=False)
# ax2 = ax.twinx()
# ppvs.plot(x="ppv", y="specificity", ax=ax2, legend=False, color="r")
# ax.figure.legend()
# plt.show()
