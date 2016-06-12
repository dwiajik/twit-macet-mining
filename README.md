# Python mining script for TwitMacet
This repository contains text mining scripts written in Python3 for TwitMacet project hosted in https://twitmacet.dwiajik.com. This readme will explain some of the files in the repository.


**chunk.py**
*Parameter 1: text file name to be analyzed*
This script will do:
- Analyze the text file line by line
- Learn from pos\_tagged\_corpus
- Tag every word with POS tag
- Detect noun phrases and adjective phrases
- Print them line by line

**classify.py**
*Parameter 1: text file name to be analyzed and classified*
*Parameter 2: output CSV file, write without the extension*
This script will do:
- Build classification model (Naive Bayes, SVM, Decision Tree) from tweets_corpus using sklearn library
- Read file stated in parameter 1 line by line
- Classify each tweet on each line
- Save the result in CSV format

**classify\_evaluate\_ten\_folds.py**
*Parameter 1: "balance"/"imbalance" -> balance using balanced data 35,184 tweets, imbalance using imbalanced data 110,449 tweets*
This script will do:
- Read tweets_corpus
- Conduct ten folds cross validation to the corpus by building classification model (Naive Bayes, SVM, Decision Tree) using sklearn library in each iteration
- Print the results of each iteration
- Print the final results (average)

**count\_words.py**
*Parameter 1: text file name to be analyzed*
This script will do:
- Read the text file
- Do preprocessing
- Count each word appearance within the file
- Print top 50 word appearance

**feature\_word\_list.txt**
Top 50 word appearance from tweets\_corpus/traffic\_tweets\_combined.txt is taken and cleaned up from unused words. We get 40 words as features.

**get\_random\_tweets.py**
*Parameter 1: number of random tweets that you want to get*
This script will do:
- Stream tweets from Twitter Streaming API with *track* filter parameters: 
```
track=['aku', 'mending', 'gak', 'nggak', 'ngga', 'oke', 'tapi', 'tidak']
```
- Save tweets in random\_tweets.txt

**get\_tweets.py**
*Parameter 1: twitter username*
Get all tweets (Twitter REST API limit up to 3200 tweets) from a twitter username then save to \[username\].txt

**init.sh**
Bash script to install required Python intepreter and libraries.

**name\_list.txt**
List of location name of Yogyakarta Province, Indonesia. Gathered from several source.

**replacement_word\_list.txt**
List of abbreviations and their real phrases.

**stop\_words_list.txt**
List of stopwords in Bahasa Indonesia, but not used in the project yet. Maybe useful later.

**stream\_and\_classify.py**
*Parameter 1: "prod" to only save result file in \*.txt and \*.csv; "dev" to also print to screen*
This script will do:
- Build classification model (Naive Bayes, SVM, Decision Tree) from tweets_corpus using sklearn library
- Stream from Twitter Streaming API tweets of Yogyakarta Province, Indonesia
- Classify tweets to "traffic" and "non_traffic"
- Save to file and print to screen

**stream\_classify\_save\_db.py**
*Parameter 1: "prod" to only save to mysql database; "dev" to also print result to screen, save file in \*.txt and \*.csv*
This script will do:
- Build classification model (Naive Bayes, SVM, Decision Tree) from tweets_corpus using sklearn library
- Stream from Twitter Streaming API tweets of Yogyakarta Province, Indonesia
- Classify tweets to "traffic" and "non_traffic"
- Save to MySQL database
- Save to file and print to screen (if "dev")

**tagged\_name\_list.txt**
List of location name of Yogyakarta Province, Indonesia that have been tagged with PRFX, B-LOC, and I-LOC tags.

**tweet\_object\_example.json**
Tweets object sample that will be returned by Twitter API.
