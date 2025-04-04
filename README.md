# IUB-Schedule-AutoBuilder
Automated Schedule Builder:

Feed it AAR (this + one.iu course search function makes the entire application IU Bloomington specific) 
Scrapes for requirements
Uses course search to find pertinent classes
When searching for class:
	Check that it meets requirements for something
	Check that it hasn’t been taken
	Check that student has necessary prerequisites
	Check if there is available time for the class in schedule
	

Website:

HOMEPAGE
IU Logo and Header
Home Page Prompts user for:
AAR upload
Semester and year for classes (limited to currently Fall 25)
Number of classes wanted
Difficulty of cumulative coursework load
Any class(es) exactly by code (ie. CSCI-C 241) they want for sure for the schedule

once all info is uploaded, shows loading screen while schedule builder runs

OUTPUT
Interactive visually pleasing layout of schedule that allows user to remove class
For each class, shows:
	Code of class
	Class difficulty score
	“X” to remove class
	Time of lecture and lab/discussion if needed 
If removed, prompts “Add new class? Or leave as is”

Possibly also an LLM produces notes of:
	What requirements the schedule completes
	Other information that might be pertinent to user that I can’t think of rn

