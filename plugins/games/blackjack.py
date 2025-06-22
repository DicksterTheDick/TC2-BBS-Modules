import random, json, os
import logging

STATE_FILE = "blackjack_state.json" # File to store game states for each player

def deal_card():
    """Returns a random card."""
    cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
    return random.choice(cards)

def calculate_score(cards):
    """
    Calculates the current score from a list of cards.
    Handles Ace (11) conversion to 1 if the score exceeds 21.
    Returns 0 for a natural Blackjack (2 cards totaling 21).
    """
    if sum(cards) == 21 and len(cards) == 2:
        return 0  # Represents a Blackjack

    score = sum(cards)
    while 11 in cards and score > 21:
        cards.remove(11)
        cards.append(1) # Change Ace from 11 to 1
        score = sum(cards)
    return score

def load_state():
    """
    Loads the game state from the JSON file.
    Returns an empty dictionary if the file does not exist or is corrupted.
    """
    logging.info(f"BLACKJACK_DEBUG: Attempting to load state from {STATE_FILE}")
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                state_data = json.load(f)
                logging.info(f"BLACKJACK_DEBUG: Successfully loaded state: {state_data}")
                return state_data
        except json.JSONDecodeError as e:
            logging.error(f"BLACKJACK_ERROR: JSONDecodeError when loading state from {STATE_FILE}: {e}")
            return {}
        except Exception as e:
            logging.error(f"BLACKJACK_ERROR: Unexpected error loading state from {STATE_FILE}: {e}")
            return {}
    logging.info(f"BLACKJACK_DEBUG: State file {STATE_FILE} not found. Returning empty state.")
    return {}

def save_state(state):
    """
    Saves the current game state to the JSON file.
    """
    logging.info(f"BLACKJACK_DEBUG: Attempting to save state to {STATE_FILE}: {state}")
    try:
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=4)
        logging.info(f"BLACKJACK_DEBUG: State saved successfully to {STATE_FILE}")
    except Exception as e:
        logging.error(f"BLACKJACK_ERROR: Failed to save state to {STATE_FILE}: {e}")

def start_game(username):
    """
    Starts a new BlackJack game for the given user.
    Initializes player and dealer hands and saves the state.
    """
    logging.info(f"BLACKJACK_DEBUG: Starting new game for user {username}")
    state = load_state()
    player_cards = [deal_card(), deal_card()]
    dealer_cards = [deal_card()]
    state[str(username)] = {
        "player_cards": player_cards,
        "dealer_cards": dealer_cards,
        "status": "playing"
    }
    save_state(state)
    return (f"{username}: Your cards: {player_cards} (score: {calculate_score(player_cards)}).\n"
            f"Dealer shows: {dealer_cards[0]}. Reply 'hit' or 'stay'.")

def hit(username):
    """
    Handles a "hit" action from the player.
    Deals a new card to the player. Checks for bust.
    """
    logging.info(f"BLACKJACK_DEBUG: User {username} chose 'hit'.")
    state = load_state()
    if str(username) not in state:
        logging.warning(f"BLACKJACK_DEBUG: No game in progress found for user {username}. Current state keys: {state.keys()}")
        return "No game in progress. Please start a new game from the menu."

    player_cards = state[str(username)]["player_cards"]
    player_cards.append(deal_card())
    score = calculate_score(player_cards)
    state[str(username)]["player_cards"] = player_cards

    if score > 21:
        logging.info(f"BLACKJACK_DEBUG: User {username} busted with score {score}.")
        del state[str(username)]
        save_state(state)
        # MODIFIED: Add end-game prompt after losing
        return f"{username}: 💥 You went over 21 with {player_cards} (score: {score}). You lose!\nType 'deal' to start new game, or [X] to Exit."
    else:
        save_state(state)
        return f"{username}: Your cards: {player_cards} (score: {score}). Reply 'hit' or 'stay'."

def stay(username):
    """
    Handles a "stay" action from the player.
    Dealer takes cards until score is 17 or more, then compares scores.
    """
    logging.info(f"BLACKJACK_DEBUG: User {username} chose 'stay'.")
    state = load_state()
    if str(username) not in state:
        logging.warning(f"BLACKJACK_DEBUG: No game in progress found for user {username}. Current state keys: {state.keys()}")
        return "No game in progress. Please start a new game from the menu."

    player_cards = state[str(username)]["player_cards"]
    dealer_cards = state[str(username)]["dealer_cards"]

    while calculate_score(dealer_cards) < 17:
        logging.info(f"BLACKJACK_DEBUG: Dealer hits. Current dealer cards: {dealer_cards}, score: {calculate_score(dealer_cards)}")
        dealer_cards.append(deal_card())

    player_score = calculate_score(player_cards)
    dealer_score = calculate_score(dealer_cards)

    logging.info(f"BLACKJACK_DEBUG: Game ended for user {username}. Player score: {player_score}, Dealer score: {dealer_score}")
    del state[str(username)]
    save_state(state)

    result_message = compare(player_score, dealer_score)
    # MODIFIED: Add end-game prompt to the final result message
    return (f"{username}: Your final cards: {player_cards} (score: {player_score})\n"
            f"Dealer's cards: {dealer_cards} (score: {dealer_score})\n{result_message}\n"
            f"Type 'deal' to start new game, or [X] to Exit.")

def compare(player_score, dealer_score):
    """
    Compares player's and dealer's scores to determine the game outcome.
    """
    if player_score > 21:
        return "❌ You lose!"
    elif dealer_score > 21:
        return "✅ Dealer busted. You win!"
    elif player_score == dealer_score:
        return "🤝 It's a draw!"
    elif player_score == 0:
        return "🂡 Blackjack! You win!"
    elif dealer_score == 0:
        return "🂡 Dealer has Blackjack! You lose!"
    elif player_score > dealer_score:
        return "✅ You win!"
    else:
        return "❌ You lose!"

def handle_message(username, message_text):
    """
    Main function to handle incoming messages for the BlackJack game logic.
    Routes messages to the appropriate game action (deal, hit, stay).
    This function is designed to be called by the main BBS message processor.
    """
    message_text_lower = message_text.lower().strip()
    logging.info(f"BLACKJACK_DEBUG: handle_message called for user {username} with message '{message_text}'")

    # If the message is explicitly "deal", always start a new game.
    if message_text_lower == "deal":
        logging.info(f"BLACKJACK_DEBUG: Received 'deal'. Starting new game for {username}.")
        return start_game(username)

    state = load_state()
    if str(username) in state:
        logging.info(f"BLACKJACK_DEBUG: Game in progress for {username}. Processing as in-game command.")
        if message_text_lower == "hit":
            return hit(username)
        elif message_text_lower == "stay":
            return stay(username)
        elif message_text_lower == "x": # Allow 'x' to be handled here during game
            # Although message_processing.py will catch 'x' when in BLACKJACK_GAME state,
            # for robustness, handle it here by effectively ending the game.
            if str(username) in state:
                del state[str(username)] # Clear game state
                save_state(state)
            # Returning None here will make message_processing.py handle the 'x'
            # as a menu exit, which is the desired behavior.
            return None
        else:
            player_cards = state[str(username)]["player_cards"]
            dealer_cards_hidden = state[str(username)]["dealer_cards"][0]
            return (f"{username}: Invalid move. Your cards: {player_cards} (score: {calculate_score(player_cards)}).\n"
                    f"Dealer shows: {dealer_cards_hidden}. Reply 'hit' or 'stay'.")
    else:
        logging.info(f"BLACKJACK_DEBUG: No active game or 'deal' command for {username}. Not handling message. Returning None.")
        return None

