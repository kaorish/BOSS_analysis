import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 读取停用词
with open("stopwords_cn.txt", "r", encoding="gb18030") as f:
    stopwords = f.read().splitlines()
# 读取所需技能文本
with open("skill_gb18030.txt", "r", encoding="gb18030") as f:
    text = f.read()

# 使用jieba进行分词
words = jieba.cut(text)

# 统计词频
word_freq = {}
for word in words:
    if word not in stopwords and len(word) > 1:
        word_freq[word] = word_freq.get(word, 0) + 1

# 绘制词云图
wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='msyh.ttc').generate_from_frequencies(word_freq)

plt.figure(figsize=(10, 6))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
