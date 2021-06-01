import fitz
from itertools import groupby
from operator import itemgetter
import pprint
import string
import os
import pandas
import statistics


class Tree:
    def __init__(self, root):
        self.root = root

    def printContent(self):
        nodesToVisit = []
        nodesToVisit.append(self.root)
        while len(nodesToVisit) > 0:
            currentNode = nodesToVisit.pop()
            if currentNode.parent != None:
                print("tag : {0}\t\tparent : {1}\t\t{2}".format(
                    currentNode.tagType, currentNode.parent.tagType, currentNode.content))
            else:
                print("tag : " + currentNode.tagType)
            i = len(currentNode.children) - 1
            while i > -1:
                nodesToVisit.append(currentNode.children[i])
                i -= 1

    def harvest(self):
        # Method 1 : group the all headers with the first paragraph and other paragraph
        output = []
        visitedNodes = []  # to keep track of visited nodes
        nodesToVisit = []  # to store all nodes we will visit later if not visited yet
        nodesToVisit.append(self.root)
        while (len(nodesToVisit) > 0):
            currentNode = nodesToVisit.pop()  # take one node we should visit
            # if this node doesn't have paragraphs as children just add his children to the node to visit
            if len(currentNode.children) > 0 and not currentNode.children[0].isParagraph():
                # add each children in the nodes to visit
                i = len(currentNode.children) - 1
                while i > -1:
                    nodesToVisit.append(currentNode.children[i])
                    i -= 1
            # it is a node that contains paragraph so build the output
            elif len(currentNode.children) > 0 and currentNode.children[0].isParagraph():
                # take the first element and group it with their headers
                groupedHeaderAndParagraph = []
                cursor = currentNode.children[0]
                while(cursor.parent is not None):
                    groupedHeaderAndParagraph.append(cursor.content)
                    cursor = cursor.parent
                # reverse the groupedHeaderAndParagraph to put text in correct order
                # add group to output
                textGroup = ''
                counter = len(groupedHeaderAndParagraph) - 1
                while(counter >= 0):
                    textGroup += groupedHeaderAndParagraph[counter] + ' '
                    counter -= 1
                output.append(textGroup)
                # add other paragraphs to output
                i = 1  # start from the second paragraph
                while (len(currentNode.children) > 1 and i < len(currentNode.children)):
                    output.append(currentNode.children[i].content)
                    i += 1  # go to the next paragraph

        return output

    def harvest_v2(self):
        # Method 2 : group the all headers with paragraphs and each paragraph must contains 500 words minimum
        output = []
        visitedNodes = []  # to keep track of visited nodes
        nodesToVisit = []  # to store all nodes we will visit later if not visited yet
        nodesToVisit.append(self.root)
        while (len(nodesToVisit) > 0):
            currentNode = nodesToVisit.pop()  # take one node we should visit
            # if this node doesn't have paragraphs as children just add his children to the node to visit
            if len(currentNode.children) > 0 and not currentNode.children[0].isParagraph():
                # add each children in the nodes to visit
                i = len(currentNode.children) - 1
                while i > -1:
                    nodesToVisit.append(currentNode.children[i])
                    i -= 1
            # it is a node that contains paragraph so build the output
            elif len(currentNode.children) > 0 and currentNode.children[0].isParagraph():
                # take the first element and group it with their headers
                groupedHeaderAndParagraph = []
                cursor = currentNode.children[0]
                while(cursor.parent is not None):
                    groupedHeaderAndParagraph.append(cursor.content)
                    cursor = cursor.parent
                # reverse the groupedHeaderAndParagraph to put text in correct order
                # add group to output
                textGroup = ''
                counter = len(groupedHeaderAndParagraph) - 1
                while(counter >= 0):
                    textGroup += groupedHeaderAndParagraph[counter] + ' '
                    counter -= 1
                output.append(textGroup)
                # add other paragraphs to output
                i = 1  # start from the second paragraph
                while (len(currentNode.children) > 1 and i < len(currentNode.children)):
                    wordsCounter = len(currentNode.children[i].content.split())
                    lastParagraphIndex = len(output) - 1
                    lastParagraphWordsCount = len(
                        output[lastParagraphIndex].split())
#                     print("-------------------\n\n")
#                     print("This is to count words in a paragraph \n\n")
#                     print(wordsCounter)
#                     print("-------------------\n\n")
#                     print("output[lastParagraphIndex] \n\n")
#                     print(lastParagraphWordsCount)
#                     print("-------------------\n\n")
#                     print(" Before Added \n\n")
#                     print((output[lastParagraphIndex]))
#                     print("-------------------\n\n")
                    if wordsCounter < 100 and lastParagraphIndex >= 0 and lastParagraphWordsCount < 100 and len(output[lastParagraphIndex].split()) < 400:
                        output[lastParagraphIndex] += ' ' + \
                            currentNode.children[i].content
                        # Modification
