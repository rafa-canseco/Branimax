from promuevo.services.spreadsheet import write_lead
from functions.querys_db import update_user_data, reset_user_data

async def flow_recruit(user_data, body, user_id, database):
    if "cancelar" in body.lower():
        return reset_recruitment_state(database, user_id)
    
    if not user_data.get('name'):
        if not user_data.get('name_prompted'):
            update_user_data(database, user_id, {'name_prompted': True})
            return "Ok, voy a pedirte unos datos. ¿Cuál es tu nombre? 😊📝"
        else:
            update_user_data(database, user_id, {'name': body, 'name_prompted': False})
            return "¿Cuál es tu edad? 📝"
        
    if not user_data.get('age'):
        update_user_data(database, user_id, {'age': body})
        return "¿Cuál es tu ciudad de residencia? 🏙️"
    
    if not user_data.get('city'):
        update_user_data(database, user_id, {'city': body})
        return "¿Cuál es tu nivel de estudios? 🎓"
    
    if not user_data.get('education_level'):
        update_user_data(database, user_id, {'education_level': body})
        return "¿Cuál es el puesto deseado? (demovendedor, demostrador, promotor) 🏢"
    
    if not user_data.get('desired_position'):
        update_user_data(database, user_id, {'desired_position': body})
        return "¿Cuál es tu email? 📧"
    
    if not user_data.get('email'):
        update_user_data(database, user_id, {'email': body})
        return "¿Cuál es tu teléfono? 📞"
    
    if not user_data.get('phone'):
        update_user_data(database, user_id, {'phone': body})
        
        date_object = {
            'nombre': user_data['name'],
            'edad': user_data['age'],
            'ciudad': user_data['city'],
            'nivelEstudios': user_data['education_level'],
            'puestoRequerido': user_data['desired_position'],
            'email': user_data['email'],
            'telefono': body
        }
        response = ( 
            f"¡Gracias {user_data['name']}! Hemos recibido tus datos:\n"
            f"Edad: {user_data['age']}\n"
            f"Ciudad: {user_data['city']}\n"
            f"Nivel de estudios: {user_data['education_level']}\n"
            f"Puesto deseado: {user_data['desired_position']}\n"
            f"Email: {user_data['email']}\n"
            f"Teléfono: {body}\n\n"
            "¿En qué más puedo ayudarte?"
        )
        await write_lead(date_object)
        
        return reset_recruitment_state(database, user_id)

    return "Lo siento, ha ocurrido un error en el proceso de reclutamiento. ¿En qué más puedo ayudarte?"
    

def reset_recruitment_state(database, user_id):
    reset_user_data(database, user_id)
    update_user_data(database, user_id, {
        'recruitment_phase': False,
        'has_interacted': False,
        'history': '[]'  
    })
    return "Proceso de reclutamiento finalizado. ¿En qué más puedo ayudarte?"