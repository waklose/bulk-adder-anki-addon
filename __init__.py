from . import config, dictionary

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect, askUser
# import all of the Qt GUI library
from aqt.qt import *


def populate_deck_menu(menu):
    """Clears and populates the menu with the current deck list."""
    menu.clear()  # Clear the menu items to refresh the list

    # Get a list of all deck names and IDs from the DeckNameId object
    decks = mw.col.decks.all_names_and_ids()  # Access the 'items' attribute

    for deck in decks:
        deck_name = deck.name  # Get the name of the deck
        deck_id = deck.id  # Get the ID of the deck (if needed for other operations)
        card_count = mw.col.decks.card_count(deck_id, include_subdecks=True)  # Get the number of cards in the deck

        # Create an action for each deck
        action = QAction(deck_name, menu)
        action.triggered.connect(lambda checked, name=deck_name, id=deck_id, count=card_count: on_deck_selected(name, id, count))
        menu.addAction(action)

def on_deck_selected(deck_name, deck_id, card_count):
    """Placeholder function triggered when a deck is selected."""
    if not askUser(f"Bulk add kanji information to {card_count} cards in deck: '{deck_name}'?"):
        return
    
    all_note_ids = mw.col.decks.cids(deck_id, children=True)  # Get all card IDs in the deck
    for note_id in all_note_ids:
        note = mw.col.get_card(note_id).note()  # Get the note object
        # Get the field names
        note_keys = note.keys()
        if not (config.source_field in note_keys and config.target_field in note_keys):
            showInfo(f"Note {note_id} in deck {deck_name} does not have the required fields.")
            return
        kanji_word = note[config.source_field]
        kanji_info = dictionary.search_word(kanji_word)
        if kanji_info is None:
            #showInfo(f"No kanji information found for '{kanji_word}'")
            continue
        note[config.target_field] = kanji_info
        mw.col.update_note(note)
    showInfo(f"Bulk addition to deck {deck_name} complete.")




def add_deck_menu_to_tools():
    """Creates a menu in Tools that displays all decks when clicked."""
    # Create the main menu
    deck_menu = QMenu("Bulk Adder", mw)
    deck_menu.aboutToShow.connect(lambda: populate_deck_menu(deck_menu))  # Populate on hover/click

    # Add the menu to the Tools menu
    mw.form.menuTools.addMenu(deck_menu)

# Run the function to add the menu when Anki starts
add_deck_menu_to_tools()