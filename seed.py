"""Initial seed for the todo database.

The legacy ``todo.html`` shipped with ~127 tasks hardcoded in a JS array.
This module mirrors that array so we can preserve IDs and notes when the
database is created for the first time.

Note: ``LEGACY_TASKS`` keeps the original schema (priority='critica' etc.).
``_transform_legacy`` applies the same migration that ``database._migrate_legacy_schema``
applies, so a fresh seed produces the same result as a migrated database.
"""

from datetime import date

from database import insert_with_id, is_empty, reset_id_sequence


def _transform_legacy(task):
    """Apply the legacy → current schema transformation to a single task dict."""
    out = dict(task)
    if out.get("priority") == "critica":
        out["priority"] = "altisima"
        if out.get("status") == "pendiente":
            out["status"] = "critico"
    out.setdefault("created_at", date.today().isoformat())
    return out

LEGACY_TASKS = [
    {"id": 1,   "title": "Hacer el ticket de CPTIN",                                                      "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 2,   "title": "Enviar mail a Cristian Quiroz",                                                 "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 3,   "title": "Levantamiento de requerimiento Sysmex",                                        "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-07", "notes": "A partir de reunión con Marcelo, Consuelo y cliente."},
    {"id": 4,   "title": "Comprar vestido para el matrimonio",                                           "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 5,   "title": "Lavar vestido de la Rocío",                                                    "category": "domestico", "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 6,   "title": "Mandar mail a clínica para pedir ficha médica",                                "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 7,   "title": "Averiguar licencia de Lovable con Jime",                                       "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 8,   "title": "Gestionar compra de nuevo Mac",                                                "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 9,   "title": "Coordinar workshop IA con el equipo",                                          "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-08", "notes": "Miércoles 8 de abril."},
    {"id": 10,  "title": "Reservar sala de reuniones (miércoles 8 abril)",                               "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-08", "notes": "¡Urgente!"},
    {"id": 11,  "title": "Revisión base instalada — queries de IA",                                      "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": "Identificar clientes donde consultas.consulta = config_historicalsqlgeneration.sql"},
    {"id": 12,  "title": "Averiguar requests promedio en M+",                                            "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "",           "notes": "Documentos y comprobantes cargados mensualmente. Máx y mín. Solo usuarios tipo N con last login dentro del mes."},
    {"id": 13,  "title": "Avanzar con Q4 de Eduardo",                                                    "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": "Urgente."},
    {"id": 14,  "title": "Regalo de Rafaella",                                                            "category": "personal",  "priority": "alta",    "status": "hecho",     "due": "2026-04-11", "notes": "Para el sábado 11 de abril."},
    {"id": 15,  "title": "Hablar con Ivo — crédito del auto",                                            "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 16,  "title": "Crear estado \"No aplica\" en Time",                                           "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": "¡Atrasado hace 2 semanas!"},
    {"id": 17,  "title": "Gestionar compra de licencias Claude para el equipo",                          "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 18,  "title": "Ejecutar ticket MMAS-10658",                                                   "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-02", "notes": "Hoy a las 9PM."},
    {"id": 19,  "title": "Coordinar domingo con la Paola",                                               "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": "Día de cumpleaños y huevitos de chocolate."},
    {"id": 20,  "title": "Enviar resultados médicos de la Fer a doctora Romy",                           "category": "personal",  "priority": "critica", "status": "hecho",     "due": "",           "notes": "¡Atrastadísimo!"},
    {"id": 21,  "title": "Enviar resultados médicos propios a la siquiatra",                             "category": "personal",  "priority": "critica", "status": "hecho",     "due": "",           "notes": "¡Atrastadísima!"},
    {"id": 22,  "title": "Enviar cita de review y planning al equipo",                                   "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-08", "notes": "Para el miércoles 8 de abril."},
    {"id": 23,  "title": "Organizar sprint de abril",                                                    "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-07", "notes": ""},
    {"id": 24,  "title": "Identificar clientes con problemas en usuarios tipo Interfaz",                 "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 25,  "title": "Transferirle a la Naty (aseo)",                                                "category": "domestico", "priority": "alta",    "status": "hecho",     "due": "2026-04-02", "notes": "Hoy."},
    {"id": 26,  "title": "Clonar OBMM-353 y construir propuesta de integración con bancos",              "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": "Tarea de investigación para construir propuesta."},
    {"id": 28,  "title": "Hacer ticket para Fabián — error Quality Water",                              "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 29,  "title": "Investigar cómo usar Claude personal y laboral",                               "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 30,  "title": "Ejecutar script apertura 2027 a toda la base instalada",                       "category": "laboral",   "priority": "critica", "status": "progreso",  "due": "",           "notes": "Tarea monstruosa."},
    {"id": 31,  "title": "Comprar regalo de matrimonio de Felipe",                                       "category": "personal",  "priority": "critica", "status": "hecho",     "due": "2026-04-10", "notes": ""},
    {"id": 32,  "title": "Pagar al Ivo",                                                                 "category": "personal",  "priority": "alta",    "status": "hecho",     "due": "2026-04-08", "notes": ""},
    {"id": 33,  "title": "Pagar tarjetas de crédito",                                                    "category": "personal",  "priority": "alta",    "status": "hecho",     "due": "2026-04-08", "notes": ""},
    {"id": 34,  "title": "Transferir dividendo",                                                         "category": "personal",  "priority": "alta",    "status": "hecho",     "due": "2026-04-08", "notes": ""},
    {"id": 35,  "title": "Girar dinero para comprar en el mercado",                                      "category": "domestico", "priority": "media",   "status": "hecho",     "due": "2026-04-07", "notes": ""},
    {"id": 36,  "title": "Hacer tickets para Plataforma",                                                "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-09", "notes": "1. Crear un proceso de suspensión y activación desde el BackOffice de Don Manager, orientado a suspensiones temporales por motivos de pago.\n2. Incorporar un campo específico para identificar suspensiones por pago.\n3. Implementar controles que eviten que la ejecución de scripts deje clientes en estado suspendido de manera no intencionada."},
    {"id": 37,  "title": "Comunicar bajada de servicio sábado 11 abril",                                 "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-11", "notes": "Sábado 11 a las 9:30 PM, máximo 2 horas. Actualizaciones de seguridad AWS."},
    {"id": 38,  "title": "Coordinar bajada de servicio para el domingo",                                 "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-12", "notes": ""},
    {"id": 39,  "title": "Ticket Plataforma: botón eliminar usuarios Don Manager",                       "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-09", "notes": "El botón de eliminar usuarios no debe hacer borrado físico. Solo debe: auth_user.is_active = false + actualizar updated_at y updated_by."},
    {"id": 40,  "title": "Arreglar registros TBRNK en lagogreybkp",                                      "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": "Corregir registros TBRNK con la deuda correcta. Encontrarlos usando la query global."},
    {"id": 41,  "title": "Asignar num_cliente a documentos TBRNK con NULL",                              "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": "Identificar qué BOVE pagaron los documentos TBRNK sin num_cliente (NULL), y qué num_cliente tiene esa BOVE. Guiarse por la glosa del comp_det."},
    {"id": 42,  "title": "Corregir script inconsistencia global: duplica registros",                     "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": "El script de inconsistencia global está duplicando registros. Identificar causa y resolver."},
    {"id": 43,  "title": "Crear épica de pruebas automatizadas",                                         "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-07", "notes": ""},
    {"id": 44,  "title": "Compartir Excel de pruebas automatizadas en modo lectura",                     "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-07", "notes": ""},
    {"id": 45,  "title": "Crear historias de pruebas automatizadas para el equipo",                      "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-07", "notes": "Repartir historias entre el equipo."},
    {"id": 46,  "title": "Ticket técnico: pruebas automatizadas en pipeline",                            "category": "laboral",   "priority": "alta",    "status": "hecho",     "due": "2026-04-07", "notes": "Incorporar pruebas automatizadas al pipeline de CI/CD."},
    {"id": 47,  "title": "Pagar a Diego el almuerzo",                                                    "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 48,  "title": "Mandar correo a directora por tema fotografías",                              "category": "personal",  "priority": "media",   "status": "progreso",  "due": "",           "notes": ""},
    {"id": 49,  "title": "Mandar mensaje por tema robos a los cursos",                                   "category": "personal",  "priority": "alta",    "status": "hecho",     "due": "",           "notes": ""},
    {"id": 50,  "title": "Revisar Excel de María Elena",                                                 "category": "personal",  "priority": "media",   "status": "pendiente", "due": "2026-04-12", "notes": "Para el fin de semana."},
    {"id": 51,  "title": "Crear PDF plantilla para la mesada",                                           "category": "personal",  "priority": "critica", "status": "progreso",  "due": "",           "notes": "Plantilla para registrar qué cosas les quitan plata, para que los niños sean más conscientes."},
    {"id": 52,  "title": "Poner visita de Mayolen en el calendario",                                     "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 53,  "title": "Carta a maestra Camila prima",                                                 "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": "Pedir que los libros y el metalófono se queden en el colegio por el peso de las mochilas de los niños."},
    {"id": 54,  "title": "Avisar a Giacaman de forros de libros",                                        "category": "personal",  "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 55,  "title": "Comprar sábanas para las niñas",                                               "category": "domestico", "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 56,  "title": "Darle acceso al repo a Eduardo Jofré",                                         "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 57,  "title": "Activar feature flag nuevo ambiente autoimplementación (Don Manager)",         "category": "laboral",   "priority": "media",   "status": "progreso",  "due": "",           "notes": ""},
    {"id": 58,  "title": "Hacer petición de Marmau",                                                     "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 59,  "title": "MMAS-10684",                                                                   "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 60,  "title": "Reserva de alojamiento en Olmué para el fin de semana",                       "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 61,  "title": "Cotizar Galaxikids para cumple de Fer y Gaspar",                               "category": "domestico", "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 62,  "title": "Mandar ficha médica de Josefina a dentista",                                   "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 63,  "title": "Comprar libro adolescencia",                                                   "category": "domestico", "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 64,  "title": "Reembolsar radiografía de mano",                                               "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 65,  "title": "Revisar requerimiento de Rex",                                                 "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-16", "notes": ""},
    {"id": 66,  "title": "Ver idea de sacar el libro mayor como query",                                  "category": "laboral",   "priority": "critica", "status": "pendiente", "due": "2026-04-16", "notes": ""},
    {"id": 67,  "title": "Ver tema Intercom: merge a lead and a user",                                   "category": "laboral",   "priority": "critica", "status": "hoy",       "due": "",           "notes": ""},
    {"id": 68,  "title": "MMAS-10742",                                                                   "category": "laboral",   "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 69,  "title": "Análisis post mortem — incidente actualización de BD en productivo",           "category": "laboral",   "priority": "alta",    "status": "pendiente", "due": "",           "notes": ""},
    {"id": 70,  "title": "Hacer banner nuevo dashboard y ratios financieros",                            "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 71,  "title": "Responder correos de Gily",                                                    "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 72,  "title": "Hacer ticket para los videos de academia",                                     "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 73,  "title": "Cotizar un Dremel",                                                            "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 75,  "title": "Generar reporte para comercial sobre uso de API",                              "category": "laboral",   "priority": "critica", "status": "pendiente", "due": "",           "notes": ""},
    {"id": 76,  "title": "Reembolsar kine de Fer",                                                       "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 77,  "title": "Ver reajustes de rentas",                                                      "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-20", "notes": ""},
    {"id": 78,  "title": "Transferir $6.000 a Vero",                                                     "category": "domestico", "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 79,  "title": "Comentar en chat del equipo el cambio al día martes",                          "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 80,  "title": "Responder a CQuiroz",                                                          "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 81,  "title": "Hacer prueba de matemáticas para Josefina",                                    "category": "personal",  "priority": "critica", "status": "hecho",     "due": "2026-04-20", "notes": ""},
    {"id": 82,  "title": "Reembolsar remedios",                                                          "category": "personal",  "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 83,  "title": "Organizar versión en Jira para entregar mañana",                              "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-22", "notes": ""},
    {"id": 84,  "title": "Hacer ticket de reparación de datos MMAS-10810",                              "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "",           "notes": ""},
    {"id": 85,  "title": "Leer propuesta de integración bancos de Eduardo",                              "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 86,  "title": "Investigar y hacer modal de novedades (informes con IA)",                      "category": "laboral",   "priority": "critica", "status": "pendiente", "due": "",           "notes": ""},
    {"id": 87,  "title": "Modal de novedades: registro de compras",                                      "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 88,  "title": "Crear modal de novedades: facturación y suscripción",                          "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 89,  "title": "Habilitar banner y novedades de dashboard dinámico con ratios",                "category": "laboral",   "priority": "critica", "status": "hecho",     "due": "2026-04-23", "notes": "Hacer después del documento de novedades de Gonzalo."},
    {"id": 90,  "title": "Instalar Docker y ambiente local (pedir ayuda)",                               "category": "laboral",   "priority": "critica", "status": "hoy",       "due": "",           "notes": ""},
    {"id": 91,  "title": "Hablar con Rodrigo",                                                           "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 92,  "title": "Analizar .md de Rodrigo con CPP",                                              "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 93,  "title": "Crear modal de novedades: integración con Ordéname",                          "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 94,  "title": "Construir propuesta de primera encuesta de satisfacción para nuevas funcionalidades", "category": "laboral", "priority": "media", "status": "hoy", "due": "", "notes": ""},
    {"id": 95,  "title": "Propuesta de ida al Rey de las Micheladas",                                    "category": "laboral",   "priority": "media",   "status": "progreso",  "due": "",           "notes": ""},
    {"id": 97,  "title": "Avisar a cliente: campos de transportistas serán obligatorios en versión de octubre", "category": "laboral", "priority": "media", "status": "pendiente", "due": "2026-09-01", "notes": ""},
    {"id": 98,  "title": "Resolver duda: cómo se ejecutarán las pruebas automatizadas",                  "category": "laboral",   "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 99,  "title": "Planificar reunión mensual",                                                   "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "2026-05-05", "notes": "Martes 5 de mayo."},
    {"id": 100, "title": "Habilitar propuesta F29 — disclaimer por uso de impuestos específico",         "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 101, "title": "Pagarle a la Naty",                                                            "category": "domestico", "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 102, "title": "Mandar mail a la maestra",                                                     "category": "personal",  "priority": "critica", "status": "hecho",     "due": "2026-04-23", "notes": "Hoy sin falta."},
    {"id": 103, "title": "Investigar bypass de captcha en Claude",                                       "category": "laboral",   "priority": "critica", "status": "pendiente", "due": "",           "notes": "Se está by-passeando el captcha."},
    {"id": 104, "title": "Coordinar con Eduardo, Consu, Osmar y Mabe para el martes",                    "category": "laboral",   "priority": "media",   "status": "progreso",  "due": "2026-04-28", "notes": ""},
    {"id": 105, "title": "Invitar a Consu a la reunión del martes",                                      "category": "laboral",   "priority": "media",   "status": "progreso",  "due": "2026-04-28", "notes": ""},
    {"id": 106, "title": "Transferir a mamá",                                                            "category": "personal",  "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 107, "title": "Reembolsos TO",                                                                "category": "domestico", "priority": "media",   "status": "progreso",  "due": "",           "notes": ""},
    {"id": 108, "title": "Reembolsos sicóloga",                                                          "category": "domestico", "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 109, "title": "Contactar a ortodoncista",                                                     "category": "domestico", "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 110, "title": "Responder encuesta de Quarta",                                                 "category": "domestico", "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 111, "title": "Responder a Jessi",                                                            "category": "laboral",   "priority": "critica", "status": "hoy",       "due": "",           "notes": ""},
    {"id": 112, "title": "[Acceso API M+][HU-07] Reporte de control uso API vs contrato (MMAS-10414)",   "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 113, "title": "Monitoreo uso Dashboard BI vs contratos, trials y usuarios activos (MMAS-10337)", "category": "laboral", "priority": "media", "status": "pendiente", "due": "", "notes": ""},
    {"id": 114, "title": "Monitoreo de ambientes con base de datos de réplica vs contratos activos (MMAS-10336)", "category": "laboral", "priority": "media", "status": "pendiente", "due": "", "notes": ""},
    {"id": 115, "title": "Responder técnicamente el tema de eliminación de empresa",                     "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 116, "title": "Contactar a ortodoncista para tomar hora",                                     "category": "domestico", "priority": "media",   "status": "pendiente", "due": "2026-04-27", "notes": "Lunes."},
    {"id": 117, "title": "Buscar clientes que usan impuestos específicos",                              "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 118, "title": "Resolver compra de Mac",                                                       "category": "laboral",   "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 119, "title": "Mandar correo a Carmencita sobre reajustes",                                   "category": "laboral",   "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 120, "title": "Mandar mensaje a Nicola por cambio de calefont",                              "category": "domestico", "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 121, "title": "Mandar mensaje a Ensusilla por falla de sábana",                              "category": "domestico", "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 122, "title": "Mandar a bot-manager-customer reporte de documentos en estado C sin comprobante asociado", "category": "laboral", "priority": "media", "status": "hecho", "due": "", "notes": ""},
    {"id": 123, "title": "Reservar Galaxikids para cumpleaños",                                          "category": "domestico", "priority": "critica", "status": "pendiente", "due": "2026-05-15", "notes": ""},
    {"id": 124, "title": "Dar idea directiva de Quarta para reutilizar",                                 "category": "laboral",   "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 125, "title": "Comprar pantalón Maikra",                                                      "category": "personal",  "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 126, "title": "Comprar en Ikea",                                                              "category": "domestico", "priority": "media",   "status": "hecho",     "due": "",           "notes": ""},
    {"id": 127, "title": "Hacer reembolsos de seguro complementario",                                    "category": "personal",  "priority": "media",   "status": "pendiente", "due": "",           "notes": ""},
    {"id": 128, "title": "Ver por qué apareció otro documento en estado C sin comprobante (etp) — para Rodrigo", "category": "laboral", "priority": "media", "status": "hoy", "due": "", "notes": ""},
    {"id": 129, "title": "Analizar propuesta F29 con impuestos específicos (Rolando)",                   "category": "laboral",   "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
    {"id": 130, "title": "Hacer foto con IA para Carmencita",                                            "category": "laboral",   "priority": "media",   "status": "hoy",       "due": "",           "notes": ""},
]


def seed_if_empty():
    if not is_empty():
        return 0
    for task in LEGACY_TASKS:
        insert_with_id(_transform_legacy(task))
    reset_id_sequence()
    return len(LEGACY_TASKS)


if __name__ == "__main__":
    from database import init_db
    init_db()
    n = seed_if_empty()
    if n:
        print(f"Seeded {n} legacy tasks.")
    else:
        print("Database already populated; skipping seed.")
