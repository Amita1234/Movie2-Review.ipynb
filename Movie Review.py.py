#!/usr/bin/env python
# coding: utf-8

# In[1]:


##Importing the required libraries

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')


# In[2]:


movies=pd.read_csv("/Users/pro/Downloads/Movie+Assignment+Data.csv")
movies.head()


# In[3]:


movies.shape


# In[4]:


movies.info()


# In[5]:


movies.describe()


# These numbers in the budget and gross are too big, compromising its readability. Let's convert the unit of the budget and gross columns from $ to million $ first.

# In[6]:


movies["Gross"]=movies["Gross"]/1000000
movies["budget"]=movies["budget"]/1000000
movies


# In[7]:


movies["profit"]=movies["Gross"]- movies["budget"]
movies


# In[8]:


movies=movies.sort_values(by="profit",ascending=False)


# In[9]:


movies.iloc[:10,:]


# In[10]:


#Plot profit vs budget

sns.jointplot("budget","profit",movies)
plt.show()


# In[11]:


movies.columns


# In[12]:


movies[movies["profit"]<0]


# movies["MetaCritic"]=movies["MetaCritic"]/10The General Audience and the Critics
# 
# You might have noticed the column `MetaCritic` in this dataset. This is a very popular website where an average score is determined through the scores given by the top-rated critics. Second, you also have another column `IMDb_rating` which tells you the IMDb rating of a movie. This rating is determined by taking the average of hundred-thousands of ratings from the general audience. 
# 
# As a part of this subtask, you are required to find out the highest rated movies which have been liked by critics and audiences alike.
# 1. Firstly you will notice that the `MetaCritic` score is on a scale of `100` whereas the `IMDb_rating` is on a scale of 10. First convert the `MetaCritic` column to a scale of 10.
# 2. Now, to find out the movies which have been liked by both critics and audiences alike and also have a high rating overall, you need to -
#     - Create a new column `Avg_rating` which will have the average of the `MetaCritic` and `Rating` columns
#     - Retain only the movies in which the absolute difference(using abs() function) between the `IMDb_rating` and `Metacritic` columns is less than 0.5. Refer to this link to know how abs() funtion works - https://www.geeksforgeeks.org/abs-in-python/ .
#     - Sort these values in a descending order of `Avg_rating` and retain only the movies with a rating equal to higher than `8` and store these movies in a new dataframe `UniversalAcclaim`.
#     

# In[13]:


movies["MetaCritic"]=movies["MetaCritic"]/10


# In[14]:


movies["Avg_rating"]=(movies["IMDb_rating"]+movies["MetaCritic"])/2


# In[15]:


movies


# In[16]:


df=movies[["Title","IMDb_rating","MetaCritic","Avg_rating"]]
df=df.loc[abs(df["IMDb_rating"]-df["MetaCritic"]<0.5)]


# In[17]:


df=df.sort_values(by="Avg_rating",ascending=False)
UniversalAcclaim=df.loc[df["Avg_rating"]>=8]
UniversalAcclaim


# You're a producer looking to make a blockbuster movie. There will primarily be three lead roles in your movie and you wish to cast the most popular actors for it. Now, since you don't want to take a risk, you will cast a trio which has already acted in together in a movie before. The metric that you've chosen to check the popularity is the Facebook likes of each of these actors.
# 
# The dataframe has three columns to help you out for the same, viz. actor_1_facebook_likes, actor_2_facebook_likes, and actor_3_facebook_likes. Your objective is to find the trios which has the most number of Facebook likes combined. That is, the sum of actor_1_facebook_likes, actor_2_facebook_likes and actor_3_facebook_likes should be maximum. Find out the top 5 popular trios, and output their names in a list.

# In[18]:


group=movies.pivot_table(values=["actor_1_facebook_likes","actor_2_facebook_likes","actor_3_facebook_likes"],
                  aggfunc="sum",index=["actor_1_name","actor_2_name","actor_3_name"])


# In[19]:


group


# In[20]:


group["Total likes"]=group["actor_1_facebook_likes"]+group["actor_2_facebook_likes"]+group["actor_3_facebook_likes"]


# In[21]:


group


# In[22]:


group=group.iloc[0:5,:]


# In[23]:


group


