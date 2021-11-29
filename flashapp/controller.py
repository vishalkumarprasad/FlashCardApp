"""Module to control all routes"""

import json
from datetime import datetime
from random import choice

from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user

from flashapp.database import db, Card, Deck

views = Blueprint('views', __name__)

score_dict = {'Easy': 1, 'Medium': 2, 'Difficult': 3}


@views.route('/')
@views.route('/home')
def home():
    return render_template('home.html', user=current_user)


@views.route('/dashboard')
@login_required
def dashboard():
    dict_final_score = {}
    dict_random_card = {}
    for deck in current_user.decks:
        tot_score = full_tot_score = 0
        for card in deck.cards:
            ind_score = card.score
            tot_score += ind_score
            full_ind_score = score_calc(1, card.diff_level)
            full_tot_score += full_ind_score
        final_score = str(tot_score)+'/'+str(full_tot_score)
        random_card = choice(deck.cards) if len(deck.cards) > 0 else None
        dict_final_score[deck] = final_score
        dict_random_card[deck] = random_card

    return render_template('dashboard.html', user=current_user, score=dict_final_score, random_card=dict_random_card)


@views.route('/decks', methods=['GET', 'POST'])
@login_required
def deck_creation():
    if request.method == 'POST':
        deck_name = request.form.get('deck')

        deck = Deck.query.filter_by(deck_name=deck_name).first()

        if deck and current_user.id == deck.user_id:
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

        if new_deck and current_user.id == new_deck.user_id:
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
    card = Card.query.filter_by(card_id=card_id).first()

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


def score_calc(score, diff_level):
    cum_score = score_dict.get(diff_level)*score
    return cum_score


@views.route('/decks/<deck_id>/review/<card_id>', methods=['GET', 'POST'])
@login_required
def deck_review(deck_id, card_id):
    deck = Deck.query.filter_by(deck_id=deck_id).first()
    card = Card.query.filter_by(card_id=card_id).first()
    max_score = score_dict.get(card.diff_level)
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer is None or len(user_answer) == 0:
            flash("Answer cannot be empty", category='error')
        elif (user_answer.strip()).lower() == (card.card_ans.strip()).lower():
            card.score = max_score
            deck.review_dt = datetime.now()
            db.session.commit()
            flash(f'Correct Answer. You scored {card.score} points!', category='success')
        else:
            flash(f'Wrong Answer. Please review!', category='error')

    next_card = choose_next_card(deck, card)

    return render_template("review.html", user=current_user, deck=deck, card=card, max_score=max_score, next_card=next_card)


@views.route('/reset-cardscore', methods=['POST'])
def reset_cardscore():
    card = json.loads(request.data)
    card_id = card['card_id']
    card_obj = Card.query.get(card_id)
    if card_obj:
        card_obj.score = 0
        db.session.commit()
        flash('Card Score reset.', category='success')
    return jsonify({})


def choose_next_card(deck, card):
    easy_cards = []
    med_cards = []
    diff_cards = []
    chosen_card = None
    for ind_card in deck.cards:
        if ind_card != card:
            if ind_card.diff_level == 'Easy':
                easy_cards.append(ind_card)
            elif ind_card.diff_level == 'Medium':
                med_cards.append(ind_card)
            else:
                diff_cards.append(ind_card)
    if len(easy_cards) > 0 or len(med_cards) > 0 or len(diff_cards) > 0:
        if card.score == 0:
            chosen_card = choice(next(cards for cards in [easy_cards, med_cards, diff_cards] if len(cards) > 0))
        elif card.score == 1:
            chosen_card = choice(next(cards for cards in [med_cards, diff_cards, easy_cards] if len(cards) > 0))
        else:
            chosen_card = choice(next(cards for cards in [diff_cards, easy_cards, med_cards] if len(cards) > 0))
    return chosen_card

