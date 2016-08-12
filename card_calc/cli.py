import click
import sys


formats={
        26: {'fac_bits': 8, 'no_bits': 16, 'parity_bits': 12, 'preamble':'000000100000000001' },
        37: {'fac_bits': 16, 'no_bits': 19, 'parity_bits': 18, 'preamble':'0000000'}
        }

@click.command()
@click.argument('facility_code', type=int, required=True)
@click.argument('card_no', type=int, required=True)
@click.argument('bits', default=26, required=False)
def main(bits, facility_code, card_no):
    """Calculate hex value of HID Prox card from card, site and bit values."""
    click.echo('\nCalculating {} bit card, facility code {} and card number {}.\n'.format(bits, facility_code, card_no))
    card = formats[bits] 
    p_bits = card['parity_bits']
    # Check that the values supplied aren't invalid for the card bit length.
    if (facility_code.bit_length() > card['fac_bits']) | ( card_no.bit_length() > card['no_bits']):
        sys.exit('Error: There are too many bits in the card or facility code to fit on the specified card size.')
    # Turn the facility and card number into a string of bits
    card_temp = "{:0{}b}{:0{}b}".format(facility_code, card['fac_bits'], card_no, card['no_bits'])
    # Calculate the parity by counting the ones in the string
    even = card_temp[:p_bits].count('1') % 2 
    odd = (card_temp[-p_bits:].count('1') % 2) ^ 1
    card_temp = "{}{}{}".format(even, card_temp, odd) 
    # Add the preamble 
    card_final = int("{}{}".format(card['preamble'], card_temp), 2)
    # Output results
    click.secho(' {:{}}{:{}}'.format(facility_code, card['fac_bits'], card_no, card['no_bits']))
    click.secho('P', fg='blue', nl=False)
    click.secho('F'*card['fac_bits'], fg='white', bold=True, nl=False)
    click.secho('C'*card['no_bits'], fg='green', nl=False)
    click.secho('P', fg='red')
    click.secho(card_temp)
    click.secho(' ' + 'E'*p_bits, fg='blue')
    click.secho('{:>{}}'.format("O"*p_bits, (bits-1)), fg='red')
    click.secho("\nHex value for Proxmark: {:09x}\n".format(card_final), fg='yellow', bold=True)
