from django.shortcuts import render, redirect
from books.models import Book
from django.core.paginator import Paginator
from datetime import datetime


def index(request):
    return redirect('books')

def books_view(request):
    template = 'books/books_list.html'
    sort = request.GET.get('sort', 'pub_date')
    books = Book.objects.all().order_by(sort)
    context = {'books': books}
    return render(request, template, context)

def show_book(request, book_id):
    template = 'books/show_book.html'
    book = Book.objects.get(id = int(book_id))
    context = {'book': book}
    return render(request, template, context)

def show_pubdate(request, pubdate):
    template = 'books/pub_dates.html'
    pubdate = datetime.date(datetime.strptime(pubdate, '%Y-%m-%d'))
    pd = Book.objects.values('pub_date').order_by('pub_date').distinct('pub_date')
    pub_dates = [b['pub_date'] for b in pd]
    if pubdate in pub_dates:
        ind = pub_dates.index(pubdate)
    else:
        nearest_date = min(pub_dates, key=lambda x: abs(x - pubdate))
        ind = pub_dates.index(nearest_date)
    page_num = ind + 1
    paginator = Paginator(pub_dates, 1)
    page = paginator.get_page(page_num)
    books = Book.objects.filter(pub_date = str(pub_dates[ind])).all()
    context = {'books': books,
               'pages': page,
               'prev': (str(pub_dates[ind - 1]) if ind != 0 else ''),
               'now': str(pub_dates[ind]),
               'next': (str(pub_dates[ind + 1]) if ind < len(pub_dates) - 1 else '')
            }
    return render(request, template, context)

