hijri_months = [
    "Muharram",
    "Safar",
    "Rabiul-awal",
    "Rabiul-akhir",
    "Jamadil-awal",
    "Jamadil-akhir",
    "Rejab",
    "Syaaban",
    "Ramadhan",
    "Syawal",
    "Zul-qaeda",
    "Zul-hijjah"
]

zone_config = {
    "SGR01": "Gombak, Petaling, Sepang, Hulu Langat, Hulu Selangor, S.Alam",
    "SGR02": "Kuala Selangor, Sabak Bernam",
    "SGR03": "Klang, Kuala Langat",
    "WLY01": "Kuala Lumpur, Putrajaya",
}

class BotConfig():
    
    def get_malay_hijri_month(month_index: str):
        return hijri_months[int(month_index) - 1]
    
    def get_available_locations():
        return [
            {
                "code": "SGR01",
                "name": "SGR01 - Gombak, Petaling, Sepang, Hulu Langat, Hulu Selangor, S.Alam"
            },
            {
                "code": "SGR02",
                "name": "SGR02 - Kuala Selangor, Sabak Bernam"
            },
            {
                "code": "SGR03",
                "name": "SGR03 - Klang, Kuala Langat"
            },
            {
                "code": "WLY01",
                "name": "WLY01 - Kuala Lumpur, Putrajaya"
            },
        ]
        
    def get_zone_full_name(code: str):
        return zone_config.get(code)