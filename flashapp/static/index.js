function deleteDeck(deck_id) {
  fetch("/delete-deck", {
    method: "POST",
    body: JSON.stringify({ deck_id: deck_id }),
  }).then((_res) => {
    window.location.href = "/decks";
  });
}

function deleteCard(card_id, deck_id) {
  fetch("/delete-card", {
    method: "POST",
    body: JSON.stringify({ card_id: card_id }),
  }).then((_res) => {
    window.location.href = "/decks/"+deck_id;
  });
}

function myFunction() {
  var x = document.getElementById("ans");
  x.classList.toggle('hidden');
}

function resetCardScore(card_id, deck_id) {
  fetch("/reset-cardscore", {
    method: "POST",
    body: JSON.stringify({ card_id: card_id }),
  }).then((_res) => {
    window.location.href = "/decks/"+deck_id+"/review/"+card_id;
  });
}
