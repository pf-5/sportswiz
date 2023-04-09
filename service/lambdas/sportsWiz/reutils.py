import re

# removes all \n\t\r, multi spaces, and strips
def clean_spacing(text):
    text = text.strip()
    text = re.sub(r'[\r|\n|\t]', ' ', text)
    text = re.sub(r'[ ]+', ' ', text)
    return text

# keep only alphanumeric
def alphanumeric(text):
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)

# keeps alphanumeric and certain special characters
def standard_characters(text, allowed='\s!@#$&()\\-`.+,/\"'):
    rgx = '[^a-zA-Z0-9%s]' % allowed
    return re.sub(rgx, '', text)

# return first word
def get_first_word(text):
    result = re.findall('[a-zA-Z]+', text)
    return result[0] if result else ''

# return first (decimal) number
def get_first_number(text):
    result = re.findall('[0-9.]+', text)
    return result[0] if result else ''
