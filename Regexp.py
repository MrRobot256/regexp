import csv
import re


with open('phonebook_raw.csv', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)
    print(contacts_list)


def normalize_names(data):
    new_data = []
    pattern = re.compile(r'^([а-яА-Я]+)[\s|,]([а-яА-Я]+)[\s|,]([а-яА-Я]+|)')
    for contact in data:
        str_contact = ','.join(contact)
        normalized_contact = pattern.sub(r'\1, \2, \3', str_contact).split(',')
        if not normalized_contact[4]:
            normalized_contact.pop(4)
        if not normalized_contact[3]:
            normalized_contact.pop(3)
        new_data.append(normalized_contact)
    return new_data


def normalize_phones(data):
    new_data = []
    pattern = re.compile(
        r'(\+7|8)\s?\(?(\d{3})\)?[\s|-]?(\d{3})[\s|-]?(\d{2})[\s|-]?(\d{2})(\s)?\(?([а-я.]+)?\s?(\d{4})?')
    for contact in data:
        str_contact = ','.join(contact)
        normalized_phones = pattern.sub(r'+7(\2)\3-\4-\5\6\7\8', str_contact).split(',')
        new_data.append(normalized_phones)
    return new_data


def remove_dupes(data):
    name_dict = {}
    for contact in data:
        if contact[0] in name_dict:
            for item in range(len(contact)):
                if contact[item] and not data[name_dict[contact[0]]][item]:
                    data[name_dict[contact[0]]][item] = contact[item]
                elif contact[item] and data[name_dict[contact[0]]][item] != contact[item]:
                    data[name_dict[contact[0]]][item + 1] = contact[item]
            data.remove(contact)
        else:
            name_dict[contact[0]] = data.index(contact)
    return data


new_contacts_list = remove_dupes(normalize_phones(normalize_names(contacts_list)))

with open("phonebook.csv", "w", encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(new_contacts_list)