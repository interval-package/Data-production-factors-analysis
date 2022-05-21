# 研究数据要素对于企业发展的影响

基本上本项目是基于python，进行数据分析与使用。

数据集使用的是`tushare`

分析库使用的是sklearn

项目地址在这里：https://github.com/interval-package/Data-production-factors-analysis.git

## 数据获取

### `tushare`获取主营业务信息

在网络上找了半天，找了例如`baostock`以及`akshare`等开源数据平台，虽然都很全面，但是就是主营业务的信息一直没有搞到。

所以最后使用了`tushare`来获得该方面数据

我们选择了推荐的80家公司，对其历史信息业务信息进行获取，然后保存在本地。

```python
def get_fina_main(code, stock_type=".SZ"):
    df = pro.fina_mainbz(ts_code=code + stock_type, type='P')
    print(code+"finish")
    df.to_csv("../data/main_prof/{}.csv".format(code), encoding="utf-8", index=False)
    return df
```

## 数据分析与模型构建

### 阶段一：通过主营业务类别进行行业类型划分

#### 数据编码化

对于我们获得的数据，实际上是很离散和非结构化的。

同时我们的获得下来的数据里，每家公司所从事的业务，具有巨大的差异性，内容可能几乎没有相同的。

将字符类型数据转化为数据向量类型的方法，有典型的`one-hot`、`docVec`以及`TF-IDF`算法，在这里我们选用`TF-IDF`进行向量化。

所以我们将每个公司的业务类型进行统计，使用TF-IDF算法对我们的数据进行一个基础的预处理。

##### TF-IDF算法

> **TF-IDF（term frequency–inverse document frequency，词频-逆向文件频率）**是一种用于信息检索（information retrieval）与文本挖掘（text mining）的常用**加权技术**。
>
> TF-IDF是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。**字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降**。
>
> TF-IDF的主要思想是：如果某个单词在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。

我们将数据按照`公司+时间`的规则进行分组，将每一组内的业务类型进行拼接，然后使用`jieba`库对我们拼接好的串进行分词，转化为结构化的类型串。

使用`公司+时间`的规则，则可以看出公司业务内容与占比随着时间而发生的变化。

然后使用`sklearn`的api将目标的内容转化为我们所要的数据矩阵。

#### 聚类分析

在这里针对上一步的分析，我们对处理好的目标数据，进行无监督聚类处理，以聚类结果作为我们划分的依据。

在这里我们使用了两种聚类方法：

- `k_means`
- `dbscan 密度聚类`

详细的算法内容，这里就不再进行解释。
