__author__ = 'DQZ'

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pandasql import *
from sqlalchemy import create_engine

####Importing datasets.
engine = create_engine('sqlite:///:memory:')

df1 = pd.read_csv("./data/Master.csv",sep=",")
df1.to_sql("Master",engine)

df2 = pd.read_csv("./data/Salaries.csv",sep=",")
df2.to_sql("Salaries",engine)

df3 = pd.read_csv("./data/Teams.csv",sep=",")
df3.to_sql("Teams",engine)

with engine.connect() as conn:
    with conn.begin():
        df_Master = pd.read_sql_table('Master', conn)
        df_Salaries= pd.read_sql_table('Salaries',conn)
        df_Teams = pd.read_sql_table('Teams',conn)

####Joining the salary ad mater dataframes
q = """
    SELECT
        m.playerID
        , s.salary
        , m.nameFirst
        , m.nameLast

    FROM
        df_Master m
    INNER JOIN
        df_Salaries s
            on m.playerID = s.playerID
    ORDER BY
        s.playerID
    ;
    """

joined = sqldf(q,globals())

joined["cummulativeSalary"] = joined.groupby("playerID").cumsum()

print joined.head()


####Ron Gant's salary

Ron_Gant_df = joined[(joined.nameFirst =="Ron") & (joined.nameLast =="Gant")][["salary",
                                                                               "cummulativeSalary"]].reset_index(drop= True)
# print Ron_Gant_df

#####Curtis Granderson and Reggie Sanders

Curtis_Granderson_df = joined[(joined.nameFirst == "Curtis") & (joined.nameLast == "Granderson")][["salary",
                                                                               "cummulativeSalary"]].reset_index(drop= True)
print Curtis_Granderson_df

Reggie_Sanders_df = joined[(joined.nameFirst == "Reggie") & (joined.nameLast == "Sanders")][["salary",
                                                                               "cummulativeSalary"]].reset_index(drop= True)
print Reggie_Sanders_df

####Cumulative Salaries

Ron_Gant_df.cummulativeSalary.plot(title = "Cummulative Salary of Ron Gant")
plt.show()

Curtis_Granderson_df.cummulativeSalary.plot(title = "Cummulative Salary of Curtis_Granderson")
plt.show()

Reggie_Sanders_df.cummulativeSalary.plot(title = "Cummulative Salary of Reggie Sanders")
plt.show()

###New York Yankees with over 90 wins
####Solution Based on SQL Query
q = """
    SELECT
        t.W
        , t.name

    FROM
        df_Teams t
    WHERE
        t.W > 90
    AND
        t.name == 'New York Yankees'

    """

df_NYY_90_a = sqldf(q,globals())
print("The number of times New York Yankees had over 90 wins = ",df_NYY_90_a.shape[0])

###Solution Based on Pandas abilities
df_NYY_90_b1 = df_Teams[["W","name"]].query('W > 90 and name == "New York Yankees"')
#pandas query
print("The number of times New York Yankees had over 90 wins = ",df_NYY_90_b1.shape[0])

df_NYY_90_b2 = df_Teams.loc[(df_Teams.W > 90) & (df_Teams.name == 'New York Yankees')]
# pandas subsetting
print("The number of times New York Yankees had over 90 wins = ",df_NYY_90_b2.shape[0])

###Team with the highest attendence 2010
df_maxAttend = df_Teams[df_Teams["yearID"] == 2010]
print("Team with the highest attendence in 2010:",
      df_maxAttend[df_maxAttend["attendance"] == df_maxAttend.attendance.max()].name)

###Average Attendence for San Francisco Giants in 1990s
df_SFG = df_Teams[(df_Teams["name"] == "San Francisco Giants") & (df_Teams["yearID"] >= 1990) & \
                                                     (df_Teams["yearID"] <= 1999)]
print("Average Attendence for SFG in 90s: ",df_SFG.attendance.mean())

###All plots combined!
myplot1 = Ron_Gant_df.cummulativeSalary.plot()
myplot2 = Curtis_Granderson_df.cummulativeSalary.plot()
myplot3 = Reggie_Sanders_df.cummulativeSalary.plot(title="Cummulative Salariers of R. Gant, C. Granderson, and R. Sanders")

plt.show()
