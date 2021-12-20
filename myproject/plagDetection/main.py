from pymongo import cursor
import pysimilar
from pprint import pprint
from pysimilar import compare
from __main__ import *
from ..plagDetection import similarity
import sys

def result(textFromFile):

   print(textFromFile)

   return (similarity.returnTableWithURL(similarity.report(str(textFromFile))))



# if __name__ == '__main__':
#     try:
#         arg = sys.argv[1]
#     except IndexError:
#         arg = None

#     return_data = result(arg)

# {% extends "home.html" %}

# @app.route('/', methods=['GET', 'POST'])
# def data():
#     return render_template('home.html')


# @app.route('/report',methods = ['POST', 'GET'])
# def result():
#    if request.method == 'POST':
#       result = request.FILES['docfile'].read()
#       return (similarity.returnTable(similarity.report(str(result))))