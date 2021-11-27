from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from flashapp.database import db, User, Card, Deck
from sqlalchemy import and_
import json

views = Blueprint('views', __name__)


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html', user=current_user)


@views.route('/dashboard')
@login_required
def dashboard():
    deck=0
    return render_template('dashboard.html', user=current_user, deck=deck)


@views.route('/decks', methods=['GET', 'POST'])
@login_required
def deck_creation():
    if request.method == 'POST':
        deck_name = request.form.get('deck')

        deck = Deck.query.filter_by(deck_name=deck_name).first()

        if deck:
            flash('Deck already exists.', category='error')
        else:
            new_deck = Deck(deck_name=deck_name, user_id=current_user.id)
            db.session.add(new_deck)
            db.session.commit()
            flash('Deck created!', category='success')

    return render_template("deck_manage.html", user=current_user)


@views.route('/decks/<deck_id>', methods=['GET', 'POST'])
@login_required
def deck_details(deck_id):
    deck = Deck.query.filter_by(deck_id=deck_id).first()
    card = Card.query.filter_by(deck_id=deck_id).all()

    if request.method == 'POST':
        deck_new_name = request.form.get('deck')

        new_deck = Deck.query.filter_by(deck_name=deck_new_name).first()

        if new_deck:
            flash('This Deck name already exists.', category='error')
        else:

            deck.deck_name = deck_new_name
            db.session.commit()
            flash('Deck updated!', category='success')

    return render_template("deck_details.html", user=current_user, deck_details=(deck, card))


@views.route('/delete-deck', methods=['POST'])
def delete_deck():
    deck = json.loads(request.data)
    deck_id = deck['deck_id']
    deck_obj = Deck.query.get(deck_id)
    if deck_obj:
        db.session.delete(deck_obj)
        db.session.commit()
        flash('Deck deleted.', category='success')
    return jsonify({})


@views.route('/decks/<deck_id>/card', methods=['GET', 'POST'])
@login_required
def card_creation(deck_id):
    if request.method == 'POST':
        card_ques = request.form.get('card-ques')
        card_ans = request.form.get('card-ans')
        diff_level = request.form.get('card-diff')

        if card_ques is None or len(card_ques) == 0:
            flash("Question cannot be empty", category='error')

        elif card_ans is None or len(card_ans) == 0:
            flash("Review cannot be empty", category='error')

        else:
            card = Card(deck_id=deck_id, card_ques=card_ques, card_ans=card_ans, diff_level=diff_level)
            db.session.add(card)
            db.session.commit()
            flash('Card created!', category='success')

    return render_template("card_manage.html", user=current_user, deck_id=deck_id)


@views.route('/decks/<deck_id>/cards/<card_id>', methods=['GET', 'POST'])
@login_required
def card_details(deck_id, card_id):
    card = Card.query.filter_by(card_id=card_id).all()

    if request.method == 'POST':
        new_card_ques = request.form.get('card-ques')
        new_card_ans = request.form.get('card-ans')
        new_diff_level = request.form.get('card-diff')

        if new_card_ques is None or len(new_card_ques) == 0:
            flash("Question cannot be empty", category='error')

        elif new_card_ans is None or len(new_card_ans) == 0:
            flash("Review cannot be empty", category='error')

        else:
            card.card_ques = new_card_ques
            card.card_ans = new_card_ans
            card.diff_level = new_diff_level
            db.session.commit()
            flash('Card updated!', category='success')

    return render_template("card_details.html", user=current_user, card=card, deck_id=deck_id)


@views.route('/delete-card', methods=['POST'])
def delete_card():
    card = json.loads(request.data)
    card_id = card['card_id']
    card_obj = Card.query.get(card_id)
    if card_obj:
        db.session.delete(card_obj)
        db.session.commit()
        flash('Card deleted.', category='success')
    return jsonify({})
