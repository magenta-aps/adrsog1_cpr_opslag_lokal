# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import html
import json
import requests
import settings
import xmltodict
import lxml.etree as ET

from jinja2 import Template

# TODO: return the raw XML, or prettyfied JSON.


def get_persons_from_address(dependencies_dict, address_dict, response_format):

    if validate_address(address_dict):

        adrog1_xml_response = call_gctp_service_adrsog1(
            dependencies_dict=dependencies_dict,
            address_dict=address_dict
        )

        if response_format == 'json':

            adrog1_response_dict = xmltodict.parse(adrog1_xml_response)
            return json.dumps(adrog1_response_dict, sort_keys=True, indent=4)

        elif response_format == 'xml':

            return adrog1_xml_response

        else:

            return 'ADRSOG1 Response Format Error'


def get_person_numbers_from_address(dependencies_dict, address_dict):
    """The function returns person numbers from a given address."""

    adrog1_response = call_gctp_service_adrsog1(
        dependencies_dict=dependencies_dict,
        address_dict=address_dict
    )

    person_numbers = filter_person_numbers_from_address(adrog1_response)

    return person_numbers


# TODO: Optimize
def call_gctp_service_adrsog1(dependencies_dict, address_dict):
    """Returns string xml of persons."""

    if validate_address(address_dict):

        soap_request_envelope = dependencies_dict.get('soap_request_envelope')

        with open(soap_request_envelope, "r") as filestream:

            template_string = filestream.read()

        xml_template = Template(template_string)

        gctp_elements = generate_gctp_field_elements(
            address_dict=address_dict
        )

        populated_template = xml_template.render(
            service_agreement=dependencies_dict.get('service_agreement'),
            system=dependencies_dict.get('system'),
            user=dependencies_dict.get('user'),
            service=dependencies_dict.get('service'),
            search_param_fields=gctp_elements
        )

        # print('TEMPLATE:\n{}'.format(populated_template))

        # response will throw UnicodeEncodeError otherwise(?).
        latin_1_encoded_xml = populated_template.encode('latin-1')

        response = requests.post(
            data=latin_1_encoded_xml,
            url=dependencies_dict.get('service_endpoint'),
            cert=dependencies_dict.get('certificate')
        )

        persons_on_address_xml = html.unescape(response.text)

        return persons_on_address_xml

    else:

        return {
            'Error': 'Something is wrong with address:\t{}'.format(
                address_dict
            )
        }


# NOTE: This validation is just an assumption. May need some testing
def validate_address(address_dict):
    """Checks if minimum required address attributes are present in the dict.
    return : boolean"""

    validate_address = False

    street_code = address_dict.get('street_code')
    house_no = address_dict.get('house_no')
    zip_code = address_dict.get('zip_code')

    if street_code and house_no and zip_code:

        validate_address = True

    return validate_address


def filter_person_numbers_from_address(address):
    """Parses adrsog1 object to a dict, and appends a person_number(PNR) to a
    list ONLY if the civilian status of the citizen equals '01'.
    return : list
    """

    # Pointing to 'Table' element as root  - consider recursive function.
    root = ET.fromstring(address)[0][0][0][0][0][0][0][1][0][0]

    person_numbers = []
    for row in root:
        temp_dict = {}
        for field in row:
            field_dict = field.attrib
            temp_dict[field_dict.get('r')] = field_dict.get('v')
            person_numbers.append(temp_dict.get('PNR'))
    return person_numbers


def generate_gctp_field_elements(address_dict):
    """ Dynamically builds a string of gctp xml field elements from the keys in
    address which contain data.
    return : string."""

    street_code = padding_prefix_zeros(address_dict['street_code'], 4)
    fields = '<Field r="VEJK" v="' + street_code + '"/>'

    house_no = format_house_number_for_adrsog1(address_dict['house_no'])
    fields += '<Field r="HNR" v="' + house_no + '"/>'

    fields += '<Field r="POST" v="' + address_dict['zip_code'] + '"/>'

    if address_dict['floor']:
        floor = format_floor_for_adrsog1(address_dict['floor'])
        fields += '<Field r="ETAG" v="' + floor + '"/>'

    if address_dict['door']:
        door = format_door_for_adrsog1(address_dict['door'])
        fields += '<Field r="SIDO" v="' + door + '"/>'

    return fields


# TODO: Make one generic function that takes len(input) as secondary paramater.
# Lengths are defined here:
# https://cprdocs.atlassian.net/wiki/download/attachments/51156205/Adresses%C3%B8gning%20-%20ADRSOG1.pdf?api=v2

def padding_prefix_zeros(street_attr, street_attr_len):
    if street_attr_len > 0 and street_attr_len < 5:
        diff = street_attr_len - street_attr_len
        for i in range(diff):
            street_attr_len = '0' + street_attr_len
        return street_attr_len
    else:
        return 'street_attr_len was: {}. 5 > street_attr_len > 0'.format(
            street_attr_len
        )


def format_street_code_for_adrsog1(street_code):
    length = len(street_code)
    if length > 0 and length < 5:
        diff = 4 - length
        for i in range(diff):
            street_code = '0' + street_code
        return street_code
    else:
        return None


def format_house_number_for_adrsog1(house_no_dawa):
    house_no = house_no_dawa
    length = len(house_no)
    if length > 0 and length < 5:
        diff = 4 - length
        for i in range(diff):
            house_no = '0' + house_no
        return house_no
    else:
        return None


def format_floor_for_adrsog1(floor_dawa):
    floor = floor_dawa
    length = len(floor)
    if length > 0 and length < 3:
        diff = 2 - length
        for i in range(diff):
            floor = '0' + floor
        return floor
    else:
        return None


def format_door_for_adrsog1(door_dawa):
    door = door_dawa
    length = len(door)
    if 0 < length < 5:
        diff = 4 - length
        for i in range(diff):
            door = '0' + door
        return door
    else:
        return None
