import csv
from datetime import datetime, timedelta

class DolarMEP:
    DATE_FORMAT = "%d/%m/%Y"
    COTIZACIONES = {}
    MIN_DATE = None

    def str2mepdate(self, strdate):
        return datetime.strptime(strdate, self.DATE_FORMAT)

    def mepdate2str(self, date):
        return datetime.strftime(date, self.DATE_FORMAT)

    def __init__(self, filename= "dolar_mep.csv") -> None:
        with open(filename) as csvfile:
            cotizaciones = csv.reader(csvfile, delimiter=';')
            for cotizacion in cotizaciones:
                if cotizacion[0] != "Fecha":
                    fecha = cotizacion[0]
                    valor = cotizacion[1]
                    self.COTIZACIONES[fecha] = float(valor)             
        self.MIN_DATE = self.str2mepdate(fecha)

    def find_mep(self, date):
        cotizacion = None
        strdate = self.mepdate2str(date)
        if strdate in self.COTIZACIONES:
            cotizacion = self.COTIZACIONES[strdate]
        else:
            while cotizacion is None and date > self.MIN_DATE:
                date = date - timedelta(days=1)
                strdate = self.mepdate2str(date)
                if strdate in self.COTIZACIONES:
                    cotizacion =  self.COTIZACIONES[strdate]
        return cotizacion


    