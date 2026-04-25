from flask import render_template, flash, redirect, url_for, request, g
from flask import Blueprint
from core.flask_shortcuts.decorators import login_required
from core.models import MailSubscription, MailBlock, db
from blueprints.mail.forms import SubscriptionForm
import settings

bp = Blueprint('mail', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    sub = MailSubscription.query.filter_by(user_id=g.user.id).first()
    form = SubscriptionForm()

    if request.method == 'GET' and sub:
        form.send_days.data = sub.send_days.split(',')
        form.send_hour.data = sub.send_hour
        form.is_active.data = sub.is_active

    if form.validate_on_submit():
        if not sub:
            sub = MailSubscription(user_id=g.user.id)
            db.session.add(sub)

        sub.send_days = ','.join(form.send_days.data)
        sub.send_hour = form.send_hour.data
        sub.is_active = form.is_active.data

        selected = request.form.getlist('categories')
        MailBlock.query.filter_by(subscription_id=sub.id).delete()
        for cat in selected:
            if cat in settings.POST_CATEGORIES:
                count = int(request.form.get(f'count_{cat}', 2))
                db.session.add(MailBlock(subscription=sub, category=cat, post_count=min(max(count, 2), 3)))

        db.session.commit()
        flash('Настройки рассылки сохранены!', 'Сообщение')
        return redirect(url_for('mail.index'))

    selected_cats = {b.category: b.post_count for b in (sub.blocks if sub else [])}
    return render_template('mail_all.html', title='Рассылки', form=form,
                           categories=settings.POST_CATEGORIES, selected_cats=selected_cats)
