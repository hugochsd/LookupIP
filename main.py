# Written by : Hugo Chauschard
# 8/4/2022
import requests
import time
import pandas as pd
from openpyxl import writer

def main():

    #key to make API calls
    apivoid_key = '902345018587a33f9c99134d8011a6739a1a7873'

    print(" ----------------------------------------------------- ")
    print("|                   IPv4 | URL                        |")
    print(" ----------------------------------------------------- ")
    print("IPv4 check - Enter:1")
    print("URL check  - Enter:2")

    choice = input("Enter:")
    if choice == '1':
        # read Excel file
        #IPdf = pd.read_excel("input.xlsx", "infected_ips")
        #IP_list = IPdf['SenderIPv4'].values.tolist()
        IP_list = ['122.226.181.165']
        print("#######################################################")
        print("#        USING APIVoid for IPV4                       #")
        print("#        ENGINES USED : 80+                           #")
        print("#        https://docs.apivoid.com/                    #")
        print("#          Requirements:                              #")
        print("#         - Column must be labeled 'SenderIPv4'       #")
        print("#         - Sheetname must be labeled 'infected_ips'  #")
        print("#######################################################")

        goodIPs = []
        badIPs = []
        # open .txt to write report
        outfile = open('report.txt', 'w')
        for ip in IP_list:
            time.sleep(0.5)
            url = f'https://endpoint.apivoid.com/iprep/v1/pay-as-you-go/?key={apivoid_key}&ip={ip}'
            r = requests.get(url)
            outfile.write('\n#####################################################################\n')
            outfile.write(f'IP : {r.json()["data"]["report"]["ip"]}\n')
            outfile.write(f'DETECTIONS : {r.json()["data"]["report"]["blacklists"]["detections"]}\n')
            outfile.write(f'COUNTRY : {r.json()["data"]["report"]["information"]["country_name"]}\n')
            outfile.write(f'CITY : {r.json()["data"]["report"]["information"]["city_name"]}\n')
            outfile.write(f'ISP : {r.json()["data"]["report"]["information"]["isp"]}\n')
            outfile.write(f'REVERSE DNS : {r.json()["data"]["report"]["information"]["reverse_dns"]}\n')
            outfile.write(f'ANONIMITY : {r.json()["data"]["report"]["anonymity"]}\n')


            if r.json()['data']['report']['blacklists']['detections'] == 0:
                print("----------------------------")
                print(f'IP : {r.json()["data"]["report"]["ip"]}')
                print(f'DETECTIONS : {r.json()["data"]["report"]["blacklists"]["detections"]}')
                print('STATE : CLEARED')
                print(f'ISP : {r.json()["data"]["report"]["information"]["isp"]}')
                print(f'COUNTRY : {r.json()["data"]["report"]["information"]["country_name"]}')
                print(f'CITY : {r.json()["data"]["report"]["information"]["city_name"]}')
                print(f'REVERSE DNS : {r.json()["data"]["report"]["information"]["reverse_dns"]}')
                goodIPs.append(ip)
            else:
                print("----------------------------")
                print(f'IP : {r.json()["data"]["report"]["ip"]}')
                print(f'DETECTIONS : {r.json()["data"]["report"]["blacklists"]["detections"]}')
                print('STATE : RISK')
                if r.json()["data"]["report"]["anonymity"]["is_hosting"] == True:
                    print("ANONYMITY TYPE: HOSTING")
                elif r.json()["data"]["report"]["anonymity"]["is_proxy"] == True:
                    print("ANONYMITY TYPE: PROXY")
                elif r.json()["data"]["report"]["anonymity"]["is_tor"] == True:
                    print("ANONYMITY TYPE: TOR")
                elif r.json()["data"]["report"]["anonymity"]["is_vpn"] == True:
                    print("ANONYMITY TYPE: VPN")
                elif r.json()["data"]["report"]["anonymity"]["is_webproxy"] == True:
                    print("ANONYMITY TYPE: WEB PROXY")
                print(f'ISP : {r.json()["data"]["report"]["information"]["isp"]}')
                print(f'COUNTRY : {r.json()["data"]["report"]["information"]["country_name"]}')
                print(f'CITY : {r.json()["data"]["report"]["information"]["city_name"]}')
                print(f'REVERSE DNS : {r.json()["data"]["report"]["information"]["reverse_dns"]}')
                badIPs.append(ip)

        outfile.close()

        print(f'CREDITS REMAINING : {r.json()["credits_remained"]}')


        goodIPdata = pd.DataFrame({'Cleared IPs':goodIPs})
        badIPdata = pd.DataFrame({'RISK IPs':badIPs})

        writer = pd.ExcelWriter('goodIP_Results.xlsx')
        writer2 = pd.ExcelWriter('badIP_Results.xlsx')
        goodIPdata.to_excel(writer, sheet_name='clearedIPsheet')
        badIPdata.to_excel(writer2, sheet_name='riskyIPsheet')
        workbook = writer.book
        workbook2 = writer2.book
        worksheet = writer.sheets['clearedIPsheet']
        worksheet2 = writer2.sheets['riskyIPsheet']
        worksheet.set_column(1,1,50)
        worksheet2.set_column(1,1,50)
        writer.save()
        writer2.save()

    elif choice == '2':
        time.sleep(0.5)
        #URLdf = pd.read_excel('input.xlsx', "URL")
        #URL_list = URLdf['URL'].values.tolist()
        URL_list = ['https://www.google.com/']
        print("#######################################################")
        print("#            USING APIVoid for URL                    #")
        print("#            ENGINES USED : 50+                       #")
        print("#            https://docs.apivoid.com/                #")
        print("#         - Column must be labeled 'URL'              #")
        print("#         - Sheetname must be labeled 'URL'           #")
        print("#######################################################")

        goodURLs = []
        badURLs = []

        for URL in URL_list:
            time.sleep(0.5)
            url = f'https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/?key={apivoid_key}&url={URL}'
            r = requests.get(url)
            outfile = open('report.txt', 'w')
            outfile.write('\n#####################################################################\n')
            outfile.write(f'COUNTRY CODE : {r.json()["data"]["report"]["server_details"]["country_code"]}\n')
            outfile.write(f'ISP : {r.json()["data"]["report"]["server_details"]["isp"]}\n')
            outfile.write(f'IP: {r.json()["data"]["report"]["server_details"]["ip"]}\n')
            outfile.write(f'DETECTIONS: {r.json()["data"]["report"]["domain_blacklist"]["detections"]}\n')
            outfile.write(f'FILE TYPE: {r.json()["data"]["report"]["file_type"]}\n')
            outfile.close()

            if r.json()["data"]["report"]["domain_blacklist"]["detections"] == 0:
                print("----------------------------")
                print(f'COUNTRY CODE : {r.json()["data"]["report"]["server_details"]["country_code"]}')
                print(f'IP: {r.json()["data"]["report"]["server_details"]["ip"]}')
                print(f'DETECTIONS: {r.json()["data"]["report"]["domain_blacklist"]["detections"]}')
                print('STATE : CLEARED')
                goodURLs.append(URL)
            else:
                print("----------------------------")
                print(f'IP: {r.json()["data"]["report"]["server_details"]["ip"]}')
                print(f'DETECTION RATE : {r.json()["data"]["report"]["blacklists"]["detection_rate"]}')
                print('STATE : RISK')
                print(f'ISP : {r.json()["data"]["report"]["server_details"]["isp"]}')
                print(f'FILE TYPE: {r.json()["data"]["report"]["file_type"]}')
                badURLs.append(URL)

        print(f'CREDITS REMAINING : {r.json()["credits_remained"]}')

        goodURLdata = pd.DataFrame({'Cleared IPs': goodURLs})
        badURLdata = pd.DataFrame({'RISK IPs': badURLs})

        writer = pd.ExcelWriter('goodURL_Results.xlsx')
        writer2 = pd.ExcelWriter('badURL_Results.xlsx')
        goodURLdata.to_excel(writer, sheet_name='cleared URL sheet')
        badURLdata.to_excel(writer2, sheet_name='risky URL sheet')
        workbook = writer.book
        workbook2 = writer2.book
        worksheet = writer.sheets['cleared URL sheet']
        worksheet2 = writer2.sheets['risky URL sheet']
        worksheet.set_column(1, 1, 80)
        worksheet2.set_column(1, 1, 80)
        writer.save()
        writer2.save()
    else:
        print("Wrong entry, program will close soon please try again..")
        time.sleep(4)
        exit()


if __name__ == "__main__" :
    main()
