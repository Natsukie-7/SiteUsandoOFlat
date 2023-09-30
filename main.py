import flet as ft

def main(pagina):
    texto = ft.Text("Mini-Chat")

    chat = ft.Column()
    nome_usuario = ft.TextField(label="Insira seu nome estranho....")

    def enviar_menssagem_tunel(menssagem):
        tipo = menssagem.get("tipo")
        usuario = menssagem.get("usuario")
        if tipo == "menssagem":
            texto_menssagem = menssagem.get("texto")
            chat.controls.append(ft.Text(f"{usuario}: {texto_menssagem}"))

        else:
            chat.controls.append(ft.Text(f"{usuario} Entrou no chat"))


        pagina.update()

    #PUBSUB
    pagina.pubsub.subscribe(enviar_menssagem_tunel)

    def enviar_menssagem(evento):
        pagina.pubsub.send_all({
        "usuario": nome_usuario.value,
        'texto': campo_mensagem.value,
        "tipo": "menssagem"
        })
        campo_mensagem.value = ''

        pagina.update()


    campo_mensagem = ft.TextField(label="Sobre o que iremos falar?")
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_menssagem)

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        pagina.add(chat)
        popup.open = False
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        pagina.add(ft.Row([
            campo_mensagem,
            botao_enviar_mensagem
        ]))
        pagina.update()

    popup = ft.AlertDialog(
        open=False, 
        modal=True,
        title=ft.Text("Bem Vindo Estranho"),
        content=nome_usuario,
        actions=[
            ft.ElevatedButton(
                "Entrar", 
                on_click=entrar_popup
            )
        ])

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton(
        "Iniciar chat", 
        on_click=entrar_chat,
    )

    pagina.add(texto)
    pagina.add(botao_iniciar)

ft.app(target=main, view=ft.WEB_BROWSER)