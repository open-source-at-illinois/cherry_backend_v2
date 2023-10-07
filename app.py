# Temporary script for actually running a flask debug server for API testing purposes

from flask import Flask, request
from api import app
import sys
import os

port = 8080

if sys.argv.__len__() > 1:
    port = sys.argv[1]
print("Api running on port : {} ".format(port))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port, debug=True)