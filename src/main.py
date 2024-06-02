from nicegui import ui
import re
from email_validator import validate_email, EmailNotValidError
import phonenumbers
from phonenumbers import NumberParseException

@ui.page('/cliente_cadastro')
def new_customer_page():
    ui.markdown('## Cadastro Cliente')

    with ui.row():
        def validate_name(event):
            value = event.value
            if not re.fullmatch(r'[A-Za-zÀ-ÖØ-öø-ÿ ]+', value):
                ui.notify('Nome deve conter apenas letras', type='error')
            return value

        name = ui.input(label='Nome',
                        placeholder='Digite o nome',
                        on_change=validate_name)
        
        def validate_lastname(event):
            value = event.value
            if not re.fullmatch(r'[A-Za-zÀ-ÖØ-öø-ÿ ]+', value):
                ui.notify('Nome deve conter apenas letras', type='error')
            return value

        lastname = ui.input(label='Sobrenome',
                            placeholder='Digite o sobrenome',
                            on_change=validate_lastname)
    
        with ui.input('Data de Nascimento') as date:
            with date.add_slot('append'):
                ui.icon('edit_calendar').classes('cursor-pointer')
            with ui.menu() as menu:
                ui.date().bind_value(date)
    
    with ui.row():
        document_id = (ui.input(label="CPF",
                                placeholder='Digite o CPF',
                                validation={'Entre com 11 valores para cpf': lambda value: len(value == 14)})
                            .props('mask="###.###.###-##"'))
        
        email = ui.input(label='Email',
                    placeholder='Digite com o email')
        
        phone1 = ui.input(label='Telefone',
                    placeholder='Digite o telefone')

        def validate_email_input(email_value):
            try:
                # Validação do email
                valid = validate_email(email_value)
                return valid.email, ""
            except EmailNotValidError as e:
                return "", str(e)
        
        def validate_phone(phone_value):
            try:
                parsed_phone = phonenumbers.parse(phone_value, "BR")  # "BR" é o código do país para o Brasil
                if not phonenumbers.is_possible_number(parsed_phone):
                    return "", 'Telefone não é possível'
                elif not phonenumbers.is_valid_number(parsed_phone):
                    return "", 'Telefone não é válido'
                else:
                    formatted_phone = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.NATIONAL)
                    return formatted_phone, ""
            except NumberParseException:
                return "", 'Formato de telefone inválido'
        
    def get_values():
        email_value, email_error = validate_email_input(email.value)
        if email_error:
            ui.notify(email_error, type='error')
            return

        # Validar telefone
        phone_value, phone_error = validate_phone(phone1.value)
        if phone_error:
            ui.notify(phone_error, type='error')
            return
        
        if name.value and document_id.value:
            ui.notify('Cadastro realizado com sucesso.', color='green')
        else:
            ui.notify('Entre com os dados necessários', type='error', color='red')

    ui.button('Cadastrar', on_click=get_values)
    ui.button('Ínicio', on_click=lambda: ui.navigate.to('/'))

@ui.page('/cliente')
def customer_page():
    ui.markdown('Cliente')


ui.markdown('## Boas vindas ao Stúdio Caju')

ui.markdown('----')
ui.markdown('### Clientes')

with ui.row():
    ui.button('Cadastrar', on_click=lambda: ui.navigate.to('/cliente_cadastro'))

ui.run()

