###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################

#############################################################
# GÖREVLER
###############################################################

    import datetime as dt
    import pandas as pd
    pd.set_option("display.max_columns", None)
    pd.set_option("display.float_format", lambda x: "%.3f" % x)


# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
 df_=pd.read_csv("WEEK 3/flo_data_20k.csv")
 df=df_.copy()
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     df.head(10)

                     # b. Değişken isimleri,
                     df.columns

                     # c. Betimsel istatistik,
                     df.describe().T.head()

                     # d. Boş değer,
                     df.isnull().sum()

                     # e. Değişken tipleri, incelemesi yapınız.
                     df.dtypes

           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           df["total_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
           df["total_price"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.

             date_col = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
             for col in date_col:

               df[col]= pd.to_datetime(df[col])
               df.dtypes

           # 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısının ve toplam harcamaların dağılımına bakınız.
            df["master_id "].describe().T
            df["total_order"].describe().T
            df["total_price"].describe().T

           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           df["max_customer"] = df["total_price"].sort_values(ascending=False).head(10)
            df.groupby("master_id","max_customer")

           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           df["total_order"].sort_values().head(10)

           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

           def create_rfm_new(dataframe):

            df[otal_order"] = df["order_num_total_ever_online"] + df["order_num_total_ever_offline"]
            df["total_price"] = df["customer_value_total_ever_online"] + df["customer_value_total_ever_offline"]

            df_col = ["first_order_date", "last_order_date", "last_order_date_online", "last_order_date_offline"]
            for col in df_col:
                df[col] = pd.to_datetime(df[col])

            return

    #GÖREV 2: RFM Metriklerinin Hesaplanması
    #Recency,Frequency,Monetary

    #Adım 1: Recency, Frequency ve Monetary tanımlarını yapınız.
    #Recency:Son ürün alma tarihi
    #Frequency:Ürün alım sıklığı
    #Monetary:Son bırakılan parasal değer

    #Adım 2: Müşteri özelinde Recency, Frequency ve Monetary metriklerini hesaplayınız.
    df["last_order_date"].max()
    today_date = dt.datetime(2021,6,1)

    #rfm = (df.groupby("master_id").agg({"last_order_date":lambda date : (today_date - last_order_date.max()).days,"total_order": lambda number_of_orders : total_order.sum(),"total_price": lambda total_value : total_price.sum() })

    df["Recency"] = [(today_date - date).days for date in df["last_order_date"]]
    df["Frequency"] = df["total_order"]
    df["Monetary"] = df["total_price"]
    #Adım 3: Hesapladığınız metrikleri rfm isimli bir değişkene atayınız.Adım 4: Oluşturduğunuz metriklerin isimlerini recency, frequency ve monetary olarak değiştiriniz.
    rfm = df[["master_id", "Recency", "Frequency", "Monetary"]]

    #GÖREV 3: RF Skorunun Hesaplanması
    rfm["recency_score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1])
    rfm["frequency_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5])
    rfm["monetary_score"] = pd.qcut(rfm["Monetary"], 5, labels=[1, 2, 3, 4, 5])

    rfm["RF_SCORE"]  = rfm["recency_score"].astype(str) + rfm["frequency_score"].astype(str)

   #Görev 4: RF Skorunun Segment Olarak Tanımlanması
   seg_map = {
        r'[1-2][1-2]': 'hibernating',  # birinci ve ikinci elemanında 1 ya da 2 görürsen 'hibernating' diye isimlendir
        r'[1-2][3-4]': 'at_Risk',
        r'[1-2]5': 'cant_loose',
        r'3[1-2]': 'about_to_sleep',
        r'33': 'need_attention',  # birinci ve ikini elemanı 3 ise 'need_attention' diye isimlendir
        r'[3-4][4-5]': 'loyal_customers',
        r'41': 'promising',
        r'51': 'new_customers',
        r'[4-5][2-3]': 'potential_loyalists',
        r'5[4-5]': 'champions'
    }

   rfm["segment"]=rfm["RFM_SCORE"].replace(seg_map,regex=True)