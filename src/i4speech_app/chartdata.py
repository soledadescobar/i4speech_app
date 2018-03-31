# -*- coding: utf-8 -*-
from .models import Textos, Autores, Escalafh, Escalamu, Escalasp, Escalagu, Escalain, Cr, Fh, Gu, Mu, Sp
import django.utils


class ChartData():

    @staticmethod
    def todos_los_promedios():
        data = {'autor': [], 'sp': [], 'fh': [], 'gu': [], 'mu': [], 'cr': []}

        autores = Autores.objects.all()

        for autor in autores:
            data['autor'].append(autor.nombre.encode('ascii'))
            data['sp'].append(Sp.prom_sp(autor.id))
            data['fh'].append(Fh.prom_fh(autor.id))
            data['gu'].append(Gu.prom_gu(autor.id))
            data['mu'].append(Mu.prom_mu(autor.id))
            data['cr'].append(Cr.prom_cr(autor.id))


        return data
