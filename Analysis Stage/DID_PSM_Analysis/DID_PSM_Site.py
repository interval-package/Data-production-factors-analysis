import psmatching.match as psm
import pytest
import pandas as pd
import numpy as np
from psmatching.utilities import *
import statsmodels.api as sm

# ===================================================================================================================

# 地址
path = "./data/psm/psm_gxslsj_data.csv"
# model由干预项和其他类别标签组成，形式为"干预项~类别特征+列别特征。。。"
model = "PUSH ~ AGE + SEX + VIP_LEVEL + LASTDAY_BUY_DIFF + " \
        "PREFER_TYPE + LOGTIME_PREFER + USE_COUPON_BEFORE + ACTIVE_LEVEL"
# 想要几个匹配项，如k=3，那一个push=1的用户就会匹配三个push=0的近似用户
k = "3"
m = psm.PSMatch(path, model, k)

# ===================================================================================================================


def PsMatching_ReIm(path, model, k):
    df = pd.read_csv(path)
    # 将用户ID作为数据的新索引
    df = df.set_index("ID")
    print("\n计算倾向性匹配得分 ...", end=" ")
    # 利用逻辑回归框架计算倾向得分，即广义线性估计 + 二项式Binomial
    glm_binom = sm.formula.glm(formula=model, data=df, family=sm.families.Binomial())
    # 拟合拟合给定family的广义线性模型
    # https://www.w3cschool.cn/doc_statsmodels/statsmodels-generated-statsmodels-genmod-generalized_linear_model-glm-fit.html?lang=en
    result = glm_binom.fit()
    # 输出回归分析的摘要
    # print(result.summary)
    propensity_scores = result.fittedvalues
    print("\n计算完成!")
    # 将倾向性匹配得分写入data
    df["PROPENSITY"] = propensity_scores

    # ===================================================================================================================

    groups = df.PUSH
    propensity = df.PROPENSITY
    # 把干预项替换成True和False
    groups = groups == groups.unique()[1]
    n = len(groups)
    # 计算True和False的数量
    n1 = groups[groups == 1].sum()
    n2 = n - n1
    g1, g2 = propensity[groups == 1], propensity[groups == 0]
    # 确保n2>n1，,少的匹配多的，否则交换下
    if n1 > n2:
        n1, n2, g1, g2 = n2, n1, g2, g1
    # 随机排序干预组，减少原始排序的影响
    m_order = list(np.random.permutation(groups[groups == 1].index))

    # ===================================================================================================================

    matches = {}
    k = int(k)
    print("\n给每个干预组匹配 [" + str(k) + "] 个对照组 ... ", end=" ")
    for m in m_order:
        # 计算所有倾向得分差异,这里用了最粗暴的绝对值
        # 将propensity[groups==1]分别拿出来，每一个都与所有的propensity[groups==0]相减
        dist = abs(g1[m] - g2)
        array = np.array(dist)
        # 如果无放回地匹配，最后会出现要选取3个匹配对象，但是只有一个候选对照组的错误，故进行判断
        if k < len(array):
            # 在array里面选择K个最小的数字，并转换成列表
            k_smallest = np.partition(array, k)[:k].tolist()
            # 用卡尺做判断
            caliper = None
            if caliper:
                caliper = float(caliper)
                # 判断k_smallest是否在定义的卡尺范围
                keep_diffs = [i for i in k_smallest if i <= caliper]
                keep_ids = np.array(dist[dist.isin(keep_diffs)].index)
            else:
                # 如果不用标尺判断，那就直接上k_smallest了
                keep_ids = np.array(dist[dist.isin(k_smallest)].index)
            #  如果keep_ids比要匹配的数量多，那随机选择下，如要少，通过补NA配平数量
            if len(keep_ids) > k:
                matches[m] = list(np.random.choice(keep_ids, k, replace=False))
            elif len(keep_ids) < k:
                while len(matches[m]) <= k:
                    matches[m].append("NA")
            else:
                matches[m] = keep_ids.tolist()
            # 判断 replace 是否放回
            replace = False
            if not replace:
                g2 = g2.drop(matches[m])
    print("\n匹配完成!")

    # ===================================================================================================================


    matches = pd.DataFrame.from_dict(matches, orient="index")
    matches = matches.reset_index()
    column_names = {}
    column_names["index"] = "干预组"
    for i in range(k):
        column_names[i] = str("匹配对照组_" + str(i + 1))
    matches = matches.rename(columns=column_names)

    matched_data = get_matched_data(matches, df)

    # ===================================================================================================================


    print("将倾向性匹配得分写入到文档 ...", end=" ")
    save_file = path.split(".")[0] + "_倾向性匹配得分.csv"
    df.to_csv(save_file, index=False)
    print("完成!")
    print("将匹配结果写入到文档 ...", end=" ")
    save_file = path.split(".")[0] + "_匹配结果.csv"
    matches.to_csv(save_file, index=False)
    print("完成!")

    variables = df.columns.tolist()[0:-2]
    results = {}
    print("开始评估匹配 ...")
    # 注意：将PUSH替换成自己的干预项
    for var in variables:
        # 制作用于卡方检验的频率计数交叉表
        crosstable = pd.crosstab(df['PUSH'], df[var])
        if len(df[var].unique().tolist()) <= 2:
            # 计算 2x2 表的卡方统计量、df 和 p 值
            p_val = calc_chi2_2x2(crosstable)[1]
        else:
            # 计算 2x2 表的卡方统计量、df 和 p 值
            p_val = calc_chi2_2xC(crosstable)[1]
        results[var] = p_val
        print("\t" + var + '(' + str(p_val) + ')', end="")
        if p_val < 0.05:
            print(": 未通过")
        else:
            print(": 通过")
    if True in [i < 0.05 for i in results.values()]:
        print("\n变量未全部通过匹配")
    else:
        print("\n变量全部通过匹配")
