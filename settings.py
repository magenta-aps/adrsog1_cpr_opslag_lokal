# Copyright (c) 2017, Magenta ApS
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

import os
from dotenv import load_dotenv
from os.path import join, dirname

# Get .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SP_SERVICE_ENDPOINT = os.environ.get('SP_SERVICE_ENDPOINT')

SP_CERTIFICATE = os.environ.get('SP_CERTIFICATE')

SP_CERTIFICATE_PASSPHRASE = os.environ.get('SP_CERTIFICATE_PASSPHRASE')

SP_SOAP_REQUEST_ENVELOPE = os.environ.get('SP_SOAP_REQUEST_ENVELOPE')

SP_SYSTEM = os.environ.get('SP_SYSTEM')

SP_USER = os.environ.get('SP_USER')

SP_SERVICE_AGREEMENT = os.environ.get('SP_SERVICE_AGREEMENT')

SP_SERVICE = os.environ.get('SP_SERVICE')
