# -- coding: utf-8 --
#
# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import settings

from adrog1_cpr_opslag_lokal import (
    get_person_numbers_from_address,
    get_persons_from_address
)

dependencies = {
    'service_endpoint': settings.SP_SERVICE_ENDPOINT,
    'certificate': settings.SP_CERTIFICATE,
    'soap_request_envelope': settings.SP_SOAP_REQUEST_ENVELOPE,
    'system': settings.SP_SYSTEM,
    'user': settings.SP_USER,
    'service_agreement': settings.SP_SERVICE_AGREEMENT,
    'service': settings.SP_SERVICE
}

test_address = {
    'street_code': '3611',
    'house_no': '15',
    'zip_code': '8240',
    'floor': '',
    'door': ''
}


# adrs01_json_response = get_persons_from_address(
#     dependencies_dict=dependencies,
#     address_dict=test_address,
#     response_format='json'
# )
#
# print(adrs01_json_response)


# adrs01_xml_response = get_persons_from_address(
#     dependencies_dict=dependencies,
#     address_dict=test_address,
#     response_format='xml'
# )
# test_output = open('output_test.xml', 'w')
# test_output.write(adrs01_xml_response)
#
# Pretty print XML
# 1) $ sudo apt install xmllint
# 2) $ xmllint --format output_test.xml


# Returns a list
# person_numbers_from_adress = get_person_numbers_from_address(
#     dependencies_dict=dependencies,
#     address_dict=test_address
# )
#
# print(person_numbers_from_adress)
