import os
import pdfplumber
from extract_data import extract_text_from_pdf, generate_csv_tables
from LLM_options import script_LLM_option_1, script_LLM_option_2, script_LLM_option_3
import glob
from analyse_csv import consolidate_financial_reports
from ratio import ratio_analysis

def option_1(pdf_file_path):
    text = extract_text_from_pdf(pdf_file_path)
    LLM_output = script_LLM_option_1(text)
    print(LLM_output)
    return

def option_2(pdf_file_path):
    text = extract_text_from_pdf(pdf_file_path, 20)
    LLM_output = script_LLM_option_2(text)
    print(LLM_output)
    return

def option_3(pdf_file_path):

    folder_name = pdf_file_path+"csv_folder"
    list_of_dict_tables_csv = generate_csv_tables(pdf_file_path,folder_name)

    ask_keywords_LLM = script_LLM_option_3(1)
    respond_user = input(ask_keywords_LLM)

    keywords = script_LLM_option_3(2,respond_user)
    keywords = keywords.split(":")[1]
    keywords = [word.strip() for word in keywords.split(",")]
    
    file_paths = glob.glob(folder_name+"/filtered_table*.csv")
    
    consolidate_financial_reports(file_paths, keywords,folder_name)
    ## TO DO : 
    
    csv_path = os.path.join(folder_name, f"consolidated_report.csv")
    LLM_output = script_LLM_option_3(3,csv_path)
    print(LLM_output)
    #CSV est le nom du fichier de consolidate_financial_reports (pd.read)


    return

def option_4(pdf_file_path):

    ################### RECUPERATION DU CSV ################################

    # Liste de mots-clés financiers pertinents pour filtrer les lignes
    keywords = ["bénéfices avant impots",
                "bénéfices",
                "bénéfice net", "net income",
                "bénéfice par action", "earnings per share",
                "flux de trésorerie", "cash flow",
                "dividendes par action", "dividends per share",
                "actif total", "total assets",
                "passif total", "total liabilities",
                "passif à long terme", "long-term liabilities",
                "actif à long terme", "long-term assets",
                "actif courant", "current assets",
                "passif courant", "current liabilities",
                "actif non courant", "non-current assets",
                "passif non courant", "non-current liabilities",
                "intérêt", "interest",
                "impôt", "tax",
                "actifs totaux", "total assets",
                "passifs totaux", "total liabilities",
                "bénéfices non répartis", "retained earnings",
                "RND", "Retained earnings",  
                "capitaux propres", "equity",
                "capital social", "share capital",
                "action ordinaire", "ordinary share",
                "actions privilégiées", "preferred shares",
                "dividendes", "dividends",
                "équivalents de trésorerie", "cash equivalents",
                "actif", "asset",
                "passif", "liability"
    ]

    folder_name = pdf_file_path+"csv_folder"
    file_paths = glob.glob(folder_name+"/filtered_table*.csv")
    list_of_dict_tables_csv = generate_csv_tables(pdf_file_path,folder_name)
    consolidate_financial_reports(file_paths, keywords,folder_name)

    ################### TASK CHOCE ################################
    dict_task = {1: "evolution_benefice_net", 
                 2: "evolution_div_action", 
                 3: "show_actifs_passifs_totaux",
                 4: "show_actifs_passifs_current",
                 5: "evolution_rnd",
                 6: "evolution_div_versé"}
    task = int(input(f"You are pleased to chose your task from the following list :\n{dict_task}.\n"))

    ################### DOMAIN CHOCE ################################
    dict_domain = {1 : "industriel", 2 : "telecoms", 3 : "services"}
    int_comparatif = int(input(f"Would you like a comparative analysis. If yes, please chose the domain from the following list :\n{dict_domain}.\nIf not, press 0"))
    domain = dict_domain.get(int_comparatif, None)

    ################### APPEL DE LA FONCTION ratio_analysis ################################
    csv_path = os.path.join(folder_name, f"consolidated_report.csv")
   
    try:
        ratio_analysis(csv_path, task, domain)
    except:
        print("an error ocurred")
        

    #CSV est le nom du fichier de consolidate_financial_reports (pd.read)


    return 


def test():
    pdf_file_path = r"C:\Users\cocor\Documents\CoursPolyMontreal\datathon_2024\ferroviaire\CN\2018-CN-Rapport-Annuel.pdf"
    task = 3

    if task == 1:
        option_1(pdf_file_path)
    if task == 2:
        option_2(pdf_file_path)
    if task == 3:
        option_3(pdf_file_path)
    if task == 4 :
        option_4(pdf_file_path)


def main(pdf_file_path):

    #Selection du input pdf file
    

    #Selection de l'action
    while True:
        task = input("What do you want to know about this file ? Please press the id of the task\n1 : Global summary of the file\n2 : Summary of the message from the direction, and fellings about it.\n3 : Report Analysis from keywords\n4: Global Report Analysis")
        if task.isdigit() :
            task = int(task)
            if 1 <= task <= 4 :
                print("Your task is in process,...")
                break
        else:
            print("ValueError : it must be an int between 1 and 4")


    
    if task == 1:
        option_1(pdf_file_path)
    if task == 2:
        option_2(pdf_file_path)
    if task == 3:
        option_3(pdf_file_path)
    if task == 4:
        option_4(pdf_file_path)
    return


if __name__=="__main__":
    # test()
    while True:
        pdf_file_path = input("Hello, please give us the path of the PDF file to analyze: ")

        # Vérifie si le fichier existe
        if os.path.isfile(pdf_file_path):
            try:
                # Essaye d'ouvrir et de lire le PDF
                with pdfplumber.open(pdf_file_path) as pdf:
                    print("File imported with success")
                    break 
            except Exception as e:
                print(f"Error while trying to open the file. Reason : {e}")
        else:
            print("The path file dose not exist. Please try again")
    user_stop = 0
    while (user_stop==0):
           
        main(pdf_file_path)
        user_stop = int(input("Do you wish to make another request ? Yes : press 0 ,No : press 1"))