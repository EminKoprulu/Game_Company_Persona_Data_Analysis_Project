import numpy as np
import pandas as pd
import seaborn as sns

# Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz.
df = pd.read_csv("datasets/persona.csv")
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 500)
df.head()
df.info()
df.shape

# Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()
df["SOURCE"].value_counts()

# Soru 3: Kaç unique PRICE vardır?
df["PRICE"].nunique()
df["PRICE"].value_counts()

# Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

# Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df["COUNTRY"].value_counts()
df.groupby("COUNTRY")["PRICE"].count()  # alternatif

# Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE": "sum"})

# Soru 7: SOURCE türlerine göre satış sayıları nedir?
df.groupby("SOURCE").agg({"PRICE": "count"})
df["SOURCE"].value_counts()  # alternatif

# Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": "mean"})

# Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"})

# Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?
df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

# Görev 2: COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"})


# Görev 3: Çıktıyı PRICE’a göre azalan şekilde sıralayınız.
agg_df = df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}).sort_values("PRICE", ascending=False)


# Görev 4: Indekste yer alan isimleri değişken ismine çeviriniz.
agg_df.reset_index(inplace=True)  # index sütunu da gelir!!


# Görev 5: Age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.
agg_df["AGE"].describe()
agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 30, 40, agg_df["AGE"].max()], labels=['0_18', '19_23', '24_30', '31_40', '41_' + str(agg_df["AGE"].max())])
# 6 bins varken 5 label var!!




# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
    # Persona tanımlamak:
agg_df["customers_level_based"] = agg_df[["COUNTRY", "SOURCE", "SEX", "AGE_CAT"]].apply(lambda x: "_".join(x).upper(),axis=1)
    # kolay alternatif:
for row in agg_df.values:  # bu döngü sütunların value'lerini gösterir
    print(row)
agg_df["customers_level_based"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[2].upper() + "_" + row[5].upper() for row in agg_df.values]

    # personaların price'larını inceleyelim:
agg_df = agg_df[["customers_level_based", "PRICE"]]

    # değerleri tekilleştirme
agg_df["customers_level_based"].value_counts()
agg_df = agg_df.groupby("customers_level_based").agg({"PRICE": "sum"})
agg_df = agg_df.reset_index()
agg_df["customers_level_based"].value_counts()  # her personadan birer tane var



# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, labels=["D", "C", "B", "A"])
    # Segmentleri betimleyiniz.
agg_df.groupby("SEGMENT").agg({"PRICE": ["sum", "max", "mean"]})


# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.

    # 33 yaşında ANDROID kullanan bir Türk kadını hangi segmenteaittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user = "TUR_ANDROID_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]

    # 35 yaşında IOS kullanan bir Fransız kadını hangi segmente aittir ve ortalama ne kadar gelir kazandırması beklenir?
new_user2 = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user2]




















