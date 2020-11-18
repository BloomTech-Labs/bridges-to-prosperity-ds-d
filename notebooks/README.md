#Notebooks Clarification Points

## DATA
- The models created used the bridge B2P Dataset_2020.10.xlsx
- This data was clean and broken into two data frames
    - [cleaned_dataset.csv](https://raw.githubusercontent.com/Lambda-School-Labs/bridges-to-prosperity-ds-d/main/Data/cleaned_dataset.csv)
    - [df_cleaned_merge](https://raw.githubusercontent.com/Lambda-School-Labs/bridges-to-prosperity-ds-d/main/Data/df_cleaned_merge) 
- The nature of the data: highly imbalanced
- Main Classes working w/ Unknown, negative, positive
  ```python
  def process_target(df):
  data = df.copy()

  # Split the dataset:
  # Positives:
  positive = (
      (data['senior_engineering_review_conducted']=='Yes') & 
      (data['bridge_opportunity_stage'].isin(
      ['Complete', 'Prospecting', 'Confirmed', 'Under Construction']))
      )
  
  # Negatives:
  negative = (
      (data['senior_engineering_review_conducted']=='Yes') & 
      (data['bridge_opportunity_stage'].isin(['Rejected', 'Cancelled']))
      )
  

  # Unknown:
  unknown = data['senior_engineering_review_conducted'].isna()
``


## Model 
The model being used is a semi-supervised learning model 
 - The [latest deployment](https://lab28dsk.bridgestoprosperity.dev/) is based on this [google colabs notebook](https://colab.research.google.com/github/Lambda-School-Labs/bridges-to-prosperity-ds-d/blob/main/notebooks/b2p_d.ipynb)
    - main differences is new predict endpoint, Column name updates: engineer review update to good_site column
 - The [previous deployment](https://b2pmergefinal.bridgestoprosperity.dev/)  
- The models probabilities represent:
- Some bugs the model is currently facing are: 



## General Comments:
-  In order to make more certain predictions we need a certain amount of training data. In this instance we had access to an extrememly low amount of samples. This created a challenge for the team 
to properly report predicitons back. 
- The Possible directions: Having multiple tools in our Data Science tool bag we went to work. Long story short - our goal was to only "create" as much data as was needed to achieve the task set forth to us. Then once we were able to create an outcome from that data, 
ensure that the outcome was validated across multiple tools
- End Result: With any modeling done on such small sample of data, I am very weary to call these predicitions. It is possible to "predict" on a very small number of items. Although the end result of the prections can be very bias towards the data it has seen, and will not be as generalizable to future data. It could see one feature, that may not be as telling, 
and assume that leads to the end result.
