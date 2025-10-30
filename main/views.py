from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from datetime import date
import requests
from django.http import HttpResponse



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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.html import escape

logger = logging.getLogger(__name__)

def recruit_apply(request):
    if request.method == 'POST':
        # === reCAPTCHA v3 検証 ===
        recaptcha_token = request.POST.get('g-recaptcha-response', '')
        try:
            recaptcha_response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data={
                    'secret': settings.RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_token
                },
                timeout=5
            ).json()
            if not recaptcha_response.get('success') or recaptcha_response.get('score', 0) < 0.5:
                messages.error(request, '不正なアクセスが検出されました。再度お試しください。')
                logger.warning(f"reCAPTCHA failed: {recaptcha_response}")
                return redirect('main:recruit_apply')
        except Exception as e:
            messages.error(request, 'reCAPTCHAサーバーエラーが発生しました。')
            logger.error(f"reCAPTCHA verification error: {e}")
            return redirect('main:recruit_apply')

        # === 入力値取得とサニタイズ ===
        def clean_input(value):
            return escape(value.strip())

        desired_position = clean_input(request.POST.get('desired_position', ''))
        last_name = clean_input(request.POST.get('last_name', ''))
        first_name = clean_input(request.POST.get('first_name', ''))
        last_name_kana = clean_input(request.POST.get('last_name_kana', ''))
        first_name_kana = clean_input(request.POST.get('first_name_kana', ''))
        birth_date = clean_input(request.POST.get('birth_date', ''))
        gender = clean_input(request.POST.get('gender', ''))
        email = clean_input(request.POST.get('email', ''))
        phone = clean_input(request.POST.get('phone', ''))
        address = clean_input(request.POST.get('address', ''))
        education = clean_input(request.POST.get('education', ''))
        work_experience = clean_input(request.POST.get('work_experience', ''))
        qualifications = clean_input(request.POST.get('qualifications', ''))
        motivation = clean_input(request.POST.get('motivation', ''))
        self_pr = clean_input(request.POST.get('self_pr', ''))
        desired_start_date = clean_input(request.POST.get('desired_start_date', ''))
        remarks = clean_input(request.POST.get('remarks', ''))

        # === 必須項目チェック ===
        required_fields = [desired_position, last_name, first_name, last_name_kana,
                           first_name_kana, birth_date, gender, email, address,
                           education, work_experience, motivation, self_pr]
        if not all(required_fields):
            messages.error(request, '必須項目が未入力です。')
            return redirect('main:recruit_apply')

        # === 生年月日未来日チェック ===
        try:
            birth_date_obj = date.fromisoformat(birth_date)
            if birth_date_obj > date.today():
                messages.error(request, '生年月日に未来の日付は入力できません。')
                return redirect('main:recruit_apply')
        except ValueError:
            messages.error(request, '生年月日が不正です。')
            return redirect('main:recruit_apply')

        # === メール・電話形式チェック ===
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, 'メールアドレス形式が不正です。')
            return redirect('main:recruit_apply')
        if phone and not re.match(r"^[0-9\-+ ]*$", phone):
            messages.error(request, '電話番号形式が不正です。')
            return redirect('main:recruit_apply')

        # === メールヘッダーインジェクション防止 ===
        for field in [last_name, first_name, email, phone]:
            if "\n" in field or "\r" in field:
                messages.error(request, '不正な文字が入力されました。')
                return redirect('main:recruit_apply')

        # === 管理者宛メール本文 ===
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

        # === 応募者宛の確認メール本文 ===
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
            # メール送信
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=False)
            send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            messages.success(request, 'ご応募ありがとうございます。ご入力いただいたメールアドレスに確認メールを送信いたしました。')
        except Exception as e:
            messages.error(request, 'メール送信中にエラーが発生しました。')
            logger.error(f"メール送信エラー: {e}")

        return redirect('main:recruit_apply')

    return render(request, 'main/recruit_apply.html', {"RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY})
def news(request):
    return render(request, 'main/news.html')

import logging
import re

logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        # reCAPTCHAトークン検証
        recaptcha_token = request.POST.get('g-recaptcha-response', '')
        try:
            recaptcha_response = requests.post(
                "https://www.google.com/recaptcha/api/siteverify",
                data={
                    'secret': settings.RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_token
                },
                timeout=5
            ).json()
            if not recaptcha_response.get('success') or recaptcha_response.get('score', 0) < 0.5:
                messages.error(request, "reCAPTCHA認証に失敗しました。")
                logger.warning(f"reCAPTCHA failed: {recaptcha_response}")
                return redirect('main:contact')
        except Exception as e:
            messages.error(request, "reCAPTCHAサーバーエラーが発生しました。")
            logger.error(f"reCAPTCHA verification error: {e}")
            return redirect('main:contact')

        # 入力値サニタイズ
        def clean_input(value):
            return escape(value.strip())

        inquiry_type = clean_input(request.POST.get('inquiry_type', ''))
        company_name = clean_input(request.POST.get('company_name', ''))
        last_name = clean_input(request.POST.get('last_name', ''))
        first_name = clean_input(request.POST.get('first_name', ''))
        email = clean_input(request.POST.get('email', ''))
        phone = clean_input(request.POST.get('phone', ''))
        message_text = clean_input(request.POST.get('message', ''))

        # 必須項目チェック
        if not all([inquiry_type, last_name, first_name, email, message_text]):
            messages.error(request, "必須項目が未入力です。")
            return redirect('main:contact')

        # メールヘッダーインジェクション防止
        for field in [last_name, first_name, email, phone]:
            if "\n" in field or "\r" in field:
                messages.error(request, "不正な文字が入力されました。")
                return redirect('main:contact')

        # メール・電話形式チェック
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messages.error(request, "メールアドレス形式が不正です。")
            return redirect('main:contact')
        if phone and not re.match(r"^[0-9\-+ ]*$", phone):
            messages.error(request, "電話番号形式が不正です。")
            return redirect('main:contact')

        # メール送信（中身は元のまま）
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
            send_mail(admin_subject, admin_message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL], fail_silently=False)
            send_mail(user_subject, user_message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
            messages.success(request, 'お問い合わせありがとうございます。ご入力いただいたメールアドレスに確認メールを送信いたしました。')
        except Exception as e:
            messages.error(request, 'メール送信中にエラーが発生しました。')
            logger.error(f"メール送信エラー: {e}")

        return redirect('main:contact')

    return render(request, 'main/contact.html', {"RECAPTCHA_SITE_KEY": settings.RECAPTCHA_SITE_KEY})
