print(reversed('parrot'))
print(list(reversed('parrot')))
print(''.join(reversed('parrot')))


def is_palindrome(word):
    """判斷字串是否為回文"""
    return word == ''.join(reversed(word))

# 測試範例
print(is_palindrome("noon"))       # True
print(is_palindrome("rotator"))    # True
print(is_palindrome("parrot"))     # False
print(is_palindrome("hello"))      # False

# 假設有一個單字列表
word_list = ["racecar", "rotator", "deified", "civic", "noon", "level", "hello", "python"]

# 找出長度至少 7 的回文詞
for word in word_list:
    if len(word) >= 7 and is_palindrome(word):
        print(word)