# In the previous subtask you found the popular trio based on the total number of facebook likes. Let's add a small condition to it and make sure that all three actors are popular. The condition is none of the three actors' Facebook likes should be less than half of the other two. For example, the following is a valid combo:
# 
# actor_1_facebook_likes: 70000
# actor_2_facebook_likes: 40000
# actor_3_facebook_likes: 50000
# But the below one is not:
# 
# actor_1_facebook_likes: 70000
# actor_2_facebook_likes: 40000
# actor_3_facebook_likes: 30000
# since in this case, actor_3_facebook_likes is 30000, which is less than half of actor_1_facebook_likes.
# 
# Having this condition ensures that you aren't getting any unpopular actor in your trio (since the total likes calculated in the previous question doesn't tell anything about the individual popularities of each actor in the trio.).
# 
# You can do a manual inspection of the top 5 popular trios you have found in the previous subtask and check how many of those trios satisfy this condition. Also, which is the most popular trio after applying the condition above?

# No. of trios that satisfy the above condition:
# 
# Most popular trio after applying the condition:

# Optional: Even though you are finding this out by a natural inspection of the dataframe, can you also achieve this through some if-else statements to incorporate this. You can try this out on your own time after you are done with the assignment.

# In[24]:


sorted([1,5,2])


# In[25]:


# Your answer here (optional)
j=0
for i in group["Total likes"]:
    temp=sorted([group.loc[j,"actor_1_facebook_likes"],group.loc[j,"actor_2_facebook_likes"],group.loc[j,"actor_3_facebook_likes"]])
    if temp[0]>= temp[1]/2 and temp[0]>=temp[2]/2 and temp[1]>=temp[2]/2:
        print(sorted([group.loc[j,"actor_1_name"],group.loc[j,"actor_2_name"],group.loc[j,"actor_3_name"]]))

    j=j+1


# Runtime Analysis
# There is a column named Runtime in the dataframe which primarily shows the length of the movie. It might be intersting to see how this variable this distributed. Plot a histogram or distplot of seaborn to find the Runtime range most of the movies fall into.

# In[26]:


plt.hist(movies["Runtime"])
plt.show()


# Checkpoint 3: Most of the movies appear to be sharply 2 hour-long.

# R-Rated Movies
# Although R rated movies are restricted movies for the under 18 age group, still there are vote counts from that age group. Among all the R rated movies that have been voted by the under-18 age group, find the top 10 movies that have the highest number of votes i.e.CVotesU18 from the movies dataframe. Store these in a dataframe named PopularR.

# In[27]:


movies.loc[movies["content_rating"]=="R"].sort_values(by="CVotesU18",ascending=False)[["Title","CVotesU18"]].head(10)


# Are these kids watching `Deadpool` a lot?

#  Demographic analysis
# If you take a look at the last columns in the dataframe, most of these are related to demographics of the voters (in the last subtask, i.e., 2.8, you made use one of these columns - CVotesU18). We also have three genre columns indicating the genres of a particular movie. We will extensively use these columns for the third and the final stage of our assignment wherein we will analyse the voters across all demographics and also see how these vary across various genres. So without further ado, let's get started with demographic analysis.

# Combine the Dataframe by Genres
# There are 3 columns in the dataframe - genre_1, genre_2, and genre_3. As a part of this subtask, you need to aggregate a few values over these 3 columns.
# 
# First create a new dataframe df_by_genre that contains genre_1, genre_2, and genre_3 and all the columns related to CVotes/Votes from the movies data frame. There are 47 columns to be extracted in total.
# Now, Add a column called cnt to the dataframe df_by_genre and initialize it to one. You will realise the use of this column by the end of this subtask.
# First group the dataframe df_by_genre by genre_1 and find the sum of all the numeric columns such as cnt, columns related to CVotes and Votes columns and store it in a dataframe df_by_g1.
# Perform the same operation for genre_2 and genre_3 and store it dataframes df_by_g2 and df_by_g3 respectively.
# Now that you have 3 dataframes performed by grouping over genre_1, genre_2, and genre_3 separately, it's time to combine them. For this, add the three dataframes and store it in a new dataframe df_add, so that the corresponding values of Votes/CVotes get added for each genre.There is a function called add() in pandas which lets you do this. You can refer to this link to see how this function works. https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.add.html
# The column cnt on aggregation has basically kept the track of the number of occurences of each genre.Subset the genres that have atleast 10 movies into a new dataframe genre_top10 based on the cnt column value.
# Now, take the mean of all the numeric columns by dividing them with the column value cnt and store it back to the same dataframe. We will be using this dataframe for further analysis in this task unless it is explicitly mentioned to use the dataframe movies.
# Since the number of votes can't be a fraction, type cast all the CVotes related columns to integers. Also, round off all the Votes related columns upto two digits after the decimal point.

# In[28]:


df_by_genre=movies.loc[:,"CVotes10":"VotesnUS"]
df_by_genre[["genre_1","genre_2","genre_3"]]=movies[["genre_1","genre_2","genre_3"]]


# In[29]:


df_by_genre


# In[30]:


df_by_genre["cnt"]=1


# In[31]:


