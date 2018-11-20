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
from requests_pkcs12 import post

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

        # response will throw UnicodeEncodeError otherwise(?).
        latin_1_encoded_xml = populated_template.encode('latin-1')

        response = post(
                dependencies_dict.get('service_endpoint'), 
                pkcs12_filename=dependencies_dict.get('certificate'),
                pkcs12_password=dependencies_dict.get('cert_passphrase'),
                data=latin_1_encoded_xml,
                )

        persons_on_address_xml = html.unescape(response.text)

        return persons_on_address_xml

    else:

        return {
            'Error': 'Something is wrong with address:\t{}'.format(
                address_dict
            )
        }


def validate_address(address_dict):
    """Checks if minimum required address attributes are present in address_dict.
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
    """Dynamically builds a string of gctp xml field elements from the keys in
    address which contain data.
    return : string."""

    street_code = padding_prefix_zeroes(address_dict['street_code'], 4)
    fields = '<Field r="VEJK" v="' + street_code + '"/>'

    house_no = padding_prefix_zeroes(address_dict['house_no'], 4)
    fields += '<Field r="HNR" v="' + house_no + '"/>'

    fields += '<Field r="POST" v="' + address_dict['zip_code'] + '"/>'

    if address_dict['floor']:
        floor = padding_prefix_zeroes(address_dict['floor'], 2)
        fields += '<Field r="ETAG" v="' + floor + '"/>'

    if address_dict['door']:
        door = padding_prefix_zeroes(address_dict['door'], 4)
        fields += '<Field r="SIDO" v="' + door + '"/>'

    return fields


def padding_prefix_zeroes(street_attr, street_attr_len):
    """Dynamically prefixes address a given attribute with zeroes."""
    if street_attr_len > 0 and street_attr_len < 5:
        diff = street_attr_len - len(street_attr)
        for i in range(diff):
            street_attr = '0' + street_attr
        return street_attr
    else:
        return 'street_attr_len was: {}. 5 > street_attr_len > 0'.format(
            street_attr_len
        )
