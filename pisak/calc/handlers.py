"""
Speller application specific handlers.
"""
import subprocess
import os

import pisak
from pisak import signals, sound_effects
from pisak.calc import widgets


@signals.registered_handler("calc/scroll_up")
def scroll_up(text_box):
    """
    Scroll the text field up.

    :param text_box: text box.
    """
    text_box.scroll_up()


@signals.registered_handler("calc/scroll_down")
def scroll_down(text_box):
    """
    Scroll the text field down.

    :param text_box: text box.
    """
    text_box.scroll_down()


@signals.registered_handler("calc/undo")
def undo(text_box):
    """
    Undo the last operation applied to a text box.

    :param text_box: undoable text box.
    """
    text_box.revert_operation()


@signals.registered_handler("calc/nav_right")
def nav_right(text_box):
    """
    Move text cursor forward for one position.

    :param text_box: text box.
    """
    text_box.move_cursor_forward()


@signals.registered_handler("calc/nav_left")
def nav_left(text_box):
    """
    Move text cursor backward for one position.

    :param text_box: text box.
    """
    text_box.move_cursor_backward()

@signals.registered_handler("calc/new_document")
def new_document(text_box):
    """
    Remove the whole text from the text buffer and clear the text box.

    :param text_box: text box.
    """
    text_box.clear_all()


@signals.registered_handler("calc/text_to_speech")
def text_to_speech(text_box):
    """
    Read the text loud.

    :param text_box: text box.
    """
    text = text_box.get_text()
    if text:
        synth = sound_effects.Synthesizer(text)
        if pisak.app.window.input_group.middleware == "scanning" and \
                pisak.app.window.pending_group is not None:
            synth.read_and_call(pisak.app.window.pending_group.start_cycle)
        else:
            synth.read()


@signals.registered_handler("calc/backspace")
def backspace(text_box):
    """
    Delete the one last character from the text buffer.

    :param text_box: text box.
    """
    text_box.delete_char()


@signals.registered_handler("calc/space")
def space(text_box):
    """
    Insert space in the end of the text buffer.

    :param text_box: text box.
    """

    text_box.type_text(" ")

@signals.registered_handler("calc/enter")
def enter(text_box):
    """
    Insert enter in the end of the text buffer.

    :param text_box: text box.
    """
    text_box.move_to_new_line()


@signals.registered_handler("calc/new_line")
def new_line(text_box):
    """
    Begin a new line of text.

    :param text_box: text box.
    """
    text_box.move_to_new_line()

@signals.registered_handler("calc/unset_toggled_state_on_select")
def unset_toggled_state_on_select(button):
    """
    Automatically unset toggled state of the button after selecting one
    of the keyboard keys.

    :param button: speller button instance.
    """
    keyboard_panel = button.related_object
    key_bag = []
    _find_and_get_keys(keyboard_panel, key_bag)
    for key in key_bag:
        try:
            key.disconnect_by_func(unset_toggled_state)
        except TypeError:
            pass
        key.connect_object("clicked", unset_toggled_state, button)


@signals.registered_handler("calc/unset_toggled_state")
def unset_toggled_state(button):
    """
    Unset toggled state of the button.

    :param button: speller button instance.
    """
    if button.get_toggled():
        button.set_toggled(False)
    try:
        keyboard_panel = button.related_object
        key_bag = []
        _find_and_get_keys(keyboard_panel, key_bag)
        for key in key_bag:
            try:
                key.disconnect_by_func(unset_toggled_state)
            except TypeError:
                pass
    except AttributeError:
        pass


@signals.registered_handler("calc/set_toggled_state")
def set_toggled_state(button):
    """
    Set toggled state of the button.

    :param button: speller button instance.
    """
    if not button.get_toggled():
        button.set_toggled(True)


@signals.registered_handler("calc/switch_toggled_state")
def switch_toggled_state(button):
    """
    Set or unset toggled state of the button.

    :param button: speller button instance.
    """
    if button.get_toggled():
        button.set_toggled(False)
    else:
        button.set_toggled(True)

@signals.registered_handler("calc/evaluate")
def evaluate(text_box):
    """
    Save the current text buffer content to a text file.
    Open a dialog window.

    :param pop_up: dialog window.
    """
    calc_input = text_box.get_text()
    try:
        calc_output = eval(calc_input)
        text_box.clear_all()
        text_box.type_text(str(calc_output))
    except:
        #TODO
        pass

@signals.registered_handler("calc/root")
def root(text_box):
    """
    Save the current text buffer content to a text file.
    Open a dialog window.

    :param pop_up: dialog window.
    """
    calc_input = text_box.get_text()
    try:
        calc_output = eval(calc_input)**(1/2.)
        text_box.clear_all()
        text_box.type_text(str(calc_output))
    except:
        #TODO
        pass