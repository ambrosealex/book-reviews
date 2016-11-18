from django.shortcuts import render, redirect
from django.contrib import messages
from . import models

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = 0
    return render(request,'book_app/index.html')

def register(request):
    check_email = models.Users.objects.filter(email = request.POST['email'])
    if check_email:
        print 'THIS EMAIL IS ALREADY IN USE'
        return redirect('/')
    if request.POST['pass_init'] != request.POST['pass_confirm']:
        print "PASSWORDS DONT MATCH"
        return redirect('/')
    models.Users.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = request.POST['pass_init'])
    return redirect('/')

def login(request):
    current_user = models.Users.objects.filter(email = request.POST['email'])
    if not current_user:
        print "NOT A VALID EMAIL"
        return redirect('/')
    if request.POST['pass_log'] == current_user[0].password:
        print "HOORAY FOR ME"
    else:
        print "WRONG PASSWORD"
        return redirect('/')
    request.session['user_id'] = current_user[0].id
    return redirect('/books')

def books(request):
    books = models.Books.objects.all().order_by('title')
    reviews = models.Reviews.objects.all()
    print "This is the request.session id", request.session['user_id']
    user = models.Users.objects.get(id = request.session['user_id'])
    recents = models.Reviews.objects.order_by('-created_at')[:3]
    print recents

    context = {
        'books' : books,
        'reviews' : reviews,
        'user' : user,
        'recents' : recents,
        'n' : range(5)
    }
    return render(request, 'book_app/books.html', context)

def add(request):
    authors = models.Books.objects.order_by().values('author').distinct()
    print authors
    context = {
        'authors' : authors
    }
    return render(request,'book_app/add.html', context)

def create(request):
    print request.POST['author2']
    if request.POST['author2'] == '':
        author = request.POST['author1']
    else:
        author = request.POST['author2']

    print author
    newBook = models.Books.objects.filter(title = request.POST['title'])
    if newBook:
        models.Reviews.objects.create(rating = request.POST['rating'], review = request.POST['review'], user_id = models.Users.objects.get(id = request.session['user_id']), book_id = newBook[0])
    else:
        models.Books.objects.create(title = request.POST['title'], author = author)

        current_book = models.Books.objects.get(title = request.POST['title'])

        request.session['book_id'] = current_book.id

        models.Reviews.objects.create(rating = request.POST['rating'], review = request.POST['review'], user_id = models.Users.objects.get(id = request.session['user_id']), book_id = models.Books.objects.get(id = request.session['book_id']))

    return redirect('/books')

def logout(request):
    del request.session['user_id']
    return redirect('/')

def page(request, id):
    book = models.Books.objects.get(id=id)
    reviews = models.Reviews.objects.filter(book_id=id)
    context = {
        'book' : book,
        'reviews' : reviews,
        'n' : range(5)
    }
    return render(request, 'book_app/page.html', context)

def users(request, id):
    user = models.Users.objects.get(id=id)
    books = models.Reviews.objects.filter(user_id=id)
    count = books.count()
    context = {
        'user' : user,
        'books' : books,
        'count' : count
    }
    return render(request, 'book_app/user.html', context)


def delete(request, id):
    bID = str(models.Reviews.objects.get(id=id).book_id.id)
    print bID
    models.Reviews.objects.filter(id=id).delete()
    return redirect('/books/'+bID)
