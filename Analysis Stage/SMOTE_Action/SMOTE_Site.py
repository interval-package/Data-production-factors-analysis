from imblearn.over_sampling import SMOTE, ADASYN

X_resampled_smote, y_resampled_smote = SMOTE().fit_sample(X, y)

sorted(Counter(y_resampled_smote).items())
Out[29]:
[(0, 4674), (1, 4674), (2, 4674)]

X_resampled_adasyn, y_resampled_adasyn = ADASYN().fit_sample(X, y)

sorted(Counter(y_resampled_adasyn).items())
Out[30]:
[(0, 4674), (1, 4674), (2, 4674)]


X_resampled, y_resampled = SMOTE(kind='borderline1').fit_sample(X, y)

print()
sorted(Counter(y_resampled).items())
Out[31]:
[(0, 4674), (1, 4674), (2, 4674)]