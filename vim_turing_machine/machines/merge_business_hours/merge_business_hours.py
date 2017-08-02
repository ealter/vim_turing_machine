"""Our tape is defined in multiple segments, each separated by a blank character.

INPUT<Blank>OUTPUT

This program solves the "Merge Business Hours" interview question: Given a
sorted list of possibly overlapping (opening, closing) hours, merge them.

Example: [[1, 5], [2, 3], [4, 6], [9, 11]] -> [[1, 6], [9, 11]]

We do this... on a turing machine.
"""
import itertools
import json
import sys

from vim_turing_machine.constants import BITS_PER_NUMBER
from vim_turing_machine.constants import BLANK_CHARACTER
from vim_turing_machine.constants import INITIAL_STATE
from vim_turing_machine.constants import VALID_CHARACTERS
from vim_turing_machine.constants import YES_FINAL_STATE
from vim_turing_machine.machines.merge_business_hours.decode_hours import decode_hours
from vim_turing_machine.machines.merge_business_hours.encode_hours import encode_hours
from vim_turing_machine.struct import BACKWARDS
from vim_turing_machine.struct import DO_NOT_MOVE
from vim_turing_machine.struct import FORWARDS
from vim_turing_machine.struct import StateTransition
from vim_turing_machine.turing_machine import TuringMachine


