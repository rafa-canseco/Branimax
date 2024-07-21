from promuevo.utilsPromuvo.historyPromuevo import clear_history
from promuevo.services.spreadsheet import write_lead
from functions.querys_db import delete_state


async def flow_recruit(state,body,from_number,database):
    if not state.get('recruitment_phase'):
        state.update({'recruitment_phase': True})

    if "cancelar" in body.lower():
        clear_history(state)
        state.update({'recruitment_phase': False})
        return "¿Cómo puedo ayudarte? 😊"
    
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
            'name': state.get('name'),
            'age': state.get('age'),
            'city': state.get('city'),
            'education_level': state.get('education_level'),
            'desired_position': state.get('desired_position'),
            'email': state.get('email'),
            'phone': state.get('phone')
        }
        response = ( 
            f"¡Gracias {state.get('name')}! Hemos recibido tus datos:"
            f"Edad: {state.get('age')}"
            f"Ciudad: {state.get('city')}"
            f"Nivel de estudios: {state.get('education_level')}"
            f"Puesto deseado: {state.get('desired_position')}"
            f"Email: {state.get('email')}"
            f"Teléfono: {state.get('phone')}"
        )
        await write_lead(date_object)
        
        state.state.clear()
        
        # Eliminar el estado de la base de datos
        delete_state(database, from_number)
        
        return response

    return "Lo siento, ha ocurrido un error en el proceso de reclutamiento. ¿En qué más puedo ayudarte?"
    



