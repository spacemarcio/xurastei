from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

# SETUP WEB DRIVER
webdriver_path = 'chromedriver'

webdriver_options = Options()
webdriver_options.add_argument('--no-sandbox')
webdriver_options.add_argument('--headless')

web = webdriver.Chrome(
    executable_path= webdriver_path,
    options=webdriver_options
)

# CRAWLING DATA
url_root = 'https://pe.olx.com.br/grande-recife/recife'

# search properties by neighborhood
neighborhoods = [
    'aflitos','apipucos','barro','boa-viagem','boa-vista','campo-grande',
    'casa-amarela','casa-forte','caxanga','cidade-universitaria','cordeiro',
    'curado','derby','encruzilhada','espinheiro','estancia','gracas',
    'ilha-do-leite','ilha-do-retiro','imbiribeira','iputinga','jaqueira',
    'macaxeira','madalena','monteiro','paissandu','parnamirim','pina',
    'poco-da-panela','prado','santo-amaro','tamarineira','tejipio','torre',
    'torreao','zumbi'
]

links = [] 
for n in neighborhoods:
    stop = False
    page = 1
    
    while stop == False:

        print(f"""
        Scrapping ads from {n}
        Page {page} 
        """)
    
        url_query = f"{url_root}/{n}/imoveis/aluguel?o={page}"

        web.get(url_query)

        # checking if we passed the last page
        try:
            response = web.find_element_by_xpath("//*[contains(text(), 'Nenhum anúncio foi encontrado.')]").text
            
            if response:
                stop = True

            print(f"{len(links)} fetched")

            print('Going to the next neighborhood...')

        # if not passed, then get ads links
        except:
            properties_elements = web.find_elements_by_tag_name('a')
            properties_links = [e.get_attribute('href') for e in properties_elements]
            properties_links = [l for l in properties_links if l is not None]
            properties_links = [l for l in properties_links if l[-9:].isnumeric()] # an ad link finish with 9 digits code

            links += properties_links

            page += 1
    
    stop = False

web.close()

# WRIRTE LINKS
links_file = open("data/olx_imoveis_links.txt",mode="w",encoding="utf-8")
links_file.writelines([link + '\n' for link in links])
links_file.close()