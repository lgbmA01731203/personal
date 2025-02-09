import json
import argparse
import time


def left_join_json(json1_path, json2_path):
    """Left join, calcula 'Sales', excluye 'title' y maneja errores."""
    try:
        with open(json1_path, 'r') as f1:
            try:
                data1 = json.load(f1)
            except json.JSONDecodeError:
                print(f"Error: Archivo JSON {json1_path} inválido.")
                return None

        with open(json2_path, 'r') as f2:
            try:
                data2 = json.load(f2)
            except json.JSONDecodeError:
                print(f"Error: Archivo JSON {json2_path} inválido.")
                return None

    except FileNotFoundError:
        print("Error: Uno o ambos archivos json no se encontraron")
        return None

    if data1 is None or data2 is None:
        return None

    result = []
    for item2 in data2:
        match = False
        for item1 in data1:
            if item2.get('Product') == item1.get('title'):
                try:
                    sales = item1.get('price', 0) * item2.get('Quantity', 0)
                    sales = round(sales, 2)
                    result.append({
                        'SALE_ID': item2.get('SALE_ID'),
                        'Product': item2.get('Product'),
                        'Quantity': item2.get('Quantity'),
                        'price': item1.get('price'),
                        'Sales': sales
                    })
                    match = True
                    break
                except TypeError:
                    print(f"Error {item2.get('Product')}. Se usará 0.")
                    sales = 0
                    result.append({
                        'SALE_ID': item2.get('SALE_ID'),
                        'Product': item2.get('Product'),
                        'Quantity': item2.get('Quantity'),
                        'price': item1.get('price'),
                        'Sales': sales
                    })
                    match = True
                    break

        if not match:
            result.append({
                'SALE_ID': item2.get('SALE_ID'),
                'Product': item2.get('Product'),
                'Quantity': item2.get('Quantity'),
                'price': None,
                'Sales': None
            })

    return result


def write_results_to_file(results, output_file, total_sales):
    """Escribe resultados y suma"""
    results_with_sales = {"results": results, "total_sales": total_sales}
    try:
        with open(output_file, 'w') as f:
            json.dump(results_with_sales, f, indent=4)
    except Exception as e:
        print(f"Error al escribir en el archivo: {e}")


if __name__ == "__main__":
    start_time = time.time()

    parser = argparse.ArgumentParser(
        description="Realiza left join entre dos archivos JSON."
    )
    parser.add_argument("json1_path", help="Ruta al primer archivo JSON.")
    parser.add_argument("json2_path", help="Ruta al segundo archivo JSON.")
    parser.add_argument(
        "-o",
        "--output",
        help="Nombre del archivo de salida (opcional)",
        default="SalesResults.txt",
    )

    args = parser.parse_args()

    result = left_join_json(args.json1_path, args.json2_path)

    if result is not None:
        total_sales = 0
        for item in result:
            print(item)
            if item.get('Sales') is not None:
                total_sales += item['Sales']

        end_time = time.time()
        elapsed_time = end_time - start_time

        write_results_to_file(result, args.output, total_sales)

        print(f"\nResultados guardados en {args.output}")
        print(f"Tiempo de ejecución: {elapsed_time:.4f} segundos")
        print(f"Suma total de ventas: {total_sales:.2f}")
    else:
        print("El programa ha terminado debido a errores en los archivos.")
