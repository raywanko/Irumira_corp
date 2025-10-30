document.addEventListener('DOMContentLoaded', function() {
    // -------------------------
    // ハンバーガーメニュー
    // -------------------------
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');

    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
            document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
        });

        document.addEventListener('click', function(e) {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // -------------------------
    // サブメニューの開閉
    // -------------------------
    const navParents = document.querySelectorAll('.nav-parent');
    navParents.forEach(parent => {
        parent.addEventListener('click', function(e) {
            e.stopPropagation();
            const submenu = this.parentElement;
            submenu.classList.toggle('active');
        });
    });

    // -------------------------
    // ヘッダーのスクロール効果
    // -------------------------
    const header = document.querySelector('.header');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // -------------------------
    // メッセージの自動非表示
    // -------------------------
    const messages = document.querySelectorAll('.alert');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            message.style.opacity = '0';
            message.style.transform = 'translateY(-20px)';
            setTimeout(() => message.remove(), 500);
        }, 5000);
    });

    // -------------------------
    // スムーススクロール
    // -------------------------
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // -------------------------
    // 生年月日未来日チェック
    // -------------------------
    const birthDateInput = document.querySelector('input[name="birth_date"]');
    if (birthDateInput) {
        birthDateInput.addEventListener('change', function() {
            const today = new Date();
            const inputDate = new Date(this.value);
            if (inputDate > today) {
                alert('生年月日に未来の日付は入力できません。');
                this.value = '';
            }
        });
    }

    // -------------------------
    // フォーム送信 + reCAPTCHA v3 + スコア警告
    // -------------------------
    const forms = document.querySelectorAll('.contact-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();

            // 必須項目チェック
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#e74c3c';
                    setTimeout(() => { field.style.borderColor = '#e0e0e0'; }, 2000);
                }
            });
            if (!isValid) {
                alert('必須項目を全て入力してください。');
                return;
            }

            // reCAPTCHA 実行
            if (typeof grecaptcha !== 'undefined') {
                grecaptcha.execute('{{ RECAPTCHA_SITE_KEY }}', { action: 'submit' }).then(function(token) {
                    // 隠しフィールドにトークンをセット
                    let recaptchaInput = form.querySelector('input[name="g-recaptcha-response"]');
                    if (!recaptchaInput) {
                        recaptchaInput = document.createElement('input');
                        recaptchaInput.type = 'hidden';
                        recaptchaInput.name = 'g-recaptcha-response';
                        form.appendChild(recaptchaInput);
                    }
                    recaptchaInput.value = token;

                    // フォーム送信（ここでサーバー側でスコアチェック）
                    fetch(form.action, {
                        method: 'POST',
                        body: new FormData(form),
                        headers: { 'X-Requested-With': 'XMLHttpRequest' }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // 正常送信
                            alert('送信が完了しました。ありがとうございます。');
                            form.reset();
                        } else if (data.score_low) {
                            // スコア低すぎ
                            alert('送信がブロックされました。不正なアクセスの可能性があります。');
                        } else {
                            // その他エラー
                            alert('送信中にエラーが発生しました。');
                        }
                    })
                    .catch(() => {
                        alert('送信中にネットワークエラーが発生しました。');
                    });
                });
            } else {
                alert('reCAPTCHA が読み込まれていません。');
            }
        });
    });

    // -------------------------
    // Googleマップのレスポンシブ対応
    // -------------------------
    const mapIframe = document.querySelector('.google-map-iframe');
    if (mapIframe) {
        let isTouch = false;
        mapIframe.addEventListener('touchstart', function() { isTouch = true; });
        mapIframe.addEventListener('touchend', function() { setTimeout(() => { isTouch = false; }, 300); });
    }

    // -------------------------
    // 画像の遅延読み込み
    // -------------------------
    if ('loading' in HTMLImageElement.prototype) {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => { img.src = img.dataset.src; });
    } else {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    imageObserver.unobserve(img);
                }
            });
        });
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // -------------------------
    // ページローディングアニメーション
    // -------------------------
    window.addEventListener('load', function() {
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.5s ease';
        setTimeout(() => { document.body.style.opacity = '1'; }, 100);
    });
});

// -------------------------
// 事業内容ページのスクロールアニメーション
// -------------------------
document.addEventListener('DOMContentLoaded', function() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    const serviceBlocks = document.querySelectorAll('.service-block');
    serviceBlocks.forEach(block => observer.observe(block));
});
