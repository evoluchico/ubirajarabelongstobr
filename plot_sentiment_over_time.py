from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

sns.set('talk')
sns.set_style('ticks')

def load_data():
	infile = 'Date-Time-TweetSentiment.xlsx'
	df = pd.read_excel(infile)

	del df['Unnamed: 0']
	del df['Unnamed: 1']

	df['datetime'] = pd.to_datetime(df['Tweet_date&time'])
	del df['Tweet_date&time']

	df['date'] = df['datetime'].apply(lambda x: x.date)
	del df['datetime']

	return df

def plot(df):
	# Daily
	sentiment_mean = df.groupby('date').mean()['Tweet_Sentiment_Value']
	sentiment_std = df.groupby('date').std()['Tweet_Sentiment_Value']

	# Weekly
	x = sentiment_mean.rolling(7).mean().index
	y = sentiment_mean.rolling(7).mean().values
	error = sentiment_std.rolling(7).std().values

	plt.figure(figsize=(12,4))
	plt.axhline(0, linestyle='-', c='silver', alpha=0.75, lw=1)
	plt.plot(x, y, 'k-')
	plt.fill_between(x, y-error, y+error, color='cornflowerblue')

	plt.xlim(x[0], pd.to_datetime('2023-04-01'))
	plt.ylabel('Tweet sentiment')

	plt.tight_layout()
	plt.savefig('tweet_sentiment_over_time.png', dpi=150)
	plt.show()

def fig1(df):
	df2 = df.groupby("date").count() 
	df2.columns = ['Tweet count']	

	date_annotations = ["2020-12-13", '''In press article on “Ubirajara jubatus” appears on the journal Cretaceous Research. [1]''',
	"2020-12-13", '''The hashtag #UbirajaraBelongstoBR is first used on Twitter by Aline M. Ghilardi. [2]''',
	"2020-12-14", '''The Brazilian Society of Palaeontology contacts Cretaceous Research.''',
	"2020-12-22", '''First report on the controversy by international media (National Geographic). [3]''',
	"2020-12-24", '''Article temporarily removed by Cretaceous Research.''',
	"2021-09-08", '''SMNK informs the Brazilian Society of Palaeontology that it will not repatriate the fossil. The Brazilian Society of Palaeontology informs its members.''',
	"2021-09-09", '''SMNK releases a statement on Instagram refusing repatriation of “Ubirajara jubatus”.''',
	"2021-09-10", '''A petition is created at Change.org. [4]''',
	"2021-09-22", '''Article withdrawn by Cretaceous Research.''',
	"2021-09-28", '''SMNK Instagram account is deactivated.''',
	"2021-09-29", '''Article in the journal Science reveals that the dinosaur was imported to Germany by fossil dealers in 2006 and purchased by SMNK in 2009. [5]''',
	"2021-10-15", '''The USA repatriates 35 fossil spiders to Brazil. [6]''',
	"2022-02-08", '''Belgium repatriates a pterosaur to Brazil. [7]''',
	"2022-07-19", '''Germany announces that “Ubirajara jubatus” will be repatriated to Brazil. [8]''']
	date_annotations = pd.DataFrame({'date':pd.to_datetime(date_annotations[::2]),'annot':date_annotations[1::2]})

	df2.plot()
	plt.text(x,y,text)

