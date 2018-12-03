"""currency.py: This module provides several string parsing functions to implement a
simple currency exchange routine using an online currency service.
The primary function in this module is exchange.

__author__ = "Xiang Liyuan"
__pkuid__  = "1800011800"
__email__  = "xiangliyuan@pku.edu.cn"
"""
from urllib.request import urlopen


def get_req():  # 1. 接收用户的输入数据
    print("\nPlease enter the type of currency you have on hand, \n" +
          "the type of currency you want to exchange to, \n" +
          "and the amount of money to exchange.")
    print("Currency you hold: ")
    a = input()
    print("Currency you want to exchange to: ")
    b = input()
    print("The amount of the currency to exchange: ")
    c = input()
    return a, b, c


def is_amo_val(amo):  # 2. 判断货币量的输入值是否合法
    try:
        amo = float(amo)
    except ValueError:
        if_val = 0
    else:
        if amo > 0:
            if_val = 1
        else:
            if_val = 0
    return if_val


def exchange_web(currency_1, currency_2, amount_1):
    # 3. 向网站发送兑换货币的请求，并接收网站给出结果
    list_url = ["http://cs1110.cs.cornell.edu/2016fa/a1server.php?from=",
                currency_1, "&to=", currency_2, "&amt=", amount_1]
    doc = urlopen("".join(list_url))
    docstr = doc.read()
    doc.close()
    jstr = docstr.decode('ascii')
    return jstr


def analyse(jstr):  # 4. 分析网站给出的结果
    list_re = jstr.split()
    num0 = list_re.index('"from"')
    num1 = list_re.index('"success"')
    num2 = list_re.index('"to"')
    before = list_re[num0 + 3: num2]
    if list_re[num1 + 2] == 'true,':
        output_o = list_re[num2 + 2: num1]
        con = 0
    else:
        num4 = list_re.index('"error"')
        output_o = list_re[num4 + 2: -1]
        con = 1
    return [con, output_o, before]


def round_val(val):  # 5. 将数字四舍五入至小数点后两位
    val = val.strip('"')
    val = float(val) * 100
    a = round(val, 0) / 100
    return str("%.2f" % a)


def feedback(con, out, before, amount_from):  # 6. 将格式变为向用户输出的结果
    # 如可兑换，货币量四舍五入至小数点后两位,省略结尾的零;如不可兑换，显示原因。
    out_1 = " ".join(out)
    out_1 = out_1.strip('",')
    if con == 0:
        text = ('The amount of currency for exchange: \n' +
                amount_from + " " + (" ".join(before)).strip('",') +
                '\nThe amount of currency you will get ' +
                'after the exchange process: \n' + out_1)
    elif con == 1:
        text = ('error: \n' + out_1)
    return text


def exchange(currency_from, currency_to, amount_from):  # 货币兑换
    jstr = exchange_web(currency_from, currency_to, amount_from)
    res = analyse(jstr)
    if res[0] == 0:
        res[1][0] = round_val(res[1][0])
    return feedback(res[0], res[1], res[2], amount_from[2])


def main():
    req = get_req()
    if is_amo_val(req[2]) == 1:
        print(exchange(req[0], req[1], req[2]))
    if is_amo_val(req[2]) == 0:
        print("The amount you input is invalid.")


#  测试函数部分
def test_is_amo_val():  # 测试“2. 判断货币量的输入值是否合法”
    assert(1 == is_amo_val(2.5))
    assert(0 == is_amo_val("abc"))
    assert(0 == is_amo_val(-1.5))


def test_exchange_web():  # 测试“3. 向网站发送兑换货币的请求，并接收网站给出结果”
    assert('{ "from" : "2.5 United States Dollars", "to" : ' +
           '"2.1589225 Euros", "success" : true, "error" : "" }'
           == exchange_web('USD', 'EUR', '2.5'))
    assert('{ "from" : "2.5 United States Dollars", "to" : ' +
           '"17.13025 Chinese Yuan", "success" : true, "error" : "" }'
           == exchange_web('USD', 'CNY', '2.5'))
    assert('{ "from" : "", "to" : "", "success" : false, "error" : ' +
           '"Exchange currency code is invalid." }'
           == exchange_web('USD', 'CNN', '2.5'))


def test_analyse():  # 测试“4. 分析网站给出的结果”
    assert([0, ['"17.13025', 'Chinese', 'Yuan",'],
            ['United', 'States', 'Dollars",']] ==
           analyse('{ "from" : "2.5 United States Dollars", ' +
                   '"to" : "17.13025 Chinese Yuan", "success" : ' +
                   'true, "error" : "" }'))


def test_round_val():  # 测试“5. 将数字四舍五入至小数点后两位”
    assert('1.52' == round_val('"1.524'))
    assert('1.44' == round_val('"1.44499999999999999'))
    assert('1.50' == round_val('"1.49999999999999999'))


def test_feedback():  # 测试“6. 将格式变为向用户输出的结果”
    assert(('The amount of currency for exchange: \n' +
            str(2.5) + " " + 'United States Dollars' +
            '\nThe amount of currency you will get ' +
            'after the exchange process: \n' + '17.13025 Chinese Yuan')
           == feedback(0, ['"17.13025', 'Chinese', 'Yuan",'],
                       ['United', 'States', 'Dollars",'], str(2.5)))
    assert ('error: \n' + 'Exchange currency code is invalid.' ==
            feedback(1, ['"Exchange', 'currency', 'code', 'is', 'invalid."'],
                     [], str(2.5)))
    assert ('error: \n' + 'Source currency code is invalid.' ==
            feedback(1, ['"Source', 'currency', 'code', 'is', 'invalid."'],
                     [], str(4)))


def testall():  # 依次进行以上测试
    test_is_amo_val()
    test_exchange_web()
    test_analyse()
    test_round_val()
    test_feedback()
    print("All tests passed.")


def start():  # 最初显示界面
    print('Would you like to run test module?\n' +
          'Please input "Yes" or "No".\n' +
          'If you input other characters, the test module will not run.')
    a = input()
    if a == "Yes":
        testall()


if __name__ == '__main__':
    start()
    main()
