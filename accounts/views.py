from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile

def signup_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        student_id = request.POST['student_id']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if not student_id.isdigit() or len(student_id) != 5:
            messages.error(request, '학번은 5자리 숫자로 입력해주세요. (예: 30512)')
            return redirect('signup')

        grade = int(student_id[0])
        class_num = int(student_id[1:3])
        student_num = int(student_id[3:5])

        if not (1 <= grade <= 3):
            messages.error(request, '학년은 1~3 사이여야 합니다.')
            return redirect('signup')

        if not (1 <= class_num <= 10):
            messages.error(request, '반은 01~10 사이여야 합니다.')
            return redirect('signup')

        max_student_num = 28 if grade == 1 else 25

        if not (1 <= student_num <= max_student_num):
            messages.error(request, f'번호는 01~{max_student_num:02d} 사이여야 합니다.')
            return redirect('signup')

        if Profile.objects.filter(student_id=student_id).exists():
            messages.error(request, '이미 등록된 학번입니다.')
            return redirect('signup')

        if password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 아이디입니다.')
            return redirect('signup')

        user = User.objects.create_user(username=username, email=email, password=password, first_name=name)
        Profile.objects.create(user=user, student_id=student_id)
        login(request, user)
        return redirect('home')

    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

from django.contrib.auth.decorators import login_required
from products.models import Product

@login_required
def mypage_view(request):
    tab = request.GET.get('tab', 'selling')

    if tab == 'sold':
        products = Product.objects.filter(seller=request.user, is_sold=True)
    elif tab == 'purchased':
        products = Product.objects.filter(buyer=request.user)
    else:
        products = Product.objects.filter(seller=request.user, is_sold=False)
        tab = 'selling'

    selling_count = Product.objects.filter(seller=request.user, is_sold=False).count()
    sold_count = Product.objects.filter(seller=request.user, is_sold=True).count()
    purchased_count = Product.objects.filter(buyer=request.user).count()

    return render(request, 'accounts/mypage.html', {
        'products': products,
        'tab': tab,
        'selling_count': selling_count,
        'sold_count': sold_count,
        'purchased_count': purchased_count,
    })

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        request.user.first_name = request.POST['name']
        request.user.email = request.POST['email']
        request.user.save()

        request.user.profile.student_id = request.POST['student_id']
        request.user.profile.save()

        return redirect('mypage')

    return render(request, 'accounts/edit_profile.html')