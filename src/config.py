__author__ = "Ziyad Alsaeed"
__email__ = "zalsaeed@qu.edu.sa"

"""
Here we set up the main projects' deadlines. You should set these up according to the deadlines for the course
(i.e., set them up once then forget about them).

What are these used for?
These are used to check the date and time of the last commit to each repo. Education management systems
(e.g., Blackboard) gives you control on the configuration file submission. However, students can keep editing their
repositories. Hence, these date will be used to check the last commit on each downloaded repository.
There could be an issue though if you give some student an exception in terms of the deadline. In such a case you will
need to handle it manually (or maybe a feature you can add!). As of now our mitigation is that we provide you with
two scores at the end of grading. One with the late penalty applied (if any) and the other act as if the late policy
doesn't exists. Thus, you get to choose which one to consider.

In addition to the deadlines, this file sets up the the logging configuration, and track the links for each project.
"""

import datetime
import logging

# set up logger
for handler in logging.root.handlers[:]:  # make sure all handlers are removed
    logging.root.removeHandler(handler)
# in some cases the logging level will change to DEBUG based on what happens in search, but in general this is the
# logging level we want
logging_level = logging.DEBUG
logging.root.setLevel(logging_level)
logging_format = logging.Formatter('%(asctime)s: %(levelname)s [%(name)s:%(funcName)s:%(lineno)d] - %(message)s')

h = logging.StreamHandler()
h.setFormatter(logging_format)
logging.root.addHandler(h)

# pattern (year, month[1:12], day[1:31], hour[0:23], minutes[0:59])
P0_DEADLINE = datetime.datetime(2022, 9, 12, 17, 0)
P1_DEADLINE = datetime.datetime(2022, 9, 19, 17, 0)
P2_DEADLINE = datetime.datetime(2022, 9, 26, 17, 0)
P3_DEADLINE = datetime.datetime(2022, 10, 3, 17, 0)
P4_DEADLINE = datetime.datetime(2022, 10, 17, 17, 0)
P5_DEADLINE = datetime.datetime(2022, 10, 24, 17, 0)
P6_DEADLINE = datetime.datetime(2022, 10, 31, 17, 0)
P7_DEADLINE = datetime.datetime(2022, 11, 7, 17, 0)

# original links for the assignment repo, we only need the workspace name and user!
# these are needed to see if student provided the link of the original repo
workspace = "your work space in bitbucket"
username = "your username in bitbucket"
