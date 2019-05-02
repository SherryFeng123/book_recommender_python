from flask import *

app = Flask(__name__)

def readBooks(bfilename):
       
       ''' Read book titles from the file bfilename,
       append each book title to the list books and return it'''

       
       book_list = []

       f = open(bfilename,'r')
       lines = f.readlines()

       for i in lines:
              i = i.replace("\n","")
              book_list.append(i)


       return book_list


@app.route('/')
def createProfile():
  
       
       books = readBooks('books.txt')
       html = ''
       html += '<h1> Welcome! Book recomendation system</h1>'

    
       html += '<form method="POST" action="/recommend">\n'

       for i in range(0,len(books)):
              html += books[i]
              n    = "rating" + str(i)
              html += '<input type="text" name="'+ n + '" value = 0>'
              html += '<br>'
       
       
       html += '<input type="submit" value="Enter" >\n'
       html += '</form>\n'
              

       return html



def readRatings(filename):

       dictionary = {}

       f = open(filename,'r')

       lines = f.readlines()


       for i in range(0,len(lines),2):
              names = lines[i]
              names = names.replace("\n","")
              ratings = lines[i+1]
              ratings = ratings.split()

              for z in range(0,len(ratings)):
                     y = int(ratings[z])
                     ratings[z] = y

              dictionary[names] = ratings
                                   
       return dictionary


def recommendBooks(books, dictRatings, userRatings) :

       similarityList = []

       v1 = userRatings

       recomBooks = []
       
       for i in dictRatings:
              user_names = i 
              v2 = dictRatings[i]
              
              dot = 0 
              
              for z in range(0,len(v2)):
                     dot += int(v1[z])*int(v2[z])

              similarityList.append([dot,user_names])

       sortedList = sorted(similarityList, reverse = True)
       #reverse = true will sort descending order
       topElems = sortedList[0:5]
       for k in topElems:
              user = k[1]
              #top 5 users

              ratings = dictRatings[user]

              count = 0
              for i in range(0,len(ratings)):
                     if ratings[i] == 5 and v1[i] == 0:
                            if count <5:
                                   if books[i] not in recomBooks:
                                          recomBooks.append(books[i])
                                          count = count + 1
                                          

       return recomBooks


@app.route('/recommend', methods = ['POST'])
def recommend():

       html = ''
       html = '<h1> These are the recommended books for you! </h1>'
       

       books = readBooks('books.txt')

       user_rating = []


       for i in range(0,len(books)):
              n = "rating" + str(i)
              ratingBook = request.form[n]
              user_rating.append(int(ratingBook))

       print(user_rating)
              

       dictRatings = readRatings('ratings.txt')
       userRatings = user_rating 

       
       recomBooks  = recommendBooks(books,dictRatings,userRatings)

       
       writeBooksToFile(recomBooks, 'recommendedBooks.txt')

       for z in recomBooks:
              html += '<br>'
              html += str(z)

       return html



def writeBooksToFile(recomBooks, filename):

       f = open(filename,'w')
       for i in recomBooks:
              f.write(i)
              f.write("\n")


app.run()
