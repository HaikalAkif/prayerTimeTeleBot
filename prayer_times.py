from datetime import datetime

class PrayerTimes:

    hijrah: str
    day: str
    date: datetime
    imsak: datetime
    subuh: datetime
    syuruk: datetime
    zohor: datetime
    asar: datetime
    maghrib: datetime
    isyak: datetime

    def __init__(self, pt_json: dict):
        self.hijrah = pt_json['hijri']
        self.day = pt_json['day']
        self.date = self.__convert_to_date__(pt_json['date'])
        self.imsak = self.__convert_to_time__(pt_json['imsak'])
        self.subuh = self.__convert_to_time__(pt_json['fajr'])
        self.syuruk = self.__convert_to_time__(pt_json['syuruk'])
        self.zohor = self.__convert_to_time__(pt_json['dhuhr'])
        self.asar = self.__convert_to_time__(pt_json['asr'])
        self.maghrib = self.__convert_to_time__(pt_json['maghrib'])
        self.isyak = self.__convert_to_time__(pt_json['isha'])

    def __convert_to_time__(self, time: str):
        return datetime.strptime(time, '%H:%M:%S') 

    def __convert_to_date__(self, date: str):
        return datetime.strptime(date, '%d-%b-%Y')