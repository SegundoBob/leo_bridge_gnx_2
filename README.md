# leo_bridge_gnx_2
The two scripts in this repository demonstrate Leo-Editor bug "Implementation bug in fix to Issue #35".
I believe this is a bug in the fix to Issue #35.  I believe this is an implementation bug, not a design bug.

I encountered this bug while using Leo-Bridge to determine the differences between my Android Outliner version and my Leo-Editor version of each of many outlines.

Unrelated Bug also Demonstrated
-------------------------------

Please note also that despite options "gui='nullGui'" and "verbose=False" Leo-Bridge still writes many lines to the terminal.  These lines do not help and only confuse users of the scripts that I write which use Leo-Bridge.  Consequently, I think that with these options Leo-Bridge should only write errors to the terminal.  That is, Leo-Editor should NOT write:

```
file not found: /home/ldi/git/leo_bridge_gnx_2/foo.leo. creating new window

** isPython3: False
Leo 5.0-final, build 20141127165348, Thu Nov 27 16:53:48 CST 2014
Git repo info: branch = master, commit = bffb0e1bce65
Python 2.7.3, LeoGui: dummy version
linux2
reading settings in /home/ldi/git/leo_bridge_gnx_2/foo.leo
traverse no settings tree for foo.leo
wrote recent file: /home/bob05/.leo/.leoRecentFiles.txt
```

Bug Analysis
------------

The current Leo-Editor passes the test for Issue #35.  This implies that when an existing Leo-Editor file is opened, the "set Max node index" works as intended.

On the other hand, the master.py-slave.py test seems to show that "set Max node index" always sets the maximum node index to zero.

These two tests are very similar.  I don't know what the crucial difference is.  But it might be an "off by one" bug.  That is, the last node in the outline may be ignored.

On 2014-10-22 at 16:08 EKR committed b4c7bac90b4164dd0a9bfedb7631e0b3f9b82d26 which "Replaced the post-pass by a smarter gnx-allocation scheme."  This new scheme probably contains the bug.

Bug Demonstration Outline
-------------------------

File master.py uses the subprocess library to spawn a process to run slave.py.  First in a loop master.py "calls" slave.py with each "index" in idxList.

When slave.py is called with index K, it uses Leo-Bridge to add a new last child node to the root node of foo.leo and it sets the headline of this new node to K.

Then master.py uses Leo-Bridge to check that foo.leo contains exactly the expected nodes with the expected headlines.  When master.py detects an error, it prints useful error information to the terminal.

How to Run the Bug Demonstration
--------------------------------

Put master.py and slave.py in one directory.

Execute master.py.

Either master.py will run to completion, or it will hang forever.

For me now, master.py has been hanging four to six times in a row between each run to completion.

Hanging Forever
---------------

Hanging forever indicates a bug in Leo-Editor, but I don't know what that bug is.  However, it may be a bug that is only encountered when the bug in "set initial node index" causes a new node to get the same GNX as an existing node.  This hang bug should probably be investigated before fixing the "set initial node index" bug.  But if the hang bug turns out to be very hard to fix, it might be acceptable to just cover it up by fixing the "set initial node index" bug.

When slave.py hangs forever, you can see that it takes a large percentage of the CPU (50% on my system) and that Ctrl-C terminates it.  Canceling slave.py leaves foo.py in a corrupt state.  When Leo-Editor opens this foo.py, Leo-Editor hangs.

Runs to Completion
------------------

When master.py runs to completion without error, it prints to the terminal:

```
Test Passed.  No Error Detected.
```

When it detects an error, it prints to the terminal an error message like:

```
*** Problem:  Probably duplicate GNXs ***
headline "NewHeadline" gnx bob05.20150113124857.1
headline "0" gnx bob05.20150113124857.2
headline "1" gnx bob05.20150113124859.1
headline "2" gnx bob05.20150113124900.1
headline "2" gnx bob05.20150113124900.1
```

Test System
-----------

Xubuntu32 12.04 (precise)
kernel:  3.2.0-75-generic

Python 2, old build:
Leo 5.0-final, build 20141127165348, Thu Nov 27 16:53:48 CST 2014
Git repo info: branch = master, commit = bffb0e1bce65
Python 2.7.3, LeoGui: dummy version

Python 3, old build:
Leo 5.0-final, build 20141127165348, Thu Nov 27 16:53:48 CST 2014
Git repo info: branch = master, commit = bffb0e1bce65
Python 3.2.3, LeoGui: dummy version

Python 2, latest build:
Leo 5.0-final, build 20150107092423, Wed Jan  7 09:24:23 CST 2015
Git repo info: branch = master, commit = aacf05b1b513
Python 2.7.3, LeoGui: dummy version

Python 3, latest build:
Leo 5.0-final, build 20150107092423, Wed Jan  7 09:24:23 CST 2015
Git repo info: branch = master, commit = aacf05b1b513
Python 3.2.3, LeoGui: dummy version

Note: Commit aacf05b1b513 is the commit to my local repo of the merge of the latest github master commit
```
commit cac740601b9c8176dc2eed9626f2db9f9c724153
Author: Edward K. Ream <edreamleo@gmail.com>
Date:   Tue Jan 13 10:39:13 2015 -0600
```


