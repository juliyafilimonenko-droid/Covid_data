import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def main():
    print("--- DEL 1: INDLÆS DATA ---")


    dato = pd.Timestamp('2020-05-26')

    dato_str = dato.strftime('%m-%d-%Y')
    path = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{dato_str}.csv'

    print(f"Henter data fra: {path}")
    df = pd.read_csv(path)

    print("\n--- df.head() ---")
    print(df.head())

    print("\n--- df.info() ---")
    df.info()

    print("\n--- DEL 2: DATARENSNING ---")

    df_renset = df.rename(columns={
        'Country_Region': 'Country',
        'Lat': 'Latitude',
        'Long_': 'Longitude'
    })

    kolonner = ["Country", "Latitude", "Longitude", "Confirmed", "Deaths", "Recovered", "Active"]
    df_renset = df_renset[kolonner].copy()

    df_renset = df_renset.fillna(0)

    print("Renset dataframe overblik:")
    print(df_renset.head())

    print("\n--- DEL 3: GRUPPÉR DATA ---")

    df_grupperet = df_renset.groupby('Country')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()

    top_10 = df_grupperet.nlargest(10, 'Confirmed')

    print("\nTop 10 lande med flest bekræftede tilfælde:")
    print(top_10[['Country', 'Confirmed', 'Deaths']])

    print("\n--- DEL 4: VISUALISERING ---")

    sns.set_theme(style="whitegrid")

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=top_10,
        x='Confirmed',
        y='Country',
        hue='Country',
        dodge=False,
        palette='viridis',
        legend=False
    )
    plt.title('Top 10 lande: Bekræftede COVID-19 tilfælde (26. Maj 2020)', fontsize=14)
    plt.xlabel('Antal bekræftede tilfælde', fontsize=12)
    plt.ylabel('Land', fontsize=12)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 8))
    plt.pie(
        top_10['Deaths'],
        labels=top_10['Country'],
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette('pastel')[0:10]
    )
    plt.title('Fordeling af dødsfald blandt de 10 mest smittede lande', fontsize=14)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()