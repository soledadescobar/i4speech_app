from .models import Textos, Autores, Escalafh, Escalamu, Escalasp, Escalagu, Escalain, Cr, Fh, Gu, Mu, Sp


class ChartData(object):

    def todos_los_promedios():
        data = {'autor': [], 'sp': [],'fh': [], 'gu': [], 'mu': [], 'cr': []}

        autores = Autores.objects.all()

        for autor in autores:
            data['autor'].append(autor.nombre)
            data['sp'].append(Sp.prom_sp().filter(idtexto__idautor_id=autor.id))


        return data
