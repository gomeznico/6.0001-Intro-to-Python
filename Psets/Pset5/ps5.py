# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Nico Gomez
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    """
    initializes NewsStory object

    has 5 attributes:
        self.guid (string, a Global Unique ID)
        self.title  (string, story title)
        self.description (string, story description)
        self.link (string, link to story)
        self.pubdate (datetime, publication date)
    """
    def __init__(self, guid, title, description, link, pubdate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_link(self):
        return self.link

    def get_pubdate(self):
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        """
        Subclass of trigger with one extra attribute

        self.phrase (string, phrase to trigger, assume phrase does not contain punctuation or multiple spaces between words)

        """
        self.phrase = phrase

    def is_phrase_in(self, text):
        """
        Returns True if self.phrase is in the text

        will return true regardless of case, punctuation, spaces.
        will return false if order is incorrect, spaces, or words break up phrase
        """

        ## remove cases and replace punctuation with spaces
        trans_dict = str.maketrans(string.punctuation, ' '*(len(string.punctuation)))

        no_punct_text = text.lower().translate(trans_dict)
        cleaned_text = ' '.join(no_punct_text.split()) + ' '

        no_punct_phrase = self.phrase.lower().translate(trans_dict)
        cleaned_phrase = ' '.join(no_punct_phrase.split()) + ' '

        if cleaned_phrase not in cleaned_text:
            return False
        else:
            return True

# Problem 3
class TitleTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_title())

# Problem 4
class DescriptionTrigger(PhraseTrigger):
    def evaluate(self, story):
        return self.is_phrase_in(story.get_description())

# TIME TRIGGERS

# Problem 5
class TimeTrigger(Trigger):
    def __init__(self, date_string):
        """
        date_string (string, date in EST format: '3 Oct 2016 17:00:10')
        """

        time = datetime.strptime(date_string,"%d %b %Y %H:%M:%S")
        self.time = time

# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def evaluate(self, story):
        # return true if pubdate is before trigger time
        try:
            return story.get_pubdate() < self.time
        except TypeError:
            time = self.time.replace(tzinfo=pytz.timezone("EST"))
            return story.get_pubdate() < time

class AfterTrigger(TimeTrigger):
    def evaluate(self, story):
        # return true if pubdate is before trigger time
        try:
            return story.get_pubdate() > self.time
        except TypeError:
            time = self.time.replace(tzinfo=pytz.timezone("EST"))
            return story.get_pubdate() > time

# COMPOSITE TRIGGERS

# Problem 7
class NotTrigger(Trigger):
        def __init__(self, trigger):
            self.trigger = trigger

        def evaluate(self, story):
            return not self.trigger.evaluate(story)

# Problem 8
class AndTrigger(Trigger):
        def __init__(self, trigger1, trigger2):
            self.trigger1 = trigger1
            self.trigger2 = trigger2

        def evaluate(self, story):
            return  (self.trigger1.evaluate(story) & self.trigger2.evaluate(story))

# Problem 9
class OrTrigger(Trigger):
        def __init__(self, trigger1, trigger2):
            self.trigger1 = trigger1
            self.trigger2 = trigger2

        def evaluate(self, story):
            return  (self.trigger1.evaluate(story) or self.trigger2.evaluate(story))

#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    triggered_stories =[]

    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
                break # go to next story as soon as a trigger is true

    return triggered_stories

#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    trigger_map ={
        'TITLE': TitleTrigger,
        'DESCRIPTION': DescriptionTrigger,
        'AFTER': AfterTrigger,
        'BEFORE': BeforeTrigger,
        'NOT': NotTrigger,
        'AND': AndTrigger,
        'OR': OrTrigger
    }

    triggers_dict = {}
    triggers_list = []

    for line in lines:
        line_arr = line.split(',')
        if line_arr[0] != 'ADD':
            name = line_arr.pop(0)
            type = line_arr.pop(0)
            if type in ['AND','OR']:
                trig1 = triggers_dict[line_arr.pop(0)]
                trig2 = triggers_dict[line_arr.pop(0)]
                triggers_dict[name] = trigger_map[type](trig1,trig2)
            else:
                arg = "".join(line_arr)
                triggers_dict[name] = trigger_map[type](arg)
        else:
            line_arr.pop(0) # remove 'ADD', and iterate through list
            for trigger_name in line_arr:
                triggers_list.append(triggers_dict[trigger_name])

    return triggers_list


SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Kamala")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line
        triggerlist = read_trigger_config('triggers.txt')

        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()


