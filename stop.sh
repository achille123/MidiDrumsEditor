kill -9 $(lsof -ti :5000 -sTCP:LISTEN)
kill -9 $(lsof -ti :5001 -sTCP:LISTEN)
kill -9 $(lsof -ti :5002 -sTCP:LISTEN)
kill -9 $(lsof -ti :5003 -sTCP:LISTEN)