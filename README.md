WTOL - Why (is LOTW) Taking Oddly Long?
---------------------------------------
Author: Fabio Pani - IZ2UQF <iz2uqf@fabiopani.it>
Version: 0.1 alpha

I like LOTW (Logbook Of The World), ARRL's worldwide system used by lots of hamradio operators.
This is the best system to upload hamradio logs and get back QSL confirmation, especially if
you want to achieve some of ARRL's awards in a simple way [IMHO]. And it's my preferred one.
Unfortunately, lately LOTW log evaluation process is taking very long time. At this moment,
evaluation queue will took more than 11 days to be processed, according to Logbook Queue Status
page (http://www.arrl.org/logbook-queue-status), and this is very strange.
Hamradio operators and ARRL members are not getting information from ARRL itself about those
issues. No information about the system and software in use.
So I decided to write a simple benchmark in order to simulate a reasonable QSO validation process,
including reading logs, writing QSOs in a database and validate them in order to get QSL
confirmations. I'm using Python + MySQL on a GNU/Linux system.
Database and software structure are simplified but they include core and critical steps, so that
expanding them in more complex structure won't probably impact in global performance.
Of course, you are free to modify and improve this software; also, you can choose to write your
own simulators using different approaches or more performant programming languages.

There are two scripts:
- generatelogs.py: this script generates random QSO log files on your file system
- validateqsos.py: this script reads all your random log files, write QSOs in the database and
validate QSOs into QSLs

Database.
Let's consider a reasonable simple core structure. The following one can be a useful core
structure in a real case and it can be expanded by joining other support tables.
Adding more descriptive fields to this table (or attached tables) shouldn't worsen very much
performances.
Create a database `wtol` and a user `wtol`@localhost, with password 'wtol'.
Create table `qso` as follows:

DROP TABLE IF EXISTS `qso`;
CREATE TABLE qso (
    `callsign` char(32) NOT NULL,
    `callsign_dx` char(32) NOT NULL,
    `datestart` datetime NOT NULL,
    `frequency` varchar(20) NOT NULL,
    `mode` varchar(10) NOT NULL,
    `qsl` int(1) unsigned default 0,
    PRIMARY KEY (`callsign`, `callsign_dx`, `datestart`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

(@) callsign: dummy callsign of the caller operator (the log submitter).
    In the real case, one station may have one or more callsigns. For our purpose, we suppose to have
    only one callsign for each station. In our model callsigns are 32-characters long unique hash strings.
(@) callsign_dx: the remote operator callsign.
(@) datestart: date and time when QSO started. Format: YYYY-MM-DD HH:MM:SS
(@) frequency: QSO frequency in kHz. For our purpose, we can choose a single band (or even non-standard frequency ranges).
(@) mode: QSO mode, among a limited set. This field has been added because it is requested when matching QSL validation.
(@) qsl: boolean. When checked, QSO has been confirmed.

generatelogs.py
---------------
This script is used to generate a set of logfile as input for the validateqsos.py script. It may take long time.
Logs are distributed in a file system structure because total log files number can be high.
Log files are not in a standard format (ADIF, Cabrillo...) but they contain one QSO for each row,
with values separated by '|'. This doesn't influence very much evaluation time.
Parameters can be set by the user in some constants.
First, the script check all required subdirs exist and create missing ones.
Then the script deletes all previously generated log files.
After that, the script generates a list of "callsigns" (hash): the number of callsigns is set in the
constant CALLSIGN_NUM.
For each callsign the script:
- generate a log file (file name is <callsign>.log under the appropriate directory);
- generate a random number of QSOs (between MIN_QSO_NUM and MAX_QSO_NUM). For each QSO:
  - date is between MIN_QSO_DATE and MAX_QSO_DATE;
  - frequency is between MIN_QSO_FREQ and MAX_QSO_FREQ;
  - mode is randomly chosen among modes in "modes" list;
  - randomly decides if a reciprocal QSO must be generated (for a future QSL generation), according to
    probability in QSL_QSO_RATE (80 means about 80% QSO will be confirmed). In this case, a reciprocal
    QSO record will be appended to <callsign_dx>.log file. In order to simulate a real case, date and
    frequency in reciprocal QSO will be modified, according tolerances in QSO_TIME_VARIANCE and
    QSO_FREQ_VARIANCE.
  - Finally append QSO to <callsign>.log file.

validateqsos.py
---------------
This script:
- removes all previous records from table qso;
- for each log file:
  - get callsign from log file name;
  - for each QSO (line) in log file:
    - retrieve all QSO values, included validation tolerances for date/time and frequency;
    - find valid reciprocal QSO for QSL confirmation: if found, then set related qsl field to 1;
    - add new QSO to qso table, setting qsl field to 0 or 1, according to previous result. Note
      that possible query exceptions are ignored here: random generation of QSOs may include
      duplicate primary keys. Probability is very low and this is not an issue if some QSOs are skipped.

Future improvements
-------------------
Reducing date/time conversion may yeld in performance improvement.

Test environment and results
----------------------------
Tested under Linux Ubuntu 12.10 desktop 32-bit.
Computer: 2 CPUs
    processor   : 0
    vendor_id   : GenuineIntel
    cpu family  : 6
    model       : 42
    model name  : Intel(R) Pentium(R) CPU G645 @ 2.90GHz
    stepping    : 7
    microcode   : 0x28
    cpu MHz     : 2900.000
    cache size  : 3072 KB
Memory: MemTotal:        4049732 kB

5347856 QSOs (about 90% confirmed): 93 minutes
