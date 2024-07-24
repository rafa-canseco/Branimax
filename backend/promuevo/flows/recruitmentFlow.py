from promuevo.utilsPromuvo.historyPromuevo import clear_history
from promuevo.services.spreadsheet import write_lead
from functions.querys_db import delete_state


async def flow_recruit(state, body, from_number, database):
    if not state.get('recruitment_phase'):
        state.update({'recruitment_phase': True})
        state.state.clear()  
        clear_history(state)  

    if "cancelar" in body.lower():
        return reset_recruitment_state(state, database, from_number)
    
    if not state.get('name'):
        if not state.get('name_prompted'):
            state.update({'name_prompted': True})
            return "Ok, voy a pedirte unos datos. ¿Cuál es tu nombre? 😊📝"
        else:
            state.update({'name':body})
            state.update({'name_prompted': False})
            return "cual es tu edad? 📝"
        
    if not state.get('age'):
        state.update({'age': body})
        return "¿Cuál es tu ciudad de residencia? 🏙️"
    
    if not state.get('city'):
        state.update({'city' : body})
        return "¿Cuál es tu nivel de estudios? 🎓"
    
    if not state.get('education_level'):
        state.update({'education_level':body})
        return "¿Cuál es el puesto deseado? (demovendedor, demostrador, promotor) 🏢"
    
    if not state.get('desired_position'):
        state.update({'desired_position': body})
        return "¿Cuál es tu email? 📧"
    
    if not state.get('email'):
        state.update({'email': body})
        return "¿Cuál es tu teléfono? 📞"
    
    if not state.get('phone'):
        state.update({'phone': body})
        
        date_object = {
            'nombre': state.get('name'),
            'edad': state.get('age'),
            'ciudad': state.get('city'),
            'nivelEstudios': state.get('education_level'),
            'puestoRequerido': state.get('desired_position'),
            'email': state.get('email'),
            'telefono': state.get('phone')
        }
        response = ( 
            f"¡Gracias {state.get('name')}! Hemos recibido tus datos:\n"
            f"Edad: {state.get('age')}\n"
            f"Ciudad: {state.get('city')}\n"
            f"Nivel de estudios: {state.get('education_level')}\n"
            f"Puesto deseado: {state.get('desired_position')}\n"
            f"Email: {state.get('email')}\n"
            f"Teléfono: {state.get('phone')}\n\n"
            "¿En qué más puedo ayudarte?"
        )
        await write_lead(date_object)
        
        return reset_recruitment_state(state, database, from_number)

    return "Lo siento, ha ocurrido un error en el proceso de reclutamiento. ¿En qué más puedo ayudarte?"


def reset_recruitment_state(state, database, from_number):
    state.state.clear()  # Limpia completamente el estado
    state.update({'recruitment_phase': False, 'has_interacted': True, 'reset_conversation': True})  # Reinicia las variables clave
    clear_history(state)  # Limpia el historial
    delete_state(database, from_number)  # Elimina el estado de la base de datos
    return "Proceso de reclutamiento finalizado. ¿En qué más puedo ayudarte?"
