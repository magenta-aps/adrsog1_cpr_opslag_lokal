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
    'cert_passphrase': settings.SP_CERTIFICATE_PASSPHRASE,
    'soap_request_envelope': settings.SP_SOAP_REQUEST_ENVELOPE,
    'system': settings.SP_SYSTEM,
    'user': settings.SP_USER,
    'service_agreement': settings.SP_SERVICE_AGREEMENT,
    'service': settings.SP_SERVICE
}


test_address = {
    'street_code': '0866',
    'house_no': '095',
    'zip_code': '9240',
    'floor': '01',
    'door': 'mf'
}

# Get a list of test-cpr numbers which exists the demo environment.
# Should return ['0707614285', '0103922852']
adrs01_json_response = get_persons_from_address(
    dependencies_dict=dependencies,
    address_dict=test_address,
    response_format='xml'
)

#print(adrs01_json_response)


# adrs01_xml_response = get_persons_from_address(
#     dependencies_dict=dependencies,
#     address_dict=test_address,
#     response_format='xml'
# )
# test_output = open('output_test.xml', 'w')
# test_output.write(adrs01_xml_response)

# Pretty print XML
# 1) $ sudo apt install xmllint
# 2) $ xmllint -format output_test.xml


# Returns a list
# person_numbers_from_adress = get_person_numbers_from_address(
#     dependencies_dict=dependencies,
#     address_dict=test_address
# )
#
# print(person_numbers_from_adress)
