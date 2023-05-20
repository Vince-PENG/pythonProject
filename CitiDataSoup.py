import requests
import os
from bs4 import BeautifulSoup

def get_province_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    provinces = soup.select('tr.provincetr td a')

    province_data = []
    for province in provinces:
        province_name = province.text
        if province_name != '湖南省':
            continue
        province_code = province['href'].split('.')[0]
        province_url = url[:url.rfind('/') + 1] + province_code + '.html'
        city_data = get_city_data(province_url)

        province_info = {
            'name': province_name,
            'code': province_code,
            'cities': city_data
        }
        province_data.append(province_info)

    return province_data

def get_city_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    cities = soup.select('tr.citytr')

    city_data = []
    for city in cities:

        city_info = city.select('td')
        city_code = city_info[0].text
        city_name = city_info[1].text
        if city_name != '长沙市':
            continue

        city_url = url[:url.rfind('/') + 1] + city_code[:2] + '/' + city_code[:4] + '.html'
        county_data = get_county_data(city_url)

        city_info = {
            'name': city_name,
            'code': city_code,
            'counties': county_data
        }
        city_data.append(city_info)

    return city_data

def get_county_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    counties = soup.select('tr.countytr')

    county_data = []
    for county in counties:
        county_info = county.select('td')
        county_code = county_info[0].text
        county_name = county_info[1].text

        if county_name != '长沙县':
            continue

        county_url = url[:url.rfind('/') + 1] + county_code[:4][-2:] + '/' + county_code[:6] + '.html'
        town_data = get_town_data(county_url)
        county_data.append({
            'name': county_name,
            'code': county_code,
            'towns':town_data
        })

    return county_data

def get_town_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    counties = soup.select('tr.towntr')

    county_data = []
    for county in counties:
        county_info = county.select('td')
        county_code = county_info[0].text
        county_name = county_info[1].text

        county_url = url[:url.rfind('/') + 1] + county_code[:6][-2:] + '/' + county_code[:9] + '.html'
        village_data = get_village_data(county_url)
        county_data.append({
            'name': county_name,
            'code': county_code,
            'villages': village_data
        })

    return county_data

#villagetr
def get_village_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    counties = soup.select('tr.villagetr')

    county_data = []
    for county in counties:
        county_info = county.select('td')
        county_code = county_info[0].text
        county_name = county_info[2].text
        county_data.append({
            'name': county_name,
            'code': county_code
        })

    return county_data


# 指定目标网页的URL
url = 'http://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2021/index.html'


if __name__ == '__main__':
    # 爬取数据
    province_data = get_province_data(url)
    # 打印结果
    csv_data = []
    for province in province_data:
        print('省:', province['name'], ', Code:', province['code'])
        csv_data.append('省:' + province['name'] + ', Code:' + province['code'] + "\n")
        for city in province['cities']:
            print('市:', city['name'], ', Code:', city['code'])
            csv_data.append('   市:' + city['name']+ ', Code:'+ city['code'] + "\n")
            for county in city['counties']:
                print('区:', county['name'], ', Code:', county['code'])
                csv_data.append('       区:'+ county['name']+ ', Code:'+ county['code']+ "\n")
                for town in county['towns']:
                    print('镇:', town['name'], ', Code:', town['code'])
                    csv_data.append('           镇:'+ town['name']+ ', Code:'+ town['code']+ "\n")
                    for village in town['villages']:
                        print('村:', village['name'], ', Code:', village['code'])
                        csv_data.append('               村:'+ village['name']+ ', Code:'+ village['code']+ "\n")
    #写入文件中
    with open(os.path.join("D:/", "长沙县-allCityData.txt"), "w", encoding="UTF-8") as f:
        f.writelines(["{}".format(sql) for sql in csv_data])