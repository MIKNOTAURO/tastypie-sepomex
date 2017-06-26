# -*- coding: utf-8 -*-

"""
d_codigo Código Postal asentamiento
d_asenta Nombre asentamiento
d_tipo_asenta Tipo de asentamiento (Catálogo SEPOMEX)
d_CP Código Postal de la Administración Postal que reparte al asentamiento
c_oficina Código Postal de la Administración Postal que reparte al asentamiento
c_tipo_asenta Clave Tipo de asentamiento (Catálogo SEPOMEX)
id_asenta_cpcons Identificador único del asentamiento (nivel municipal)
d_zona Zona en la que se ubica el asentamiento (Urbano/Rural)

D_mnpio Nombre Municipio (INEGI, Marzo 2013)
c_mnpio Clave Municipio (INEGI, Marzo 2013)

d_estado Nombre Entidad (INEGI, Marzo 2013)
c_estado Clave Entidad (INEGI, Marzo 2013)

d_ciudad Nombre Ciudad (Catálogo SEPOMEX)
c_cve_ciudad Clave Ciudad (Catálogo SEPOMEX)

c_CP Campo Vacio
"""

import json

from django.urls import reverse_lazy
from django.test import TestCase
from django.core.management import call_command


class ApiTest(TestCase):
    def setUp(self):
        call_command('loadmxstates')
        self.kwargs = {
            'api_name': 'v1', 'resource_name': 'mxestado'
        }
        self.cli_options = {'content_type': 'application/json', 'follow': True}

    def test_tilde_in_nombre(self):
        kwargs = {'pk': 15}
        kwargs.update(self.kwargs)
        url = reverse_lazy('api_dispatch_detail', kwargs=kwargs)
        response = self.client.get(url, **self.cli_options)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('México' in response.content)

    def test_total_states(self):
        url = reverse_lazy('api_dispatch_list', kwargs=self.kwargs)
        response = self.client.get(url, **self.cli_options)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(32, json.loads(response.content)['meta']['total_count'])
