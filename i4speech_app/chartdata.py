from .models import Textos, Autores, Escalafh, Escalamu, Escalasp, Escalagu, Escalain, Cr, Fh, Gu, Mu, Sp, Ocasiones, Ejes
import django.utils.encoding
import django.http.request


class ChartData():

    @staticmethod
    def chart_data(indfil, autfil , ocfil , ejefil):
        if 'indice' not in indfil.data == {}:
            data = {'autor': [],'cr':[], 'drilldown':[]}
        else:
             data = {'autor': [], 'drilldown':[]}
             if '1' in indfil.data.getlist('indice'): data.update({'cr': []})
             if '2' in indfil.data.getlist('indice'): data.update({'gu': []})
             if '3' in indfil.data.getlist('indice'): data.update({'fh': []})
             if '4' in indfil.data.getlist('indice'): data.update({'mu': []})
             if '5' in indfil.data.getlist('indice'): data.update({'sp': []})
        if  'nombre' not in autfil.data: lista_autores= Autores.objects.all().values('id')
        else: lista_autores= autfil.data.getlist('nombre')
        autores= Autores.objects.filter(pk__in=lista_autores)
        if 'ocasion' not in ocfil.data: lista_ocasiones = Ocasiones.objects.all().values('pk')
        else: lista_ocasiones= ocfil.data.getlist('ocasion')
        if 'eje' not in ejefil.data: lista_ejes = Ejes.objects.all().values('pk')
        else: lista_ejes = ejefil.data.getlist('eje')
        for autor in autores:
            au = django.utils.encoding.force_text(autor.nombre,'utf-8')
            data['autor'].append(au)
            data['drilldown'].append(au)
            if 'cr' in data.keys(): data['cr'].append(Cr.prom_cr(autor.id,lista_ocasiones, lista_ejes))
            if 'gu' in data.keys(): data['gu'].append(Gu.prom_gu(autor.id, lista_ocasiones, lista_ejes))
            if 'fh' in data.keys(): data['fh'].append(Fh.prom_fh(autor.id, lista_ocasiones, lista_ejes))
            if 'mu' in data.keys(): data['mu'].append(Mu.prom_mu(autor.id,lista_ocasiones, lista_ejes))
            if 'sp' in data.keys(): data['sp'].append(Sp.prom_sp(autor.id, lista_ocasiones, lista_ejes))
            
        return data

    @staticmethod
    def drilldowns(data, indfil, ocfil, ejefil):
        drilldown={'series':[]}
        for autor in data.get('autor'):
            serie = {'id': [], 'name': [], 'type':[], 'data': []}
            serie['id'] = autor
            if 'indice' not in indfil.data == {}:
                serie['name'] = 'CR'
            else:
                if '1' in indfil.data.getlist('indice'):  serie['name'] = 'CR'
                if '2' in indfil.data.getlist('indice'):  serie['name'] = 'GU'
                if '3' in indfil.data.getlist('indice'):  serie['name'] = 'FH'
                if '4' in indfil.data.getlist('indice'):  serie['name'] = 'MU'
                if '5' in indfil.data.getlist('indice'):  serie['name'] = 'SP'
            serie['type']= "column"
            if 'ocasion' not in ocfil.data and 'eje' not in ejefil.data:
                lista_textos = Textos.objects.filter(idautor__nombre=autor).order_by('fecha')
            else:
                if 'ocasion' not in ocfil.data and 'eje' in ejefil.data:
                    lista_textos = Textos.objects.filter(idautor__nombre=autor, ideje__in=ejefil.data['eje']).order_by('fecha')
                else:
                    if 'ocasion' in ocfil.data and 'eje' not in ejefil.data:
                        lista_textos = Textos.objects.filter(idautor__nombre=autor, idocasion__in=ocfil.data['ocasion']).order_by('fecha')
                    else:
                        lista_textos = Textos.objects.filter(idautor__nombre=autor, idocasion__in=ocfil.data['ocasion'],
                                             ideje__in=ejefil.data['eje']).order_by('fecha')
            if len(lista_textos) > 0:
                for texto in lista_textos:
                    if 'indice' not in indfil.data == {}: textodata = {'fecha': texto.fecha.__str__(), 'y': texto.cr.resultado, 'name':texto.titulo}
                    else:
                        if '1' in indfil.data.getlist('indice'):  textodata = {'fecha': texto.fecha.__str__(), 'y': texto.cr.resultado, 'name':texto.titulo}
                        if '2' in indfil.data.getlist('indice'):  textodata = {'fecha': texto.fecha.__str__(), 'y': texto.gu.resultado, 'name':texto.titulo}
                        if '3' in indfil.data.getlist('indice'):  textodata = {'fecha': texto.fecha.__str__(), 'y': texto.fh.resultado, 'name':texto.titulo}
                        if '4' in indfil.data.getlist('indice'):  textodata = {'fecha': texto.fecha.__str__(), 'y': texto.mu.resultado, 'name':texto.titulo}
                        if '5' in indfil.data.getlist('indice'):  textodata = {'fecha': texto.fecha.__str__(), 'y': texto.sp.resultado, 'name':texto.titulo}
                    serie['data'].append(textodata)
                drilldown['series'].append(serie)
        return drilldown