#                         print("Length--\n\n")
#                         print(len(output[lastParagraphIndex].split()))
#                         print("Added \n\n")
#                         print((output[lastParagraphIndex]))
#                         print("-------------------\n\n")
#                         print("------i is--------")
#                         print(i)
#                         print("-------------------\n\n")
                        #i += 1
                        # continue

                    else:
                        # take the element and group it with their headers
                        groupedHeaderAndParagraph = []
                        cursor = currentNode.children[i]
                        while(cursor.parent is not None):
                            groupedHeaderAndParagraph.append(cursor.content)
                            cursor = cursor.parent
                        # reverse the groupedHeaderAndParagraph to put text in correct order
                        # add group to output
                        textGroup = ''
                        counter = len(groupedHeaderAndParagraph) - 1
                        while(counter >= 0):
                            textGroup += groupedHeaderAndParagraph[counter] + ' '
                            counter -= 1
                        output.append(textGroup)
                    i += 1  # go to the next paragraph

        return output


class Node:
    def __init__(self, parent, tagType, content):
        self.children = []
        self.parent = None
        self.tagType = tagType
        self.content = content
        if parent is not None:
            self.addParent(parent)

    def addChild(self, newChild):
        self.children.append(newChild)

    def addParent(self, parent):
        self.parent = parent
        parent.addChild(self)

    def getPage(self):
        cursor = self.parent
        # get the page where this element is attached to
        while cursor and cursor.tagType != '<page>':
            cursor = cursor.parent
        return cursor

    def isHeader(self):
        return self.tagType == '<h>'

    def isParagraph(self):
        return self.tagType == '<p>'


def fonts(doc):
    """Extracts fonts and their usage in PDF documents.
    :param doc: PDF document to iterate through
    :type doc: <class 'fitz.fitz.Document'>
    :rtype: [(font_size, count), (font_size, count}], dict
    :return: most used fonts sorted by count, font style information
    """
    styles = {}
    font_counts = {}

    for page in doc:
        blocks = page.getText("dict")["blocks"]
        for b in blocks:  # iterate through the text blocks
            if b['type'] == 0:  # block contains text
                for l in b["lines"]:  # iterate through the text lines
                    for s in l["spans"]:  # iterate through the text spans
                        identifier = "{0}".format(s['size'])
                        styles[identifier] = {'size': s['size']}
                        font_counts[identifier] = font_counts.get(
                            identifier, 0) + 1  # count the fonts usage

    font_counts = sorted(font_counts.items(), key=itemgetter(1), reverse=True)

    if len(font_counts) < 1:
        raise ValueError("Zero discriminating fonts found!")

    return font_counts, styles


def font_tags(font_counts, styles):
    """Returns dictionary with font sizes as keys and tags as value.
    :param font_counts: (font_size, count) for all fonts occuring in document
    :type font_counts: list
    :param styles: all styles found in the document
    :type styles: dict
    :rtype: dict
    :return: all element tags based on font-sizes
    """
    p_style = styles[font_counts[0][0]
                     ]  # get style for most used font by count (paragraph)
    p_size = p_style['size']  # get the paragraph's size

    # sorting the font sizes high to low, so that we can append the right integer to each tag
    font_sizes = []
    for (font_size, count) in font_counts:
        font_sizes.append(float(font_size))
    font_sizes.sort(reverse=True)

    # aggregating the tags for each font size
    idx = 0
    size_tag = {}
    for size in font_sizes:
        if size == p_size:
            idx = 0
            size_tag[size] = '<p>'
        if size > p_size:
            size_tag[size] = '<h>'
        elif size < p_size:
            size_tag[size] = '<s>'

    return size_tag


def my_paragraph_extractor(text):
    currentParagraph = 0
    lines = text.splitlines()
    paragraphs = []
    paragraphs.append('')
    current_paragraph = 0
    lastLine = ''
    for line in lines:
        if line.isspace() and len(lastLine) > 2 and not lastLine.isspace():
            current_paragraph += 1
        elif (not line.isspace()) and len(line) > 2:
            if len(paragraphs) - 1 < current_paragraph:
                paragraphs.append('')
            paragraphs[current_paragraph] += line + ' '
        lastLine = line
        #print("--- LINE ----")
        # print(len(line))
        # print(line)
        # print("--------------\n\n")

    return paragraphs


