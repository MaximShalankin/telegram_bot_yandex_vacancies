def read_logs(path, filename='logs.txt'):
    
    import os
    import json
   
    complete_path = os.path.join(path, filename)
    if not os.path.exists(complete_path):
        raise IOError('logs file does not exist')
        
    with open(complete_path, 'r', encoding='utf8') as file:
        logs = json.load(file)
        
    return logs


def write_logs(logs, path, filename='logs.txt'):
    
    import os
    import json
    from datetime import datetime
    
    complete_path = os.path.join(path, filename)
    
    if not logs: # the first empty initialization
        logs = {}
        logs['actual_date'] = datetime.now().date().strftime("%Y-%m-%d")
        logs['vacancy_tag'] = {}

    with open(complete_path, 'w', encoding='utf8') as file:
        json.dump(logs, file)

        
def get_new_vacancies(tag='machinelearning'):
    
    """returns list of new vacancies which are up to date"""
    
    
    from bs4 import BeautifulSoup
    import requests
    import re
    
    def extract_text(obj):
        """Extraxt text from html code"""
        ans = []
        for i in obj:
            for ii in i:
                try:
                    ans.append(ii.get_text())
                except AttributeError:
                    ans.append(ii)
                    pass
        return ' '.join(str(i) for i in ans)
    
    url_ds = 'https://yandex.ru/jobs/vacancies/dev/?cities=213&tags=' + tag
    try:
        page = requests.get(url_ds, timeout=30.0) # URL HERE ###
    
    except: # There may be unknown error via server block
        return ['While server parsing error occured. There are no respond from server.']
        
    
    data = page.text
    structured_links = BeautifulSoup(data, 'lxml')
    try:
        vacancies = structured_links.find_all(class_='serp__item')
    except: # Error cause extraction failed
        return ['Extraction from server Error']
    
    list_of_matched_vacancies = [vacancy for vacancy 
                             in vacancies if re.findall(tag, vacancy.get('data-bem'))]
    
    matched_vacancies = [extract_text(vacancy) for vacancy in list_of_matched_vacancies]
    
    return matched_vacancies


def check_log_changes(path_to_logs, log_filename='logs.txt'):
    
    from datetime import datetime
    import os
    
    today_date = datetime.now().date()
    logs_file = read_logs(path_to_logs, log_filename)
    log_date = datetime.strptime(logs_file['date'], "%Y-%m-%d").date()
    
    if today_date > log_date:
        # Need to update information and rewrite logs
        
        #TODO: update vacancies becouse of new date
        old_vacancies = logs_file['tags']['machinelearning']['current']
        
        today_vacancies = get_new_vacancies() # Use this function for updating information about new vacancies

        removed_vacancies = list(set(old_vacancies) - set(today_vacancies))
        new_vacancies = list(set(today_vacancies) - set(old_vacancies))
        
        logs_file['date'] = today_date.strftime("%Y-%m-%d")
        logs_file['tags']['machinelearning']['current'] = today_vacancies
        logs_file['tags']['machinelearning']['removed'] = removed_vacancies
        logs_file['tags']['machinelearning']['new'] = new_vacancies
        
        write_logs(logs_file, path_to_logs, log_filename) # Write new logs to load them again 
        
        return today_date.strftime("%Y-%m-%d"), today_vacancies, removed_vacancies, new_vacancies
    else:
        # Information is up to date, just return it
        pass



def result_explanation(path_to_logfile, tag):
    """"
    -------
    Return:
        date, vacancies, vacancies_new, vacancies_deleted
    """
    
    logs = read_logs(path_to_logfile)
    date = logs['date']
    vacancies = logs['tags'][tag]['current']
    vacancies_new = logs['tags'][tag]['new']
    vacancies_deleted = logs['tags'][tag]['removed']

    return date, vacancies, vacancies_new, vacancies_deleted