country_dict = {"Ukraine" : "Kyiv", "Italy" : "Rome", "Great Britain" : "London"}

country_list = ["Ukraine", "Italy", "Romania", "France"]

for cntr in country_list:

    if cntr in country_dict.keys():
        print(country_dict[cntr])
