# 研究数据要素对于企业发展的影响

基本上本项目是基于python，进行数据分析与使用。

数据集使用的是`tushare`

分析库使用的是sklearn

项目地址在这里：https://github.com/interval-package/Data-production-factors-analysis.git

## 数据获取

### `tushare`获取主营业务信息

在网络上找了半天，找了例如`baostock`以及`akshare`等开源数据平台，虽然都很全面，但是就是主营业务的信息一直没有搞到。

所以最后使用了`tushare`来获得该方面数据，`tushare`官网：https://tushare.pro

我们选择了推荐的80家公司，对其历史信息业务信息进行获取，然后保存在本地。

```python
def get_fina_main(code, stock_type=".SZ"):
    df = pro.fina_mainbz(ts_code=code + stock_type, type='P')
    print(code+"finish")
    df.to_csv("../data/main_prof/{}.csv".format(code), encoding="utf-8", index=False)
    return df
```

#### 如何配置数据环境

这里的话，从git上clone下来是没有带有数据的，所以需要进行一个初始化，在共做目录创建文件夹：

```python
"../data/main/prof"

from DataBase.NetData_req.FetchData import *
from DataBase.Load_csv_Data import read_main_bz_csv_data
from DataBase.NetData_req.tushare_home import get_fina_main

from Process_Site.main_prof.proess_factors import FactorProcess

def preloading_data():
    codes = get_codes()
    for code in codes:
        get_fina_main(code)


if __name__ == '__main__':
    preloading_data()
    pass
```

运行，然后就从`tushare`下载好了。

#### 数据简单标定

对于，我们对于营业业务类型先做一个简单的标定。对于有使用数据要素的，标定为1，没有使用的，标定为0。

### 营业状况数据

目标内容：总资产净利率，资产负债率，存货周转率，营业外收入（政府补贴/其他收入），研发投入比，现金流能力（公司流动金额），是否使用数据要素。

# 数据分析与模型构建

## 阶段一：通过主营业务类别进行行业类型划分

### 数据编码化

对于我们获得的数据，实际上是很离散和非结构化的。

同时我们的获得下来的数据里，每家公司所从事的业务，具有巨大的差异性，内容可能几乎没有相同的。

将字符类型数据转化为数据向量类型的方法，有典型的`one-hot`、`docVec`以及`TF-IDF`算法，在这里我们选用`TF-IDF`进行向量化。

所以我们将每个公司的业务类型进行统计，使用TF-IDF算法对我们的数据进行一个基础的预处理。

#### TF-IDF算法

> **TF-IDF（term frequency–inverse document frequency，词频-逆向文件频率）**是一种用于信息检索（information retrieval）与文本挖掘（text mining）的常用**加权技术**。
>
> TF-IDF是一种统计方法，用以评估一字词对于一个文件集或一个语料库中的其中一份文件的重要程度。**字词的重要性随着它在文件中出现的次数成正比增加，但同时会随着它在语料库中出现的频率成反比下降**。
>
> TF-IDF的主要思想是：如果某个单词在一篇文章中出现的频率TF高，并且在其他文章中很少出现，则认为此词或者短语具有很好的类别区分能力，适合用来分类。

我们将数据按照`公司+时间`的规则进行分组，将每一组内的业务类型进行拼接，然后使用`jieba`库对我们拼接好的串进行分词，转化为结构化的类型串。

使用`公司+时间`的规则，则可以看出公司业务内容与占比随着时间而发生的变化。

然后使用`sklearn`的api将目标的内容转化为我们所要的数据矩阵。

### 聚类分析

在这里针对上一步的分析，我们对处理好的目标数据，进行无监督聚类处理，以聚类结果作为我们划分的依据。

在这里我们使用了两种聚类方法：

- `k_means`
- `dbscan 密度聚类`

详细的算法内容，这里就不再进行解释。

对于类型的基本标签，我们可以认为，对于进行信息化的企业，可以分为以下大类：

| type           | 特征 | 分析 |
| -------------- | ---- | ---- |
| 数字产品制造业 |      |      |
| 数字产品服务业 |      |      |
| 数字技术应用业 |      |      |
| 数字要输驱动业 |      |      |

可以看出不同公司的主营业务内容具有一定的区分性，同时一个公司在不同时间段内，进行的主营业务内容也有较大的区分。通过业务分类的标签变化，可以直观地了解到公司的战略变化。

## 阶段二：比对业务投入比划分行业行为特征

对于我们的营业数据，我们会又三个大方面的指标：

- 投资金额 $C_{invest}$
- 销售金额 $C_{sale}$
- 营收金额 $C_{prof}$

设立投资比例系数${\phi}_{fac_{sale}} = C_{sale}/C_{invest}$，${\phi}_{fac_{prof}} = C_{prof}/C_{invest}$认为该比例系数可以反映一个公司对于某个业务的重视程度，以及一定时间段内，公司的投资策略特征。

我们取一段时间内，各公司的该两个系数的平均值，作为我们聚类的向量元素，再次进行聚类分析，划分不同公司在某一时刻的投资策略特征。

与上一阶段的特征，进行比对，确认公司在主营业务变化时，所进行的投资策略的变化。

## 阶段三：使用PCA进行主成分分析



## 阶段四：使用DID-PSM进行前后影响分析