df_by_genre[["genre_1","genre_2","genre_3"]]


# In[32]:


df_by_g1=df_by_genre.groupby("genre_1").aggregate(np.sum)
df_by_g2=df_by_genre.groupby("genre_2").aggregate(np.sum)
df_by_g3=df_by_genre.groupby("genre_3").aggregate(np.sum)


# In[33]:


df_by_g1


# In[34]:


df_by_g2


# In[35]:


df_add=df_by_g1.add(df_by_g2,fill_value=0)
df_add=df_add.add(df_by_g3,fill_value=0)
df_add


# In[36]:


genre_top_10=df_add.loc[df_add["cnt"]>10]


# In[37]:


genre_top_10


# In[38]:


genre_top_10.iloc[:,0:-1]=genre_top_10.iloc[:,0:-1].divide(genre_top_10["cnt"],axis=0)


# In[39]:


genre_top_10


# In[40]:


genre_top_10.loc[:,"VotesM":"VotesnUS"]=round(genre_top_10.loc[:,"VotesM":"VotesnUS"],2)


# In[41]:


genre_top_10[genre_top_10.loc[:,"CVotes10":"CVotesnUS"].columns]=genre_top_10[genre_top_10.loc[:,"CVotes10":"CVotesnUS"].columns].astype(int)


# In[42]:


genre_top_10


# If you take a look at the final dataframe that you have gotten, you will see that you now have the complete information about all the demographic (Votes- and CVotes-related) columns across the top 10 genres. We can use this dataset to extract exciting insights about the voters!

# Now let's derive some insights from this data frame. Make a bar chart plotting different genres vs cnt using seaborn.

# In[43]:


# Countplot for genres
sns.barplot(x=genre_top_10["cnt"],y=genre_top_10.index)
plt.show()


# Is the bar for Drama the tallest?

# Gender and Genre
# If you have closely looked at the Votes- and CVotes-related columns, you might have noticed the suffixes F and M indicating Female and Male. Since we have the vote counts for both males and females, across various age groups, let's now see how the popularity of genres vary between the two genders in the dataframe.
# 
# Make the first heatmap to see how the average number of votes of males is varying across the genres. Use seaborn heatmap for this analysis. The X-axis should contain the four age-groups for males, i.e., CVotesU18M,CVotes1829M, CVotes3044M, and CVotes45AM. The Y-axis will have the genres and the annotation in the heatmap tell the average number of votes for that age-male group.
# 
# Make the second heatmap to see how the average number of votes of females is varying across the genres. Use seaborn heatmap for this analysis. The X-axis should contain the four age-groups for females, i.e., CVotesU18F,CVotes1829F, CVotes3044F, and CVotes45AF. The Y-axis will have the genres and the annotation in the heatmap tell the average number of votes for that age-female group.
# 
# Make sure that you plot these heatmaps side by side using subplots so that you can easily compare the two genders and derive insights.
# 
# Write your any three inferences from this plot. You can make use of the previous bar plot also here for better insights. Refer to this link- https://seaborn.pydata.org/generated/seaborn.heatmap.html. You might have to plot something similar to the fifth chart in this page (You have to plot two such heatmaps side by side).
# 
# Repeat subtasks 1 to 4, but now instead of taking the CVotes-related columns, you need to do the same process for the Votes-related columns. These heatmaps will show you how the two genders have rated movies across various genres.
# 
# You might need the below link for formatting your heatmap. https://stackoverflow.com/questions/56942670/matplotlib-seaborn-first-and-last-row-cut-in-half-of-heatmap-plot
# 
# Note : Use genre_top10 dataframe for this subtask

# In[44]:


plt.figure(figsize=(20,10))
plt.subplot(1,2,1)
ax=sns.heatmap(genre_top_10[["CVotesU18M","CVotes1829M","CVotes3044M","CVotes45AM"]],annot=True,cmap="coolwarm")
plt.subplot(1,2,2)

ax=sns.heatmap(genre_top_10[["CVotesU18F","CVotes1829F","CVotes3044F","CVotes45AF"]],annot=True,cmap="coolwarm")
plt.show()


# **`Inferences:`** A few inferences that can be seen from the heatmap above is that males have voted more than females, and Sci-Fi appears to be most popular among the 18-29 age group irrespective of their gender. What more can you infer from the two heatmaps that you have plotted? Write your three inferences/observations below:
# - Inference 1: Genre romance has got the least number of votes among any age group of males, but there is no such pattern among the females
# - Inference 2:Action seems to be the more popular genre among the under 18 males, and Animation appears to be the most popular genre among under 18 females.
# - Inference 3: 18-29 age group seems to be most actively voting for any genre irrespective of gender

# In[ ]:




