from django.shortcuts import render, redirect
from django.contrib import messages

MENU_DATA = {
    "menu": [
        {"title": "社長挨拶", "link": "/company/message/", "subtitle": "PRESIDENT MESSAGE"},
        {"title": "会社概要・役員一覧", "link": "/company/profile/", "subtitle": "COMPANY PROFILE"},
        {"title": "沿革", "link": "/company/history/", "subtitle": "HISTORY"},
        {"title": "組織概念図", "link": "/company/organization/", "subtitle": "ORGANIZATION"}
    ]
}

def index(request):
    return render(request, 'main/index.html', {'menu_data': MENU_DATA['menu']})

def product(request):
    return render(request, 'main/product.html')

def company(request):
    return render(request, 'main/company.html', {'menu_data': MENU_DATA['menu']})

def company_message(request):
    return render(request, 'main/message.html')

def company_profile(request):
    return render(request, 'main/profile.html')

def company_history(request):
    return render(request, 'main/history.html')

def company_organization(request):
    return render(request, 'main/organization.html')

def recruit(request):
    return render(request, 'main/recruit.html')

def recruit_apply(request):
    if request.method == 'POST':
        messages.success(request, 'ご応募ありがとうございます。担当者より折り返しご連絡させていただきます。')
        return redirect('main:recruit_apply')
    return render(request, 'main/recruit_apply.html')

def news(request):
    return render(request, 'main/news.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'お問い合わせありがとうございます。担当者より折り返しご連絡させていただきます。')
        return redirect('main:contact')
    return render(request, 'main/contact.html')
