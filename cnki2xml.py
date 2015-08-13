#coding:utf-8
import sys
import re
import xml.dom.minidom

txtFileName = sys.argv[1]

txtFile = open(txtFileName, "r")
tagFieldList = txtFile.readlines()

def getFileName(fullFileName):
    for i in range(len(fullFileName)):
        if(fullFileName[i] == '.'):
            return fullFileName[0:i]
    return fullFileName

def getTagField(tag_field):
    tag = tag_field[0:2]
    field = tag_field[3:]
    return [tag, field]

def getFieldByTag(list, index, tag):
    while(index >= 0):
        [tag_in, field] = getTagField(list, index)
        if(tag_in == tag):
            return field
        index -= 1
def getKeywordsList(keywords):
    keywordsList = []
    lastSemPos = -1
    for i in range(len(keywords)):
        if(keywords[i:i+1] == ';'):
            keywordsList.append(keywords[lastSemPos+1:i])
            lastSemPos = i
    keywordsList.append(keywords[lastSemPos+1:])
    return keywordsList

def isFirstAuthor(list, index):
    FA_List = []
    for i in range(len(list)):
        if(list[i][0:2] == "%A" and list[i-1][0:2] != "%A"):
            FA_List.append(i)

    if index in FA_List:
        return True
    else:
        return False

def isPeriodical(list, index):
    while(index >= 0):
        [tag, field] = (list[index])
        if(tag == "%0" and field == "Journal Article"):
            return True
        index -= 1
    return False

index = 0
while index < len(tagFieldList):
    if(tagFieldList[index][0] != "%"):
        tagFieldList[index-1] = tagFieldList[index-1] + tagFieldList[index]
        del tagFieldList[index]
        index -= 1
    index += 1

end_rtrn_re = re.compile('(\r\n)+')
end_blnk_re = re.compile('\s+$')
for index in range(len(tagFieldList)):
    tagFieldList[index] = end_rtrn_re.sub(' ', tagFieldList[index])
    tagFieldList[index] = end_blnk_re.sub('', tagFieldList[index])

root = xml.dom.minidom.Document()
xml = root.createElement("xml")
root.appendChild(xml)
records = root.createElement("records")
xml.appendChild(records)

index = 0
while index < len(tagFieldList):
    [tag, field] = getTagField(tagFieldList[index])
    if(tag == "%0"):
        record = root.createElement("record")
        records.appendChild(record)
        refType = root.createElement("ref-type")
        record.appendChild(refType)
        if(field == "Journal Article"):
            refType.setAttribute("name", "Journal Article")
            refValue = root.createTextNode("17")
        elif(field == "Thesis"):
            refType.setAttribute("name", "Thesis")
            refValue = root.createTextNode("32")
        elif(field == "Conference Proceedings"):
            refType.setAttribute("name", "Conference Proceedings")
            refValue = root.createTextNode("10")
        refType.appendChild(refValue)
        index += 1
        continue


    elif(tag == "%A"):
        if(isFirstAuthor(tagFieldList, index)):
            contributors = root.createElement("contributors")
            record.appendChild(contributors)
            authors = root.createElement("authors")
            contributors.appendChild(authors)
        author = root.createElement("author")
        authors.appendChild(author)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        author.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%Y"):
        tertiary_author = root.createElement("tertiary-authors")
        contributors.appendChild(tertiary_author)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        tertiary_author.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)


    elif(tag == "%+"):
        auth_address = root.createElement("auth-address")
        record.appendChild(auth_address)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        auth_address.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%T"):
        titles = root.createElement("titles")
        record.appendChild(titles)
        title = root.createElement("title")
        titles.appendChild(title)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        title.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%J"):
        secondary_title = root.createElement("secondary-title")
        titles.appendChild(secondary_title)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        secondary_title.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

        periodical = root.createElement("periodical")
        record.appendChild(periodical)
        full_title = root.createElement("full-title")
        periodical.appendChild(full_title)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        full_title.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%P"):
        pages = root.createElement("pages")
        record.appendChild(pages)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        pages.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%N"):
        number = root.createElement("number")
        record.appendChild(number)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        number.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%D"):
        dates = root.createElement("dates")
        record.appendChild(dates)
        year = root.createElement("year")
        dates.appendChild(year)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        year.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%@"):
        isbn = root.createElement("isbn")
        record.appendChild(isbn)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        isbn.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%L"):
        call_num = root.createElement("call-num")
        record.appendChild(call_num)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        call_num.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%W"):
        remote_database_provider = root.createElement("remote-database-provider")
        record.appendChild(remote_database_provider)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        remote_database_provider.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%I"):
        publisher = root.createElement("publisher")
        record.appendChild(publisher)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        publisher.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%9"):
        work_type = root.createElement("work-type")
        record.appendChild(work_type)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        work_type.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%X"):
        abstract = root.createElement("abstract")
        record.appendChild(abstract)
        style = root.createElement("style")
        style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
        abstract.appendChild(style)
        field_node = root.createTextNode(field)
        style.appendChild(field_node)

    elif(tag == "%K"):
        keywords = root.createElement("keywords")
        record.appendChild(keywords)
        keywordsList = getKeywordsList(field)
        for i in range(len(keywordsList)):
            keyword = root.createElement("keyword")
            keywords.appendChild(keyword)
            style = root.createElement("style")
            style.setAttribute("face", "normal");style.setAttribute("font", "default");style.setAttribute("size", "100%")
            keyword.appendChild(style)
            field_node = root.createTextNode(keywordsList[i])
            style.appendChild(field_node)

    index += 1

xmlFileName = getFileName(sys.argv[1]) + ".xml"
xmlFile = open(xmlFileName, "w")
root.writexml(xmlFile, "  ", "  ", "\n", "utf-8")
xmlFile.close()