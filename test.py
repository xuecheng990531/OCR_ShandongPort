import re
text='经营asdqw范c围；求饿哦我的吧'
pattern = re.compile(r'经\s*营\s*范\s*围', re.IGNORECASE)
esult = re.sub(pattern, '', text)
print(esult)