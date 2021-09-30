This is my code I made for the extract summit coding contest by Zyte that happened in September 30th 2021.

The main objective was to scrape 4 fields of data of each item in the website: item_id, image_id (avaible or not), flavor (string), name. You released code from your scrapy spider into the Zyte cloud, and a discord bot gave you feedback on the submission. You had to reach the 100 score (all fields scraped with no errors) to win.

Since I don't know scrapy, I instead used my standard requests + beautiful soup knowledge in the scrapy spider. It was terrible to write code because I wrote a python spider and copy and pasted into the scrapy spider because I couldn't really read what was going on in the scrapy console.

I managed to hit 68 score in the first 1 hour and 30 minutes, however I got stuck there because I couldn't proceed. I spent the next hours trying to see if my data was wrong when in reality I needed to scrape more stuff. 15 minutes before the competition was over I noticed that you had to scrape the "recommendations" (a section of items inside an item). Recommendations had some items that wheren't avaible in the site. Because of that, I lost.

It was still fun though, and I liked the experience I got. I didn't have enough time to finish the test website, but I did some of it. I noticed some of the "gotchas" on the website where the same as on the competition, so someone could only be on the top 3 winners if they completed the test website. Alas, I loose. I hope to do better next year.

The code is definitely not pretty since it was made in a hurry, and might possibly not be working because I had to write my code on spider.py and then put it inside my scrapy spider. And I figured the recommendations thing 15 minutes before the competition was over so I wrote the item extraction function in a hurry (which was code inside the for loop in the extract page function).