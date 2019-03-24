import csv 
import xlwt
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string

from .models import Book
from .forms import BookForm


def home(request):
    return render(request, 'home.html')


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book/book_list.html', {'books': books})


def save_book_form(request, form, template_name):
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            books = Book.objects.all()
            data['html_book_list'] = render_to_string('book/includes/partial_book_list.html', {
                'books': books
            })
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
    else:
        form = BookForm()
    return save_book_form(request, form, 'book/includes/partial_book_create.html')


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
    else:
        form = BookForm(instance=book)
    return save_book_form(request, form, 'book/includes/partial_book_update.html')


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    data = dict()
    if request.method == 'POST':
        book.delete()
        data['form_is_valid'] = True
        books = Book.objects.all()
        data['html_book_list'] = render_to_string('book/includes/partial_book_list.html', {
            'books': books
        })
    else:
        context = {'book': book}
        data['html_form'] = render_to_string('book/includes/partial_book_delete.html', context, request=request)
    return JsonResponse(data)


def get_date(dd):
    return f"{dd.day}/{dd.month}/{dd.year}"


def export_users_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users.csv'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Plublication date', 'Author', 'Price', 'Pages', 'Type','Content'])

    users = Book.objects.all().values_list('title', 'publication_date', 'author', 'price', 'pages', 'btype', 'body')
   
    for user in users:
        user = list(user) # parse list
        if isinstance(user[-1], datetime):
            user[-1] = get_date(user[-1])
        writer.writerow(user)
    
    return response 


def export_users_xls(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['content-Disposition'] = 'attachment; filename="users.xlsx"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True 

    columns = ['Title', 'Plublication date', 'Author', 'Price', 'Pages', 'Type','Content']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num],font_style)
    
    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Book.objects.all().values_list('title', 'publication_date', 'author', 'price', 'pages', 'btype', 'body')

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num])
            pass
    wb.save(response)
    return response