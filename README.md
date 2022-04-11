# Match My Abstract

Economists, like all academics, often need to publish their work in journals. But particularly when early in your career, it’s not always obvious what journal would be a good fit for your paper, and scouring through recent papers in a large number of journals to find out is very time-consuming. This web app is meant to help here. It uses data from arXiv to match your paper with a suitable journal based on the similarity of your abstract with already published papers.

# Data
Currently, the web app is based on a relatively small data set of about 500 abstracts in English from x journals in economics, all drawn from arXiv. arXiv was chosen because they have a good API that makes it fairly easy to collect abstracts in bulk. The ambition is for later versions of the app to work off of a much larger data set and on abstracts drawn from more academic disciplines.

# Method
The app uses cosine similarity to measure the similarity between your abstract and each of the abstracts in the data set. Cosine similarity is a well-established measure for text similarity. How does it work? Any quantitative analysis of texts needs to convert a text to a set of numbers. This process is known as “vectorisation”, since the resulting set of numbers for any given texts represents a vector in an n-dimensional vector space. Cosine similarity corresponds to the cosine of the angle between two such vectors. A cosine of 0 represents two vectors that are at 90 degrees to one another and as such orthogonal or unrelated. The closer cosine gets to 1 the smaller the angle and greater the match. The cosine similarity score returned for a journal by the app is the average score for each abstract in that journal.

# Limitations
The size of the data set is an obvious limitation. Relatedly, some journals are represented by a small number of abstracts, in some cases as few as one. The app’s “recommendations” should be taken with these facts in mind.

# Contact
For any questions, comments or suggestions, contact me at ahlstromvij@gmail.com. 
