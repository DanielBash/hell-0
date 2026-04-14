"""Менеджер сообщений"""


# -- импортирование модулей
from flask import flash, g, request, redirect, url_for
from flask import Blueprint, render_template
from core.models import User, db, MailMessage
from .forms import MessageForm
from sqlalchemy import or_
from core.flask_shortcuts.decorators import login_required
import settings


bp = Blueprint('messages', __name__)


@bp.route('/filter', methods=['GET', 'POST'])
@login_required
def filter():
    form = MessageForm()
    
    if form.validate_on_submit():
        reciever = User.query.filter_by(username=form.data['reciever_username']).first()
        
        if not reciever:
            flash('Получатель ну существует.', 'Неудача')
            return redirect(url_for('messages.filter'))
        
        if not g.user.get_permission('SEND_MAIL_MESSAGES'):
            flash('Вам нельзя отправлять сообщения', 'Неудача')
            return redirect(url_for('messages.filter'))
        
        mail_message = MailMessage(content=form.data['content'], receiver_id=reciever.id, sender_id=g.user.id, subject=form.data['subject'])
        db.session.add(mail_message)
        db.session.commit()
        
        flash('Успешная доставка!', 'Успех')
        
        return redirect(url_for('messages.filter'))
    
    page = request.args.get("page", 1, type=int)

    pagination = MailMessage.query\
        .filter(
            or_(
                MailMessage.sender_id == g.user.id,
                MailMessage.receiver_id == g.user.id
            )
        )\
        .order_by(MailMessage.sent_at.desc())\
        .paginate(page=page, per_page=settings.MESSAGES_PAGINATION)

    messages = pagination.items
    
    return render_template(
        "messages.html",
        messages=messages,
        pagination=pagination,
        title='Сообщения',
        form=form
    )


@bp.route('/view/<int:id>', methods=['GET'])
@login_required
def message(id):
    message = MailMessage.query.get_or_404(id)
    
    if message.sender_id == g.user.id or message.receiver_id == g.user.id:
        return render_template(
        "message.html",
        message=message,
        title='Сообщение',
    )
    
    return redirect(url_for('main.index'))