from TransHelp import app

@app.template_filter('signed')
def signed(n:int) -> str:
    return '%+d' % n

@app.template_filter('rating_name')
def rating_name(rating:int) -> str:
    '''
    To convert a guide rating to a name of the rating enum.
    This can be usefull in the css classes.
    :param rating:
    :return:
    '''
    from models.guide import GuideRating
    return GuideRating(rating).name

@app.template_filter('lang_to_name')
def lang_to_name(language:str) -> str:
    from pycountry import languages
    return languages.get(alpha_3=language).name

@app.template_filter('country_to_flag')
def country_to_flag(country) -> str:
    if type(country) == str:
        return country.lower()

@app.template_filter('country_to_name')
def country_to_name(country) -> str:
    from pycountry import countries
    if type(country) == str:
        return countries.get(alpha_2=country).name