class MergeBusinessHoursGenerator(object):
    def __init__(self, num_bits=BITS_PER_NUMBER):
        self._num_bits = num_bits

    def merge_business_hours_transitions(self):
        """This is the main orchestration point of the program"""
        # This is the beginning of the loop that goes through the rest of the hours.
        CHECK_NEXT_SET_OF_HOURS = 'CheckNextSetOfHours'

        # We begin the program by copying the first hours pair into the output
        # array. At the end of this, the cursor will be at the end of the
        # output array.
        transitions = list(
            self.copy_bits_to_end_of_output(
                initial_state=INITIAL_STATE,
                num_bits=self._num_bits * 2,
                final_state=CHECK_NEXT_SET_OF_HOURS,
            )
        )

        BEGIN_COPY_NEXT_SET_OF_HOURS = 'CopyNextSetOfHours'
        BEGIN_COMPARISON = 'BeginComparison'

        # Then move back to the beginning of the input while checking if there is any input left
        transitions.extend(
            self.check_if_there_is_any_input_left(
                initial_state=CHECK_NEXT_SET_OF_HOURS,
                final_state=BEGIN_COPY_NEXT_SET_OF_HOURS,
            )
        )

        # Now it's time to copy the opening hours of the next pair.
        transitions.extend(
            self.copy_bits_to_end_of_output(
                initial_state=BEGIN_COPY_NEXT_SET_OF_HOURS,
                num_bits=self._num_bits,
                final_state=BEGIN_COMPARISON,
            )
        )

        OPEN_HOUR_IS_LESS_THAN = 'OpeningLessThan'
        OPEN_HOUR_IS_GREATER_THAN = 'OpeningGreaterThan'

        # Next we compare the closing hours of the previous pair with the
        # opening hours of the current pair.
        transitions.extend(
            self.compare_two_sequential_numbers(
                initial_state=BEGIN_COMPARISON,
                greater_than_or_equal_to_state=OPEN_HOUR_IS_LESS_THAN,
                less_than_state=OPEN_HOUR_IS_GREATER_THAN,
            )
        )

        transitions.extend(
            self.copy_closing_hour_without_merging(
                initial_state=OPEN_HOUR_IS_GREATER_THAN,
                final_state=CHECK_NEXT_SET_OF_HOURS,
            )
        )

        transitions.extend(
            self.copy_closing_hour_and_merge(
                initial_state=OPEN_HOUR_IS_LESS_THAN,
                final_state=CHECK_NEXT_SET_OF_HOURS,
            )
        )

        return transitions

    def copy_closing_hour_without_merging(self, initial_state, final_state):
        """Things are super simple if we don't need to merge the hours. We just need
        to copy over the closing hours from the input array.

        Precondition: we are at the end of the output array. The opening hours
            have already been copied. The opening hour is greater than the
            previous pair's closing hour.
        Postcondition: we are at the end of the output array
        """
        COPY_CLOSING_HOUR_WITHOUT_MERGING = 'CopyClosingHourWithoutMerging'

        # First move back to the beginning of the input array since the copy
        # function requires that.
        transitions = self.move_to_blank_spaces(
            initial_state=initial_state,
            final_state=COPY_CLOSING_HOUR_WITHOUT_MERGING,
            final_character=BLANK_CHARACTER,
            final_direction=FORWARDS,
            direction=BACKWARDS,
            num_blanks=2,
        )

        # Then just copy the closing hour from the input array to the output array.
        transitions.extend(
            self.copy_bits_to_end_of_output(
                initial_state=COPY_CLOSING_HOUR_WITHOUT_MERGING,
                num_bits=self._num_bits,
                final_state=final_state,
            )
        )

        return transitions

    def copy_closing_hour_and_merge(self, initial_state, final_state):
        """Call this if you need to merge in the 2nd set of hours.

        Precondition: we are at the end of the output array. The opening hours
            have already been copied. The opening hour is less than or equal to
            the previous pair's closing hour.
        Postcondition: we are at the end of the output array
        """
        MOVE_BACK_TO_BEGINNING_TO_COPY_CLOSING_HOUR = 'MoveToBeginningToCopyClosingHour'
        COPY_OVER_CLOSING_HOUR = 'CopyClosingHour'
        COMPARE_CLOSING_HOUR = 'CompareClosingHour'
        CLOSING_HOUR_IS_LARGER = 'ClosingHourIsLarger'
        CLOSING_HOUR_IS_NOT_LARGER = 'ClosingHourIsNotLarger'

        # If the opening hour is less than the closing hour of the previous pair,
        # then we discard that opening hour. So essentially, [2, 7, 5] becomes [2, 7].
        transitions = self.erase_number(
            initial_state=initial_state,
            final_state=MOVE_BACK_TO_BEGINNING_TO_COPY_CLOSING_HOUR,
        )

        # Move back to the beginning of the array.
        transitions.extend(
            self.move_to_blank_spaces(
                initial_state=MOVE_BACK_TO_BEGINNING_TO_COPY_CLOSING_HOUR,
                final_state=COPY_OVER_CLOSING_HOUR,
                final_character=BLANK_CHARACTER,
                final_direction=FORWARDS,
                direction=BACKWARDS,
                num_blanks=2,
            )
        )

        # Now after erasing that number, we need to copy over the closing hour so
        # that we can merge it in.
        transitions.extend(
            self.copy_bits_to_end_of_output(
                initial_state=COPY_OVER_CLOSING_HOUR,
                num_bits=self._num_bits,
                final_state=COMPARE_CLOSING_HOUR,
            )
        )

        # Now we take the max of the 2 pairs' closing hours.
        transitions.extend(
            self.compare_two_sequential_numbers(
                initial_state=COMPARE_CLOSING_HOUR,
                less_than_state=CLOSING_HOUR_IS_LARGER,
                greater_than_or_equal_to_state=CLOSING_HOUR_IS_NOT_LARGER,
            )
        )

        # If the closing hour is less than or equal to the previous closing hour, just nuke it.
        transitions.extend(
            self.erase_number(
                initial_state=CLOSING_HOUR_IS_NOT_LARGER,
                final_state=final_state,
            )
        )

        # But if the closing hour is greater than the previous closing hour, we
        # should overwrite that closing hour with our larger value.
        transitions.extend(
            self.replace_number(
                initial_state=CLOSING_HOUR_IS_LARGER,
                final_state=final_state,
            )
        )

        return transitions

    def noop_when_non_blank(self, state, direction):
        return (
            StateTransition(
                previous_state=state,
                previous_character='0',
                next_state=state,
                next_character='0',
                tape_pointer_direction=direction,
            ),
            StateTransition(
                previous_state=state,
                previous_character='1',
                next_state=state,
                next_character='1',
                tape_pointer_direction=direction,
            ),
        )

    def move_n_bits(self, initial_state, direction, final_state, num_bits):
        """Moves 'num_bits' in the specified direction. Errors if it encounters a
        blank space while doing so. Ends in the final_state."""
        def state_name(bit_index):
            if bit_index == 0:
                return initial_state
            elif bit_index == num_bits:
                return final_state
            else:
                return '{}MovingBit{}'.format(initial_state, bit_index)

        return itertools.chain.from_iterable([
            [
                StateTransition(
                    previous_state=state_name(bit_index),
                    previous_character=bit_value,
                    next_state=state_name(bit_index + 1),
                    next_character=bit_value,
                    tape_pointer_direction=(
                        direction
                        if bit_index < num_bits - 1
                        else DO_NOT_MOVE
                    ),
                )
                for bit_index in range(num_bits)
            ]
            for bit_value in ['0', '1']
        ])

    def move_to_blank_spaces(
        self,
        initial_state,
        final_state,
        final_character,
        final_direction,
        direction,
        num_blanks,
    ):
        """Moves along the array until it hits a certain number of blank spaces.

        :param str initial_state: The state used to trigger this code
        :param str final_state: The state we should finish with
        :param str final_character: The character we should write on that state transition
        :param int final_direction: Which direction we should move at the end
        :param int direction: Which direction we should search in
        :param int num_blanks: How many blanks to search for
        """

        def state_name(blank_num):
            return '{}Searching{}'.format(initial_state, blank_num)

        transitions = [
            # Rename our current state
            StateTransition(
                previous_state=initial_state,
                previous_character=character,
                next_state=state_name(blank_num=0),
                next_character=character,
                tape_pointer_direction=DO_NOT_MOVE,
            )
            for character in VALID_CHARACTERS
        ]

        for blank_num in range(num_blanks):
            transitions.extend(
                # If we're looking for the first blank, then keep going until we hit it
                self.noop_when_non_blank(state_name(blank_num=blank_num), direction=direction)
            )

            if blank_num == num_blanks - 1:
                # This is the last blank
                transitions.append(
                    StateTransition(
                        previous_state=state_name(blank_num),
                        previous_character=BLANK_CHARACTER,
                        next_state=final_state,
                        next_character=final_character,
                        tape_pointer_direction=final_direction,
                    )
                )
            else:
                # This is not the last blank
                transitions.append(
                    StateTransition(
                        previous_state=state_name(blank_num),
                        previous_character=BLANK_CHARACTER,
                        next_state=state_name(blank_num + 1),
                        next_character=BLANK_CHARACTER,
                        tape_pointer_direction=direction,
                    )
                )

        return transitions

    def copy_bits_to_end_of_output(self, initial_state, num_bits, final_state):
        """
        :param string initial_state: The state used before we start to move
        :param int num_bits: The number of bits to copy
        :param StateTransition final_state: The state to finish with when we are done copying

        Note: This overwrites the copied section with blanks.

        Precondition: We are at the beginning of the input array
        Postcondition: We are at the end of the output array

        :rtype: [StateTransition]
        """
        def state_name(bit_index):
            if bit_index == 0:
                return initial_state
            else:
                return '{}Copy{}'.format(initial_state, bit_index)

        def copy_bit(bit_index, bit_value):
            base_copying_state = '{}Bit{}'.format(state_name(bit_index + 1), bit_value)

            return [
                # Let's start copying the character. Note how we replace it with a blank.
                StateTransition(
                    previous_state=state_name(bit_index),
                    previous_character=bit_value,
                    next_state='{}Forward'.format(base_copying_state),
                    next_character=BLANK_CHARACTER,
                    tape_pointer_direction=FORWARDS,
                ),

                *self.move_to_blank_spaces(
                    initial_state='{}Forward'.format(base_copying_state),
                    # If we're on the last character, don't go backwards
                    final_state=(
                        '{}Backwards'.format(base_copying_state)
                        if bit_index < num_bits - 1
                        else final_state
                    ),
                    final_character=bit_value,
                    final_direction=DO_NOT_MOVE,
                    direction=FORWARDS,
                    num_blanks=2,
                ),
                *self.move_to_blank_spaces(
                    initial_state='{}Backwards'.format(base_copying_state),
                    final_state=state_name(bit_index + 1),
                    final_character=BLANK_CHARACTER,
                    final_direction=FORWARDS,
                    direction=BACKWARDS,
                    num_blanks=2,
                ),
            ]

        return itertools.chain.from_iterable(
            (
                *copy_bit(bit_index, bit_value='0'),
                *copy_bit(bit_index, bit_value='1'),
            )
            for bit_index in range(num_bits)
        )

    def compare_two_sequential_numbers(self, initial_state, greater_than_or_equal_to_state, less_than_state):
        """
        If the earlier number is greater than or equal to the later number, this
        will end in the greater_than_or_equal_to_state. If the earlier number is
        less than the later number, this will end in the less_than_state.

        Precondition: The cursor is at the end of the output array
        Postcondition: The cursor is at the end of the output array
        """
        # We can't directly transition into the >= or < states since we need to end
        # up at the end of the output array.
        FOUND_GREATER_THAN_OR_EQUAL_TO_STATE = '{}FoundGreaterThanOrEqualTo'.format(initial_state)
        FOUND_LESS_THAN_STATE = '{}FoundLessThan'.format(initial_state)

        def already_have_one_bit_state(bit_index, bit_value):
            """This means that we've read a 'bit_value' at 'bit_index'. We are
            currently searching for the equivalent bit in the other number."""
            return '{}BitIndex{}BitValue{}'.format(initial_state, bit_index, bit_value)

        def about_to_read_first_bit_state(bit_index):
            """This means that we're about to start reading/comparing the next bit
            index. We always immediately transition from this state to the
            'already_have_one_bit_state' after reading its value."""
            if bit_index == self._num_bits:
                # At this point, we know that the numbers are equal since we've compared every bit.
                return FOUND_GREATER_THAN_OR_EQUAL_TO_STATE
            else:
                return '{}BitIndex{}'.format(initial_state, bit_index)

        def about_to_compare_bits_state(bit_index, bit_value):
            """Our cursor is over the other bit we want to compare this one too."""
            return '{}BitIndex{}CompareWithBitValue{}'.format(initial_state, bit_index, bit_value)

        # Begin by moving to the beginning of the 2nd number.
        transitions = list(
            self.move_n_bits(
                initial_state=initial_state,
                direction=BACKWARDS,
                final_state=about_to_read_first_bit_state(bit_index=0),
                num_bits=self._num_bits,
            )
        )

        direction = BACKWARDS

        # Then begin comparing the digits one by one from largest to smallest
        for bit_index in range(self._num_bits):
            for bit_value in ['0', '1']:
                transitions.append(
                    # Read the current bit
                    StateTransition(
                        previous_state=about_to_read_first_bit_state(bit_index),
                        previous_character=bit_value,
                        next_state=already_have_one_bit_state(bit_index, bit_value),
                        next_character=bit_value,
                        tape_pointer_direction=direction,
                    )
                )

                # Then go to the equivalent bit in the other number. We already
                # moved 1 space in that direction.
                transitions.extend(
                    self.move_n_bits(
                        initial_state=already_have_one_bit_state(bit_index, bit_value),
                        direction=direction,
                        final_state=about_to_compare_bits_state(bit_index, bit_value),
                        num_bits=self._num_bits,
                    )
                )

                # We've already read the 2nd number and now we're comparing it to
                # the first. Now finally do the comparison
                transitions.append(
                    # If the numbers are equal
                    StateTransition(
                        previous_state=about_to_compare_bits_state(bit_index, bit_value),
                        previous_character=bit_value,
                        next_state=about_to_read_first_bit_state(bit_index + 1),
                        next_character=bit_value,
                        tape_pointer_direction=FORWARDS,
                    )
                )

                transitions.append(
                    # If the numbers are not equal
                    StateTransition(
                        previous_state=about_to_compare_bits_state(bit_index, bit_value),
                        previous_character=invert_bit(bit_value),
                        next_state=(
                            FOUND_GREATER_THAN_OR_EQUAL_TO_STATE
                            if (
                                (bit_value == '1' and direction == FORWARDS) or
                                (bit_value == '0' and direction == BACKWARDS)
                            )
                            else FOUND_LESS_THAN_STATE
                        ),
                        next_character=invert_bit(bit_value),
                        tape_pointer_direction=invert_direction(direction),
                    )
                )

            direction = invert_direction(direction)

        # After we've determined the answer, we need to move to the end of the output array
        transitions.extend(
            self.move_to_blank_spaces(
                initial_state=FOUND_GREATER_THAN_OR_EQUAL_TO_STATE,
                final_state=greater_than_or_equal_to_state,
                final_character=BLANK_CHARACTER,
                final_direction=BACKWARDS,
                direction=FORWARDS,
                num_blanks=1,
            )
        )

        transitions.extend(
            self.move_to_blank_spaces(
                initial_state=FOUND_LESS_THAN_STATE,
                final_state=less_than_state,
                final_character=BLANK_CHARACTER,
                final_direction=BACKWARDS,
                direction=FORWARDS,
                num_blanks=1,
            )
        )

        return transitions

    def erase_number(self, initial_state, final_state):
        """Erases the number under the cursor by replacing it with blanks.

        Precondition: The cursor is at the end of that number
        Postcondition: The cursor is right before the beginning of that number
        """
        def state_name(bit_index):
            if bit_index == 0:
                return initial_state
            elif bit_index == self._num_bits:
                return final_state
            else:
                return '{}ErasingBit{}'.format(initial_state, bit_index)

        transitions = []

        for bit_index in range(self._num_bits):
            for bit_value in ['0', '1']:
                transitions.append(
                    StateTransition(
                        previous_state=state_name(bit_index),
                        previous_character=bit_value,
                        next_state=state_name(bit_index + 1),
                        next_character=BLANK_CHARACTER,
                        tape_pointer_direction=BACKWARDS,
                    )
                )

        return transitions

    def replace_number(self, initial_state, final_state):
        """Replaces the 2nd to last number with the last number. So, [1, 5, 7] would become [1, 7].

        Precondition: The cursor is at the end of the output array
        Postcondition: The cursor is at the end of the output array
        """
        def need_to_read_bit(bit_index):
            if bit_index == 0:
                return initial_state
            elif bit_index == self._num_bits:
                return final_state
            else:
                return '{}ReadingBitIndexToMove{}'.format(initial_state, bit_index)

        def read_bit(bit_index, bit_value):
            return '{}ReadingBitIndexToMove{}Bit{}'.format(initial_state, bit_index, bit_value)

        def overwrite_bit(bit_index, bit_value):
            return '{}OverwritingBitIndex{}Bit{}'.format(initial_state, bit_index, bit_value)

        def move_back_to_end(bit_index):
            return '{}ReplacingNumberMovingBackToEnd{}'.format(initial_state, bit_index)

        transitions = []
        for bit_index in range(self._num_bits):
            for bit_value in ['0', '1']:
                # Start by reading the bit under the cursor. Replace it with a blank.
                transitions.append(
                    StateTransition(
                        previous_state=need_to_read_bit(bit_index),
                        previous_character=bit_value,
                        next_state=read_bit(bit_index, bit_value),
                        next_character=BLANK_CHARACTER,
                        tape_pointer_direction=BACKWARDS,
                    )
                )

                # Then go to the equivalent bit in the other number.
                transitions.extend(
                    self.move_n_bits(
                        initial_state=read_bit(bit_index, bit_value),
                        direction=BACKWARDS,
                        final_state=overwrite_bit(bit_index, bit_value),
                        num_bits=self._num_bits,
                    )
                )

                # Then overwrite the current bit with the stored bit
                transitions.extend(
                    StateTransition(
                        previous_state=overwrite_bit(bit_index, bit_value),
                        previous_character=bit_value_we_are_reading,
                        next_state=move_back_to_end(bit_index),
                        next_character=bit_value,
                        tape_pointer_direction=FORWARDS,
                    )
                    for bit_value_we_are_reading in ['0', '1']
                )

            # Lastly move back to the end of the output array
            transitions.extend(
                self.move_to_blank_spaces(
                    initial_state=move_back_to_end(bit_index),
                    final_state=need_to_read_bit(bit_index + 1),
                    final_character=BLANK_CHARACTER,
                    final_direction=BACKWARDS,
                    direction=FORWARDS,
                    num_blanks=1,
                )
            )

        return transitions

    def check_if_there_is_any_input_left(self, initial_state, final_state):
        """
        Precondition: We are at the end of the output array
        Postcondition: We are at the beginning of the input array

        If there is no more input left, this ends the program
        """
        CHECK_IF_ANY_HOURS_LEFT = '{}CheckIfAnyHoursLeft'.format(initial_state)

        # Then move back to the beginning of the input
        transitions = self.move_to_blank_spaces(
            initial_state=initial_state,
            final_state=CHECK_IF_ANY_HOURS_LEFT,
            final_character=BLANK_CHARACTER,
            final_direction=FORWARDS,
            direction=BACKWARDS,
            num_blanks=2,
        )

        # If we moved back 2 blanks and still ended on a blank, then there is
        # nothing left in the input because we hit 2 blanks in a row.
        transitions.append(
            StateTransition(
                previous_state=CHECK_IF_ANY_HOURS_LEFT,
                previous_character=BLANK_CHARACTER,
                next_state=YES_FINAL_STATE,
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            )
        )

        # If we did not find a blank, then we just chill where we are
        transitions.extend(
            StateTransition(
                previous_state=CHECK_IF_ANY_HOURS_LEFT,
                previous_character=bit_value,
                next_state=final_state,
                next_character=bit_value,
                tape_pointer_direction=DO_NOT_MOVE,
            )
            for bit_value in ['0', '1']
        )

        return transitions


def invert_bit(bit_value):
    if bit_value == '0':
        return '1'
    elif bit_value == '1':
        return '0'
    else:
        raise AssertionError('Invalid bit {}'.format(bit_value))


def invert_direction(direction):
    if direction == BACKWARDS:
        return FORWARDS
    elif direction == FORWARDS:
        return BACKWARDS
    else:  # pragma: no cover
        raise AssertionError('Invalid direction {}'.format(direction))


if __name__ == '__main__':
    input_string = json.loads(sys.argv[1])
    num_bits = int(sys.argv[2])

    initial_tape = encode_hours(input_string, num_bits)

    gen = MergeBusinessHoursGenerator(num_bits)
    merge_business_hours = TuringMachine(gen.merge_business_hours_transitions(), debug=True)
    merge_business_hours.run(initial_tape=initial_tape, max_steps=5000)

    print(decode_hours(''.join(merge_business_hours.tape), num_bits))
