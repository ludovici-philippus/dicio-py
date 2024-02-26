import sys
import re
from unicodedata import normalize
from urllib.request import urlopen

BASE_URL = 'https://www.dicio.com.br/'
COLORS = {
    'RED': "\033[1;31m",
    'WHITE': "\033[1m",
    'YELLOW': "\033[1;33m",
    'BLUE': "\033[1;34m",
    'MAGENTA': "\033[1;35m",
    'END': "\033[m",
    'ITALIC': '\033[3m'
}

def colorize(text, color):
    return f"{COLORS[color.upper()]}{text}{COLORS['END']}"

def print_with_color(text: str, color: str):
    print(colorize(text, color))

def print_results() :
    print_with_color(f"Significado de {COLORS['BLUE']}{WORD.upper()}{COLORS['END']}", 'White')
    print(format_html(HTML_MEANING))

def get_content_of_tag(html, tag, close_tag):
    tag_index = html.find(tag)
    start_index = tag_index + len(tag)
    end_index = html[start_index:].find(close_tag) + start_index
    return html[start_index:end_index]

def format_html(html):
    etymologies = html.split('<span class="cl">')
    etymologies.pop(0)
    formatted_text = ""
    for etymology in etymologies:
        meanings = etymology.split('</span>')
        formatted_text += f"\n- {colorize(meanings[0], 'Magenta')}\n\n"
        meanings.pop(0)
        for meaning in meanings:
            meaning = meaning.strip()
            if(meaning.startswith('<span class="etim">')):
                formatted_meaning = meaning.replace('<span class="etim">', COLORS['WHITE'])
                formatted_meaning = formatted_meaning.replace('<i>', COLORS['ITALIC'])
                formatted_meaning = formatted_meaning.replace('</i>', COLORS['END'])
                formatted_meaning = formatted_meaning.replace('<br />', '')
                formatted_meaning = formatted_meaning.replace('<span>', '- ')
                formatted_text += f"{formatted_meaning}{COLORS['END']}"                    
            elif(meaning.startswith('<span><span class="tag">')):
                formatted_meaning = meaning.replace('<span class="tag">', COLORS['YELLOW'])
                formatted_meaning = formatted_meaning.replace('<span>', '- ')
                formatted_text += f" {formatted_meaning}{COLORS['END']}"
            else:
                formatted_meaning = meaning.replace('<span>', '- ')
                TAG_PATTERN = re.compile(r'<.*?>')
                formatted_meaning = TAG_PATTERN.sub('', formatted_meaning)
                formatted_text += f" {formatted_meaning}{COLORS['END']}\n"
    return formatted_text

if len(sys.argv) < 2:
    print_with_color("ERRO! Você precisa prover uma palavra", 'RED')
    print("Uso: python ./dicio-py.py [PALAVRA]")
    exit()
WORD = sys.argv[1].lower()
try:
    NORMALIZED_WORD = normalize('NFKD', WORD).encode('ASCII','ignore').decode('ASCII')
    PAGE_WORD = urlopen(f"{BASE_URL}{NORMALIZED_WORD}")
except:
    print_with_color("A palavra que você pesquisou não foi encontrada", 'Red')
    exit()

HTML = PAGE_WORD.read().decode('utf-8')
HTML_MEANING = get_content_of_tag(HTML, '<p class="significado textonovo">', '</p>')

print_results()