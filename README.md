# Functional and Performance tests
**Note:** In order to automatically install all the libraries needed to run those tests run the following command:
>pip install -r requirements.txt

There is also the option to run the dockerized pipeline on every push or manually by selecting **Run workflow** ![image](https://user-images.githubusercontent.com/22115159/232199469-31d24c0b-8bd4-4bbe-b2fb-9b465a123bd6.png)

In order to skip running the pipeline on every push the 
>[ci skip]

command should be entered in the end of each commit message.
>e.g. first commit [ci skip]




Functional test suite:

    1) Contains a fake http server in Python with API that behaves similar to https://swapi.dev/
    It supports the same three end-points (people/xx/, planets/xx/, starships/xx/)
    and  can always return the same json response for any id passed.
    For ids >100 returns a 404 Not Found error with a json body that describes the problem.
    The server keeps a log file that logs all the incoming requested URLs and response codes.
    
    2) Contains an automated test suite using Robot Framework that:
        a) prepares the test environment by starting the http server
        b) runs test cases per end-point that verify both happy path (sends back a valid json response with the expected values)
            or edge cases
        c) shuts down the environment
        d) prints out the test execution results to the console

Performance test suite:

    3) Extention of the http server to incur a random small delay per http request.
    
    4) Creation of a performance test that:
        a) prepares the test environment by starting the http server
        b) accesses one of the end-points continuously for a time duration of 1 minute
        c) for each access it keeps track of the response time on the client side
        d) shuts down the environment
        e) prints out mean & standard deviation of the response time for the end-point
