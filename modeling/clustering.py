import psycopg2

import boto3

import pandas as pd
from pandasql import sqldf

from sklearn.cluster import KMeans

def handler(user = "postgres",password = "1234",host = "localhost"):
    """
    Function to fetch neighborhood data, clustering and find types of location.

    Params:
    - user            : PostgreSQL' user.
    - password        : PostgreSQL' password.
    - host            : PostgreSQL' endpoint. 
    """
    
    # IMPORT DATA  
    conn = psycopg2.connect(
        host=host,
        database="xox",
        user=user,
        password=password
    )

    cur = conn.cursor()

    cur.execute("""
    select
        *
    from
        cep_features
    """)

    data = cur.fetchall()
    data = pd.DataFrame(
        data,
        columns=[
            'CEP',
            'qtd_esporte',
            'qtd_mercado',
            'qtd_educacao',
            'qtd_cultura',
            'qtd_saude',
            'qtd_policia',
            'qtd_turismo',
            'qtd_condominio',
            'qtd_restaurante',
            'qtd_industria',
            'qtd_ocorrencias_risco',
            'qtd_estacoes_bikes',
            'qtd_onibus',
            'qtd_area_verde',
            'qtd_pracas',
            'qtd_feiras'        
        ]
    )

    # NORMALIZING FEATURES
    def standardization(feature):
        """
        Transform features values to standard deviation as unit.

        Params:
        - feature : list
        """
        total = sum(feature)
        mean = total / len(feature)
        ratio = [v * 100.0 / total for v in feature]
        std_values = [(v - mean) / mean for v in ratio]

        return std_values

    for col in data.columns:
        if col != 'CEP':
            data[f"{col.replace('qtd','diff')}"] = standardization(data[col].values.tolist())
        else:
            print("It's just the CEP. We can jump that column.")

    # MODELING DATA
    clusters = KMeans(
        n_clusters=8, 
        random_state=0
        ).fit(
        data[[col for col in data.columns if col.startswith('diff')]]
        )

    # RE-LABELING CLUSTERS
    labels = [
        'outros','outros','estudar_perto_de_casa','vida_ativa','vida_em_familia',\
        'passeio_ao_ar_livre','outros','outros'
    ]

    clusters_labels = [labels[c] for c in clusters.labels_]

    cluster_data = pd.DataFrame({
        'CEP' : data['CEP'].values.tolist(),
        'TIPO_LUGAR' : clusters_labels
    })

    # INSERT DATA INTO DATABASE
    rows = data.values.tolist()
    
    # inserting row by row
    for row in rows:
        sql = f"""
        INSERT INTO lugares VALUES
            {tuple(row)};
        """

        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    handler()