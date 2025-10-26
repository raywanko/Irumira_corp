from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

MENU_DATA = {
    "menu": [
        {"title": "社長挨拶", "link": "/company/message/", "subtitle": "PRESIDENT MESSAGE"},
        {"title": "会社概要・役員一覧", "link": "/company/profile/", "subtitle": "COMPANY PROFILE"},
        {"title": "沿革", "link": "/company/history/", "subtitle": "HISTORY"},
        {"title": "事業内容", "link": "/company/organization/", "subtitle": "ORGANIZATION"}
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
        # フォームデータ取得
        desired_position = request.POST.get('desired_position', '')
        last_name = request.POST.get('last_name', '')
        first_name = request.POST.get('first_name', '')
        last_name_kana = request.POST.get('last_name_kana', '')
        first_name_kana = request.POST.get('first_name_kana', '')
        birth_date = request.POST.get('birth_date', '')
        gender = request.POST.get('gender', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        education = request.POST.get('education', '')
        work_experience = request.POST.get('work_experience', '')
        qualifications = request.POST.get('qualifications', '')
        motivation = request.POST.get('motivation', '')
        self_pr = request.POST.get('self_pr', '')
        desired_start_date = request.POST.get('desired_start_date', '')
        remarks = request.POST.get('remarks', '')
        
        # 管理者宛メール本文
        admin_subject = f'【採用応募】{last_name} {first_name}様からの応募 - {desired_position}'
        admin_message = f"""
採用応募がありました。

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 基本情報
━━━━━━━━━━━━━━━━━━━━━━━━━━
希望職種: {desired_position}
お名前: {last_name} {first_name}
フリガナ: {last_name_kana} {first_name_kana}
生年月日: {birth_date}
性別: {gender}

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 連絡先
━━━━━━━━━━━━━━━━━━━━━━━━━━
メールアドレス: {email}
電話番号: {phone}
住所: {address}

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 学歴・経歴
━━━━━━━━━━━━━━━━━━━━━━━━━━
最終学歴: {education}

職務経歴:
{work_experience}

保有資格:
{qualifications if qualifications else '（なし）'}

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 志望動機
━━━━━━━━━━━━━━━━━━━━━━━━━━
{motivation}

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ 自己PR
━━━━━━━━━━━━━━━━━━━━━━━━━━
{self_pr}

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ その他
━━━━━━━━━━━━━━━━━━━━━━━━━━
希望入社時期: {desired_start_date if desired_start_date else '未選択'}

特記事項:
{remarks if remarks else '（なし）'}

━━━━━━━━━━━━━━━━━━━━━━━━━━
このメールは自動送信されています。
株式会社イルミラ 採用管理システム
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # 応募者宛の確認メール本文
        user_subject = '【株式会社イルミラ】採用応募を受け付けました'
        user_message = f"""
{last_name} {first_name} 様

この度は株式会社イルミラの採用にご応募いただき、誠にありがとうございます。

以下の内容で応募を受け付けいたしました。

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ ご応募内容
━━━━━━━━━━━━━━━━━━━━━━━━━━
希望職種: {desired_position}
お名前: {last_name} {first_name}
メールアドレス: {email}
電話番号: {phone}

━━━━━━━━━━━━━━━━━━━━━━━━━━

担当者より2〜3営業日以内にご連絡させていただきます。
今しばらくお待ちくださいませ。

※このメールは送信専用です。返信いただいてもお答えできませんのでご了承ください。

━━━━━━━━━━━━━━━━━━━━━━━━━━
株式会社イルミラ 採用担当
〒460-0003
愛知県名古屋市中区錦3-19-20 ロジック千種ビル3階
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        try:
            # 管理者にメール送信
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # 応募者に確認メール送信
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'ご応募ありがとうございます。ご入力いただいたメールアドレスに確認メールを送信いたしました。')
        except Exception as e:
            messages.error(request, 'メール送信中にエラーが発生しました。しばらくしてから再度お試しください。')
            print(f"メール送信エラー: {e}")
        
        return redirect('main:recruit_apply')
    return render(request, 'main/recruit_apply.html')

def news(request):
    return render(request, 'main/news.html')

def contact(request):
    if request.method == 'POST':
        # フォームデータ取得
        inquiry_type = request.POST.get('inquiry_type', '')
        company_name = request.POST.get('company_name', '')
        last_name = request.POST.get('last_name', '')
        first_name = request.POST.get('first_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        message_text = request.POST.get('message', '')
        
        # 管理者宛メール本文
        admin_subject = f'【お問い合わせ】{last_name} {first_name}様 - {inquiry_type}'
        admin_message = f"""
お問い合わせがありました。

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ お問い合わせ情報
━━━━━━━━━━━━━━━━━━━━━━━━━━
お問い合わせ種別: {inquiry_type}
会社名: {company_name if company_name else '（個人）'}
お名前: {last_name} {first_name}
メールアドレス: {email}
電話番号: {phone if phone else '（未入力）'}

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ お問い合わせ内容
━━━━━━━━━━━━━━━━━━━━━━━━━━
{message_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━
このメールは自動送信されています。
株式会社イルミラ お問い合わせ管理システム
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        # 問い合わせ者宛の確認メール本文
        user_subject = '【株式会社イルミラ】お問い合わせを受け付けました'
        user_message = f"""
{last_name} {first_name} 様

この度は株式会社イルミラへお問い合わせいただき、誠にありがとうございます。

以下の内容でお問い合わせを受け付けいたしました。

━━━━━━━━━━━━━━━━━━━━━━━━━━
■ お問い合わせ内容
━━━━━━━━━━━━━━━━━━━━━━━━━━
お問い合わせ種別: {inquiry_type}
会社名: {company_name if company_name else '（個人）'}
お名前: {last_name} {first_name}
メールアドレス: {email}

お問い合わせ内容:
{message_text}

━━━━━━━━━━━━━━━━━━━━━━━━━━

担当者より2〜3営業日以内にご連絡させていただきます。
今しばらくお待ちくださいませ。

※このメールは送信専用です。返信いただいてもお答えできませんのでご了承ください。

━━━━━━━━━━━━━━━━━━━━━━━━━━
株式会社イルミラ
〒460-0003
愛知県名古屋市中区錦3-19-20 ロジック千種ビル3階
━━━━━━━━━━━━━━━━━━━━━━━━━━
        """
        
        try:
            # 管理者にメール送信
            send_mail(
                admin_subject,
                admin_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            
            # 問い合わせ者に確認メール送信
            send_mail(
                user_subject,
                user_message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'お問い合わせありがとうございます。ご入力いただいたメールアドレスに確認メールを送信いたしました。')
        except Exception as e:
            messages.error(request, 'メール送信中にエラーが発生しました。しばらくしてから再度お試しください。')
            print(f"メール送信エラー: {e}")
        
        return redirect('main:contact')
    return render(request, 'main/contact.html')