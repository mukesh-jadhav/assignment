# Assignment
A sample python project demonstrating a service that receives stream of packets, processes them and calls web-hook to store the results. 

A “service” that does the following three jobs:<br><br>
● Receive packets of data in real-time and pass this on to an ancillary service for
processing<br>
● Collate the output from the ancillary service for a particular Primary Resource ID into a
single data packet<br>
● Once all data packets for a particular Resource are received, pass on the collated output
data further for downstream processing with minimum latency by calling a webhook<br><br>

<h2>Instructions to set up:</h2>
● Download and Redis for Windows MSI package from <a href='https://github.com/microsoftarchive/redis/releases/tag/win-3.0.504'>here.</a><br>
● Set up project dependencies in your virtual environment using provided requirements.txt.<br> 
● Set up Environment variable 'FORKED_BY_MULTIPROCESSING' with value 1.<br>
● Run below command to run celery workers.<br><b><code>python -m celery -A app.client worker -l info -P eventlet</code></b></p>
● Run files <b>'app.py', 'webhook.py'</b>- app.py is the actual service that accepts packets. wehook.py is a webhook for storing the output.<br>
● 'producer.py' simulates random number of sending package with unique resource_id's. </br></br>

<h2>Assumptions:</h2>
● The time difference between the receipt of two consecutive ordered data packets is random.<br>
● Ancillary service is a long-running job and it works in a synchronous manner.<br>
● The payload data is simulated by a simple string containing multiple words separated by a space.<br>
● As stated in the document, The “ancillary service” is a simple function that takes in a string consisting of several
space-separated words and returns an array of integers representing the length in
characters of each word in the input string.<br>
● API tests are omited as it's not much of a code and isn't really following a structured pattern.<br>

<br><br><br>
<b>Note: <b>After successful execution, code should auto generate a new directory(configurable in config) with all the text files for resources received. 
