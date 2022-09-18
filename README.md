# PyGrade

PyGrade is a mini auto grader framework targeting python based projects. PyGrade is designed to pull code from remote repositories
(one for each student) and to perform a set of tasks (tests) then generate accumulative and detailed reports for the
instructor and the students. 

PyGrade assumes that you will have students provide key file that has their assignment information
(name, link to repo, and student id, in a `.ini` format). Using the key file PyGrade will go over all the tasks you
defined for each student to collect a task feedback and finally generate all the reports. In designing PyGrade
the main goal was to simplify defining tasks (tests). That is tasks are simply methods that you define 
to perform some test and return whether they passed or not with a clear message of how did they pass or not.
The tasks you define are expected to be error handling tasks. Meaning, if the student fails your test, instead of
throwing an exception, you should catch it and return it as a feedback.

###### Author: Ziyad Alsaeed

## Implemented Features:

1. **Task based grading system.** The tasks are not necessary unittests. Instead, they are 
   whatever the user define as a method (including unit test). A task should have an id, goal,
   possible points, points earned, feedback, and a command to execute. The command here is whatever
   the instructor want to do.
2. **Reading Keys.** We provide the essential tool to read key files to establish the student information.
3. **Git Handling Module.** The PyGrade have a git module that would clone any repo given to it and return the
   result of the clone process. Also, it handles the checking the repos last made edits against a defined deadline.
4. **Rubric module.** We provide a notion of a rubric that would be added to each student object and store all
   the task defined by the instructor. Based on the tasks, the rubric will provide an easy interface to calculate
   grades and grade related reports. 
5. **Reporting Module.** The PyGrade allows you to generate accumulative reports that are suited for instructor. Also, 
   it provides reporting student performance to easily communicate the grades breakdown with students. See sample
   outputs in the [samples](samples) directory. 

## Planned Features <sup>[1](#myfootnote1)</sup>

- **Communicating Details:** As of now, the generated reports have to be uploaded one by one to the education management 
   system (e.g., blackboard). Such portals don't provide any API to upload such files. Thus, this is an unfortunate
   end to an automated PyGrade. The next best option is to email the reports directly to students. We already have
   their accounts; all we need is to write a module that would email them one by one using our official account
   (if it allows smtp). The other option, which we don't like, is to push the report to the student's repos. We don't
   want to go this rout as we would like to preserve the student's repos integrity. 
- **Feedback Class:** Currently, we use a tuple to record feedback from a task we conduct (bool, message). This is good
   so far. However, the tuple feedback is very rigid. We should create a class that holds the feedback which provides
   some additional functionality (like giving a student half a point for a task). Also, a feedback object will make
   it easier to extend the PyGrade in the future. 
- **Export student detailed feedback:** The markdown we generate is not a format we could use in the future. We need to
   generate a report in a more sustainable format. Instead of exporting as Markdown, we should export with something
   like CSV (what other options?). Then, at any point in the future, we can generate the markdown from the CSV. The
   current setup leaves us with the markdown only, which is good but not portable.
- **Posting Grades:** We need to write a script to merge our new project grade with the student's overall grades from
   the education management system (e.g., blackboard). The merger script will make communicating the grades much easier
   (just import them).
- **Plagiarism Detection** For the initial projects the tasks are simple and have no deep algorithmic requirements.
   However, as students advance in the course a more demanding projects will be assigned. In these future projects,
   a similarity check system might be necessary to sustain the automation. There are different similarity check
   systems. One of the most well know applications is [Moss](https://theory.stanford.edu/~aiken/moss/). We should
   look into how to integrate with Moss and sustain the automation. 

## Files Structure

Ordered alphabetically:

- **[src/command.py](src/command.py)** is a class that takes a reference of a method and its argument for latter execution. 
   The there are two types of commands (python methods and bash commands). As of now only one type (python based
   commands) is implemented.
- **[src/config.py](src/config.py)** is a configuration file. The most important part of the file is setting up the assignments'
   deadlines.
- **[src/git.py](src/git.py)** is a set of methods that handles cloning students repos as well as checking the edits made against
   the defined deadline.
- **[p0.py](p0.py)** is a sample assignment grading file that uses all the defined modules to put everything together.
   In addition of using all the modules, it defines additional task as tests for the student.
- **[src/report.py](src/report.py)** A set of methods that handle all the reporting of the assignments at the end of the grading
   process.
- **[src/rubric.py](src/rubric.py)** A class defining a rubric that should be attached to each student. It is necessary for
   holding task and making final grade calculations. 
- **[src/student.py](src/student.py)** A student module that defines the student's information and grades. 
- **[src/task.py](src/task.py)** A task module which defines a task that needs a goal and a command to execute then it will return
   results of executing the command with the points earned (if any).
- **[src/util.py](src/util.py)** helper functions. 

## Footnotes
<a name="myfootnote1">1</a>: The features are not ordered according to prioritization!