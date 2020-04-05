import xlrd

def word_convert(iw, hg):
    book_obje = xlrd.open_workbook("/home/conansjh20/lyric/words-book2.xlsx")
    book_sheet = book_obje.sheet_by_name("1")

    list_korea1 = []
    list_korea2 = []
    list_korea = []
    list_japan = []

    for total_nums in range(0,book_sheet.nrows):
        for col_nums in range(0,4):
            list_korea1.append(book_sheet.cell_value(total_nums,col_nums))
        for l in list_korea1:
            if l != "":
                list_korea2.append(l)
        list_korea.append(list_korea2)
        list_korea1 = []
        list_korea2 = []
        list_japan.append(book_sheet.cell_value(total_nums,hg))

    input_word = iw
    list_input_word = []
    for i in input_word:
        list_input_word.append(i)

    converted_word = []

    for syl in list_input_word:
        for order_num in range(0,len(list_korea)):
            if syl in list_korea[order_num]:
                converted_word.append(list_japan[order_num])

    final_converted_word = "".join(converted_word)

    return final_converted_word
