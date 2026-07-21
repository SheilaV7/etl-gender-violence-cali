from services.api_client import DatosGovClient

def main():

    client = DatosGovClient()

    datos = client.get_dataset(
        "fpe5-yrmw",
        {
            "$where": "municipio='Cali (CT)'"
        }
    )

    print(datos)

if __name__ == "__main__":
    main()
