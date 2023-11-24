# Experience controller

Lacking of a good experience strategy is main difficult to our evaluation.
It is also cost time to learn new experience framework on market.
Therefore, we intend to design a minimum framework to measure our evaluation.
It is mostly based on our hasty design in IRIT Toulouse (our master intern project)
surrounding by four factors:

1. Tester: configure and execute test case from clean environment.
2. Monitor: access internal resource and report quantitative activities.
3. Env: recover test environment to clean state after each test.
4. IO: control flow of input and output events in single experience.

This project is not intended to compete to any competitor in marker
but only try to minimize our learning curve
while trying to improve the usage through time if necessary.
By philosophy, the universal and usability is forbidden
while friendly, simplicity and scalability are our ally.

Project target is simply delivered in two steps:
Firstly, the designer define list of objects relating to predefined factors.
The controller receive user policy,
combine all designed object and deliver result to expected output directory.
For simplicity, the expected outcome of an experience is single text file.

## Controller communication

The controller is designed to communicate through UNIX socket.
The user drive controller through UNIX socket interface
which allows not only human but also test program to control itself.

The communication prompt is straightforward:
```
# Prompt:
[OBJECT TYPE] [OBJECT NAME] [OBJECT PARAMETERS]

# Example
TEST loop-20.py
MONITOR monitor.py --pid {PID}

# Special command to stop controller server
STOP CONTROLLER

# Special command to control IO flow
## Set result path
IO PATH {path}

## Set IO action
IO APPEND [True | False]
```

## Log driven

Driving test flow based on the event log is difficult but necessary.
For example, in sequence of test,
there is the test work specifically
after a state of other test.
Then the controller need to read previous test log
before deciding to fire up next test.
We call these case a log driven sequence.

To support this scenario,
we introduce pub/sub model
to distribute log data to multiple subscribes.

For performance, we propose some constraints on our design.
Subscribers are predefined before controller activate.
This is real time model without queue captured.
Subscriber work in side controller process
and communicate to controller through method call.
Subscriber contains special method
allowing controller to send log message in text format.
External subscriber work through IPC is extended from base subscriber
and should not be responsible of this work.
