import smtplib
import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime, timedelta
from core.logger import log


def _build_blocks(subscription):
    from core.models import Post
    cutoff = datetime.utcnow() - timedelta(hours=2)
    blocks = []
    for block in subscription.blocks:
        posts = Post.query.filter(
            Post.category == block.category,
            Post.created_at >= cutoff
        ).order_by(Post.created_at.desc()).limit(block.post_count).all()

        parsed = []
        for p in posts:
            lines = p.data.strip().splitlines()
            headline = lines[0].lstrip('#').strip() if lines else ''
            summary_lines = [l for l in lines[1:] if l.strip() and not l.startswith('[')]
            summary = ' '.join(summary_lines[:2])
            link = ''
            for l in lines:
                if l.startswith('[') and '](http' in l:
                    link = l.split('](')[1].rstrip(')')
                    break
            parsed.append({'headline': headline, 'summary': summary, 'link': link})

        title = settings.POST_CATEGORIES.get(block.category, {}).get('readable', block.category)
        blocks.append({'title': title, 'posts': parsed})
    return blocks


def _render_email(blocks):
    from flask import render_template
    now = datetime.now().strftime('%d.%m.%Y %H:%M')
    return render_template('mail_email.html', blocks=blocks, now=now)


def send_newsletters(app):
    with app.app_context():
        from core.models import MailSubscription
        now = datetime.now()
        weekday = str(now.weekday())
        hour = now.hour

        subs = MailSubscription.query.filter_by(is_active=True).all()
        for sub in subs:
            days = sub.send_days.split(',')
            if weekday not in days or sub.send_hour != hour:
                continue
            if not sub.user.email:
                continue

            blocks = _build_blocks(sub)
            if not any(b['posts'] for b in blocks):
                continue

            html_content = _render_email(blocks)
            _send(sub.user.email, html_content)


def _send(to_email, html_content):
    if not settings.MAIL_SERVER or not settings.MAIL_USERNAME:
        log.warning('Mail not configured, skipping send')
        return

    msg = MIMEMultipart()
    msg['From'] = settings.MAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = f'Новости hell-0 — {datetime.now().strftime("%d.%m.%Y %H:%M")}'
    msg.attach(MIMEText('Ваша новостная рассылка во вложении.', 'plain', 'utf-8'))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(html_content.encode('utf-8'))
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename='news.html')
    msg.attach(part)

    try:
        with smtplib.SMTP(settings.MAIL_SERVER, int(settings.MAIL_PORT), timeout=15) as s:
            s.starttls()
            s.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            s.sendmail(settings.MAIL_FROM, to_email, msg.as_string())
        log.info(f'Email sent to {to_email}')
    except Exception as e:
        log.error(f'Email send failed to {to_email}: {e}')