def isNextLineWhitespace(currentIndex, lines):
    totalLine = len(lines)
    if (currentIndex == totalLine - 1 or currentIndex < 0 or currentIndex >= totalLine):
        return False
    else:
        return lines[currentIndex + 1]['text'].isspace()


def isPreviousLineWhitespace(currentIndex, lines):
    totalLine = len(lines)
    if (currentIndex == 0 or currentIndex < 0 or currentIndex >= totalLine):
        return False
    else:
        return lines[currentIndex - 1]['text'].isspace()


def isStartingWithCapital(text):
    i = 0
    while (i < len(text) and text[i].isspace()):
        i += 1
    return text[i].isupper()


def isLastCharFullStop(text):
    i = len(text) - 1
    while(i > 0 and text[i].isspace()):
        i -= 1

    return text[i] == '.'


def isPreviousLineEndWithFullStop(currentIndex, lines):
    totalLine = len(lines)
    if (currentIndex == 0 or currentIndex < 0 or currentIndex >= totalLine):
        return False
    else:
        return isLastCharFullStop(lines[currentIndex - 1]['text'])


def isInside(text, paragraph_model, iterator):
    return text in paragraph_model[iterator]


def isNextSpan(currentIndex, lines):
    totalLine = len(lines)
    if (currentIndex == totalLine - 1 or currentIndex < 0 or currentIndex >= totalLine):
        return False
    else:
        return lines[currentIndex + 1]['text'].isspace()


def pdfParagraphExtractor(pdf):
    #pdf = ('DISABILITY-RIGHTS-PROMOTION-INTERNATIONAL-Monitoring-The-Human-Rights-of-Persons-with-Disabilities-Country-Report-Cameroon.pdf')
    #pdf = ('pdf_files/A Guide to Economic, Social, and Cultural Rights in I.C.E.S.C.R. related to disability FACILITATOR VERSION.pdf')
    #file.name = ('Are We Moving Forward_ Regional Study on the Rights of Women with Disabilities in the Middle East.pdf')
    #file = ('pdf_files/A Guide to Economic, Social, and Cultural Rights in I.C.E.S.C.R. related to disability FACILITATOR VERSION.pdf')
    doc = fitz.open(pdf)
    #doc = fitz.open('pdf_files/A Guide to Economic, Social, and Cultural Rights in I.C.E.S.C.R. related to disability FACILITATOR VERSION.pdf')
    #doc = fitz.open(file.name)
    font_counts, styles = fonts(doc)
    size_tag = font_tags(font_counts, styles)
    root = Node(None, '<root>', '')
    redietsTree = Tree(root)
    currentPage = None
    currentNode = None
    lastNode = None
    sizeOfEachPara = []
    for page in doc:
        # pprint.pprint(my_paragraph_extractor(page))
        paragraph_model = []
        blocks = page.get_text('blocks')
        for block in blocks:
            if block[6] == 0:  # if block is text
                text = block[4]
                extractedParagraphs = my_paragraph_extractor(text)
                for paragraph in extractedParagraphs:
                    if (len(paragraph) > 0):
                        paragraph_model.append(paragraph)

    #             for paragraph in paragraph_model :
    #                 print("---- MODEL ----")
    #                 print(paragraph)
    #                 print("\n\n")
        for paragraph in paragraph_model:
            if (len(paragraph.split()) > 1):
                sizeOfEachPara.append(len(paragraph.split()))

    #             for size in sizeOfEachPara :
    #                 print("---- SIZES ----")
    #                 print(size)
    #                 print("\n\n")

        paragraph_model_iterator = 0
        span_iterator = 0
        currentPage = Node(redietsTree.root, '<page>', '')
        blocks = page.get_text('dict', flags=fitz.TEXT_PRESERVE_WHITESPACE)
        # gather every span in an array
        spans = []
        for block in blocks['blocks']:
            if block['type'] == 0:
                for line in block['lines']:
                    #                 print(line)
                    #                 print("\n\n")
                    currentIndex = 0
                    for span in line['spans']:
                        # handle space inside paragraph detected as line jump
                        if len(line['spans']) > 1 and span['text'].isspace() and currentIndex != 0 and currentIndex != len(line['spans']) - 1:
                            pass
                        else:
                            spans.append(span)
                        currentIndex += 1
        foundInLast = False
        while span_iterator < len(spans) and paragraph_model_iterator < len(paragraph_model):
            isHeader = size_tag[spans[span_iterator]['size']] == '<h>'
            isParagraph = size_tag[spans[span_iterator]['size']] == '<p>'
            isSubscript = size_tag[spans[span_iterator]['size']] == '<s>'
            isAfterLineJump = isPreviousLineWhitespace(span_iterator, spans)
            isBeforeLineJump = isNextLineWhitespace(span_iterator, spans)
            isAfterFullStop = isPreviousLineEndWithFullStop(
                span_iterator, spans)
            isBold = spans[span_iterator]['flags'] == 16
            text = spans[span_iterator]['text']

            isLengthofWordEnough = len(text) > 1

            if span_iterator + 1 < len(spans):
                nexttext = spans[span_iterator + 1]['text']
            else:
                nexttext = spans[span_iterator]['text']
            # using sum() + strip() + split() to count words in string
            # https://www.geeksforgeeks.org/python-program-to-count-words-in-a-sentence/
            countWord = sum([i.strip(string.punctuation).isalpha()
                            for i in text.split()])
            containText = not text.isspace()
    #         print("\n\n ---- MODEL -----")
    #         print(paragraph_model[paragraph_model_iterator])
    #         print("\n\n ---- // -----")

