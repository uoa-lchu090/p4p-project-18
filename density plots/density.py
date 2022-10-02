import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = "Mansfield" # JL, Mansfield, Mozilla
models = ['Model_Baseline', 'Model_All','Model_MAN_only','Model_MZ_only','Model_no_JL']

# example = pd.read_csv("finetuned model results/Model_All/JL_test_results.csv")

# # seaborn density plot
# sns.distplot(example['MER'], hist=False, kde=True,
#              kde_kws = {'linewidth': 3})


for model in models:
    data = pd.read_csv("finetuned model results/" + model + "/" + dataset + "_test_results.csv")
    sns.distplot(data['MER'], hist=False, kde=True,
              kde_kws = {'linewidth': 1},
              label = model)




# Add labels
plt.legend(prop={'size': 8}, title = 'Model')
plt.title('Density plot of MER on the ' + dataset + " dataset with mutiple models")
plt.xlabel('MER score')
plt.ylabel('Density')
plt.savefig(dataset + '_density.png', dpi = 300)

plt.show()