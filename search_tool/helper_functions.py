from sqlalchemy import select, or_

from models import Provider, Licence, StandardGeographicClassification

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def fun_search_provider(sesh, x, print_results=True):
    query = select(Provider) \
            .where(Provider.provider_name.like("%%%s%%" % x.lower().strip()))

    result = list(sesh.scalars(query))

    pad_1 = max([len(i.provider_name) for i in result])
    pad_2 = max([len(i.uid) for i in result])

    if print_results:
        print(f'{color.BOLD}{"Provider Name": <{pad_1}}\t{"UID": <{pad_2}}\tURL{color.END}')
        for i in result:
            print(f"{i.provider_name: <{pad_1}}\t{i.uid: <{pad_2}}\t{i.provider_url}")    

    return result

def fun_search_licence(sesh, x, print_results=True):
    qstr = "%%%s%%" % x.lower().strip("/").strip()
    query = select(Licence) \
            .where(
                or_(
                    Licence.licence_url.like(qstr),
                    Licence.attribution.like(qstr)
                )
            )

    result = list(sesh.scalars(query))

    pad_1 = max([len(i.uid) for i in result])
    pad_2 = max([len(i.licence_url) for i in result])

    if print_results:
        print(f'{color.BOLD}{"UID": <{pad_1}}\t{"URL": <{pad_2}}\tAttribution{color.END}')
        for i in result:
            print(f"{i.uid: <{pad_1}}\t{i.licence_url: <{pad_2}}\t{i.attribution}")    

    return result

def fun_search_area(sesh, x, print_results=True):
    query = select(StandardGeographicClassification) \
        .where(StandardGeographicClassification.sgc_name.like("%%%s%%" % x.lower().strip())) \
        .order_by(StandardGeographicClassification.sgc_name)

    result = list(sesh.scalars(query))

    pad_1 = max([len(i.sgc_name) for i in result])
    pad_2 = max([len(i.sgc_uid) for i in result])
    pad_3 = max([len(i.dguid) for i in result])

    if print_results:
        print(f'{color.BOLD}{"Area": <{pad_1}}\t{"UID": >{pad_2}}\t{"DGUID": <{pad_3}}\t{"Area Type"}{color.END}')
        for i in result:
            print(f"{i.sgc_name: <{pad_1}}\t{i.sgc_uid: >{pad_2}}\t{i.dguid: <{pad_3}}\t{i.sgc_level.sgc_type_name_en}") 

    return result 