#             print("\n\n ---- BLOCK -----")
#             print("isHeader = {}".format(isHeader))
#             print("isParagraph = {}".format(isParagraph))
#             print("isSubscript = {}".format(isSubscript))
#             print("isAfterLineJump = {}".format(isAfterLineJump))
#             print("isBeforeLineJump = {}".format(isBeforeLineJump))
#             print("isBold = {}".format(isBold))
#             print(text)
#             print("---- BLOCK -----\n")
            if containText and not isSubscript and isLengthofWordEnough:
                if text.isnumeric() and text not in paragraph_model[paragraph_model_iterator]:
                    span_iterator += 1
                    foundInLast = False
                elif text not in paragraph_model[paragraph_model_iterator] and nexttext not in paragraph_model[paragraph_model_iterator]:
                    paragraph_model_iterator += 1
                    foundInLast = False
                else:
                    if not foundInLast:
                        if isHeader:
                            # previous node is header
                            if lastNode is not None and lastNode.isHeader():
                                currentNode = Node(lastNode, '<h>', text)
                            else:  # previous node is paragraph
                                currentNode = Node(currentPage, '<h>', text)
                        elif isParagraph and isBold and (isAfterLineJump or isBeforeLineJump):
                            # previous node is header
                            if lastNode is not None and lastNode.isHeader():
                                currentNode = Node(lastNode, '<h>', text)
                            else:  # previous node is paragraph
                                currentNode = Node(currentPage, '<h>', text)
                        elif isParagraph and isBold and len(text) + 1 == len(paragraph_model[paragraph_model_iterator]):
                            # previous node is header
                            if lastNode is not None and lastNode.isHeader():
                                currentNode = Node(lastNode, '<h>', text)
                            else:  # previous node is paragraph
                                currentNode = Node(currentPage, '<h>', text)
                        else:
                            if lastNode is not None and lastNode.isHeader():
                                currentNode = Node(lastNode, '<p>', text)
                            elif lastNode is not None and lastNode.isParagraph() and (not isLastCharFullStop(lastNode.content) or not isStartingWithCapital(text)):
                                lastNode.content += ' ' + text
                            elif lastNode is not None and lastNode.isParagraph():
                                currentNode = Node(
                                    lastNode.parent, '<p>', text)
                    else:
                        if lastNode is not None and lastNode.isHeader():
                            currentNode = Node(lastNode, '<p>', text)
                        elif lastNode is not None and lastNode.isParagraph() and isAfterLineJump and isLastCharFullStop(lastNode.content) and isStartingWithCapital(text):
                            currentNode = Node(lastNode.parent, '<p>', text)
                        elif lastNode is not None and lastNode.isParagraph():
                            lastNode.content += ' ' + text
                    lastNode = currentNode
                    span_iterator += 1
                    foundInLast = True
            else:
                span_iterator += 1
                foundInLast = False
    #         mean = int(statistics.mean(sizeOfEachPara))
    #         print("---- Mean ----")
    #         print(mean)

#     redietsTree.printContent()
    listExtractedParagraph = redietsTree.harvest_v2()
    return listExtractedParagraph
    #         df = pandas.DataFrame(data=listExtractedParagraph)
    #         df = df.iloc[1: , :]
    #         df.to_excel(file.name + ".xlsx",index=False, encoding="utf-16")
    #         csvFileIterator += 1
#     file = 'new file'
#     print("\n\n\n NEW PDF : " + file)
#     for p in listExtractedParagraph :
#         print("------ PARAGRAPH -----")
#         print(p)
#         print(len(p.split()))
#         print("-------END-----\n\n")
