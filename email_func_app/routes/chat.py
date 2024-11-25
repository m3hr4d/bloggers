from flask import Blueprint, jsonify, request, render_template, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from email_func_app import db
from email_func_app.models.chat import Conversation, ServiceTicket
from email_func_app.models.message import Message
from email_func_app.decorators import check_user_type

chat = Blueprint('chat', __name__)

@chat.route('/conversations')
@login_required
def get_conversations():
    """Get all conversations for the current user"""
    conversations = Conversation.query.filter(
        or_(
            Conversation.influencer_id == current_user.id,
            Conversation.business_id == current_user.id
        )
    ).all()
    
    return render_template('chat/conversations.html', conversations=conversations)

@chat.route('/conversation/<int:conversation_id>')
@login_required
def get_conversation(conversation_id):
    """Get a specific conversation and its messages"""
    conversation = Conversation.query.get_or_404(conversation_id)
    
    # Check if user is part of the conversation
    if current_user.id not in [conversation.influencer_id, conversation.business_id]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Mark all unread messages as read
    unread_messages = Message.query.join(conversation_messages).filter(
        and_(
            conversation_messages.c.conversation_id == conversation_id,
            Message.recipient_id == current_user.id,
            Message.read == False
        )
    ).all()
    
    for message in unread_messages:
        message.read = True
    
    db.session.commit()
    
    return render_template('chat/conversation.html', 
                         conversation=conversation,
                         messages=conversation.messages)

@chat.route('/message/send', methods=['POST'])
@login_required
def send_message():
    """Send a new message in a conversation"""
    data = request.json
    conversation_id = data.get('conversation_id')
    content = data.get('content')
    
    if not all([conversation_id, content]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conversation = Conversation.query.get_or_404(conversation_id)
    
    # Check if user is part of the conversation
    if current_user.id not in [conversation.influencer_id, conversation.business_id]:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Determine recipient
    recipient_id = conversation.influencer_id if current_user.id == conversation.business_id else conversation.business_id
    
    message = Message(
        sender_id=current_user.id,
        recipient_id=recipient_id,
        subject="Chat Message",
        body=content,
        read=False
    )
    
    db.session.add(message)
    conversation.messages.append(message)
    db.session.commit()
    
    return jsonify({
        'id': message.id,
        'content': message.body,
        'created_at': message.created_at.isoformat(),
        'sender_id': message.sender_id,
        'read': message.read
    })

@chat.route('/ticket/create', methods=['POST'])
@login_required
@check_user_type('business')
def create_service_ticket():
    """Create a new service ticket"""
    data = request.json
    required_fields = ['influencer_id', 'service_type', 'description']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if conversation exists or create new one
    conversation = Conversation.query.filter(
        and_(
            Conversation.influencer_id == data['influencer_id'],
            Conversation.business_id == current_user.id
        )
    ).first()
    
    if not conversation:
        conversation = Conversation(
            influencer_id=data['influencer_id'],
            business_id=current_user.id
        )
        db.session.add(conversation)
        db.session.flush()
    
    ticket = ServiceTicket(
        conversation_id=conversation.id,
        service_type=data['service_type'],
        description=data['description']
    )
    
    # Create a message to notify the influencer
    message = Message(
        sender_id=current_user.id,
        recipient_id=data['influencer_id'],
        subject=f"New Service Request: {data['service_type']}",
        body=data['description'],
        read=False
    )
    
    db.session.add(ticket)
    db.session.add(message)
    conversation.messages.append(message)
    db.session.commit()
    
    return jsonify({
        'id': ticket.id,
        'conversation_id': conversation.id,
        'service_type': ticket.service_type,
        'status': ticket.status
    })

@chat.route('/ticket/<int:ticket_id>/update-status', methods=['POST'])
@login_required
@check_user_type('influencer')
def update_ticket_status(ticket_id):
    """Update the status of a service ticket"""
    data = request.json
    new_status = data.get('status')
    
    if not new_status or new_status not in ['accepted', 'rejected', 'negotiating']:
        return jsonify({'error': 'Invalid status'}), 400
    
    ticket = ServiceTicket.query.get_or_404(ticket_id)
    conversation = ticket.conversation
    
    # Check if user is the influencer for this ticket
    if current_user.id != conversation.influencer_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    ticket.status = new_status
    
    # Create a status update message
    message = Message(
        sender_id=current_user.id,
        recipient_id=conversation.business_id,
        subject=f"Service Request Status Update: {ticket.service_type}",
        body=f"Status updated to: {new_status}",
        read=False
    )
    
    db.session.add(message)
    conversation.messages.append(message)
    db.session.commit()
    
    return jsonify({
        'id': ticket.id,
        'status': ticket.status
    })
