import sqlite3
import flet as ft
import os

DB_PATH = "filtros_wega.db"


def main(page: ft.Page):
    page.title = "Consulta Wega - LMAutoProg"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = ft.ScrollMode.AUTO

    campo_montadora = ft.TextField(label="Montadora")
    campo_modelo = ft.TextField(label="Modelo")
    lista = ft.Column(spacing=10)

    def buscar(e):
        lista.controls.clear()

        try:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM catalogo WHERE modelo LIKE ? AND classificacao LIKE ?"
            cursor.execute(query, (f"%{campo_montadora.value.strip()}%", f"%{campo_modelo.value.strip()}%"))
            resultados = cursor.fetchall()

            if not resultados:
                lista.controls.append(ft.Text("Nenhum resultado encontrado."))
            else:
                for row in resultados:
                    lista.controls.append(
                        ft.Card(content=ft.Container(
                            ft.Column([
                                ft.Text(f"🚗 {row['modelo']} - {row['classificacao']}", weight="bold", size=16,
                                        color="blue"),

                                # A coluna 'ano' agora será exibida exatamente como está no banco
                                ft.Container(
                                    content=ft.Text(f"📅 Ano: {row['ano']}", weight="bold", color="black"),
                                    bgcolor="grey200",
                                    padding=5,
                                    border_radius=5
                                ),

                                ft.Divider(),

                                ft.Text(f"💨 Filtro de Ar: {row['filtro_ar']}"),
                                ft.Text(
                                    f"🛢 Filtro de Óleo: {row['filtro_oleo']} {'(Opc: ' + row['filtro_oleo_opcional'] + ')' if row['filtro_oleo_opcional'] else ''}"),
                                ft.Text(
                                    f"⛽ Filtro de Combustível: {row['filtro_combustivel']} {'(Opc: ' + row['filtro_combustivel_opcional'] + ')' if row['filtro_combustivel_opcional'] else ''}"),
                                ft.Text(
                                    f"❄️ Filtro de Cabine: {row['filtro_cabine']} {'(Carvão: ' + row['filtro_cabine_carvao'] + ')' if row['filtro_cabine_carvao'] else ''}"),
                            ]),
                            padding=15
                        ))
                    )
            conn.close()
        except Exception as err:
            lista.controls.append(ft.Text(f"Erro ao buscar: {err}"))
        page.update()

    page.add(
        ft.Text("Consulta de Filtros", size=20, weight="bold"),
        campo_montadora,
        campo_modelo,
        ft.ElevatedButton("Pesquisar", on_click=buscar, bgcolor="blue", color="white"),
        lista
    )


if __name__ == "__main__":
    ft.app(target=main)