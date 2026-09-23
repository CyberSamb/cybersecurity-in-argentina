"""
etiquetas.py
Traduce los nombres técnicos de la columna 'metrica' a texto legible para
mostrar en gráficos. Centralizado acá para que todos los paneles usen la
misma redacción y no haya que tocar 3 archivos si se corrige una etiqueta.
"""

ETIQUETAS = {
    # Personal
    "reportes_delitos_informaticos": "Reportes de delitos informáticos (UFECI)",
    "pct_usuarios_victimas_hackeo_fraude": "Se declara víctima de hackeo o fraude",
    "pct_usuarios_usa_gestor_password": "Usa gestor de contraseñas",
    "pct_usuarios_password_debil": "Usa contraseña débil",
    "pct_usuarios_reutiliza_password": "Reutiliza la misma contraseña",
    "pct_usuarios_no_cambia_password_frecuencia": "No cambia sus contraseñas con frecuencia",
    "pct_usuarios_solo_3_passwords": "Usa solo 3 contraseñas o menos para todo",
    "pct_accesos_ilegitimos_whatsapp": "Accesos ilegítimos vía WhatsApp",
    "pct_accesos_ilegitimos_mercadopago": "Accesos ilegítimos vía Mercado Pago",
    "accesos_ilegitimos_total": "Accesos ilegítimos (total de casos)",
    "pct_fraude_en_linea": "Casos que son fraude en línea",

    # Organizacional
    "pct_orgs_complejidad_operativa_riesgo_preocupante": "Preocupa la complejidad operativa como riesgo",
    "pct_orgs_espera_aumento_ciberataques": "Espera un aumento de ciberataques",
    "pct_orgs_evaluacion_formal_riesgo_terceros": "Tiene evaluación formal de riesgo de terceros",
    "pct_orgs_procesos_formales_seguridad_datos": "Tiene procesos formales de seguridad de datos",
    "pct_orgs_espera_aumento_ataques_nube": "Espera un aumento de ataques a la nube",
    "pct_orgs_prioriza_mitigacion_riesgo_cibernetico": "Prioriza mitigar el riesgo cibernético",
    "pct_orgs_despliega_computacion_cuantica_ciberdefensa": "Despliega computación cuántica en ciberdefensa",
    "pct_orgs_prioriza_mitigacion_riesgo_digital_tecnologico": "Prioriza mitigar el riesgo digital/tecnológico",
    "pct_orgs_anticipa_riesgos_macro_tecnologia_estrategia": "Anticipa riesgos macro/tecnológicos en su estrategia",
    "pct_orgs_asigna_presupuesto_principales_riesgos": "Asigna presupuesto a los principales riesgos",
    "pct_orgs_visibilidad_ot_implementada": "Tiene visibilidad de tecnología operativa (OT)",
    "pct_orgs_asigna_dependencias_tecnologicas_mapeadas": "Tiene dependencias tecnológicas mapeadas",
    "pct_orgs_informa_directorio_riesgos_regulacion": "Informa al directorio sobre riesgos y regulación",
    "pct_orgs_colabora_otras_areas_empresa": "Colabora con otras áreas de la empresa",
    "pct_orgs_controles_respuesta_rapida_resiliencia": "Tiene controles de respuesta rápida",
    "pct_orgs_invierte_proactivo": "Invierte significativamente más en medidas proactivas",
    "pct_orgs_no_preparadas_computacion_cuantica": "No está preparada para computación cuántica",
    "pct_orgs_aumenta_inversion_riesgos_geopolitico": "Aumenta inversión en riesgos por contexto geopolítico",
    "pct_orgs_cambia_ubicacion_infraestructura_critica": "Cambia la ubicación de infraestructura crítica",
    "pct_orgs_cambia_politicas_comerciales_operativas": "Cambia políticas comerciales y operativas",
    "pct_orgs_cambia_polizas_seguro_ciber": "Cambia pólizas de seguro cibernético",
    "pct_orgs_cambia_lugar_actividad_comercial": "Cambia el lugar de su actividad comercial",
    "pct_orgs_cambia_proveedores": "Cambia de proveedores",

    # Gubernamental
    "incidentes_totales_estado": "Incidentes totales reportados al Estado",
    "incidentes_criticos_sector_estado": "Incidentes críticos en el sector Estado",
    "incidentes_sector_finanzas": "Incidentes en el sector Finanzas",
    "incidentes_sector_estado_gob": "Incidentes en organismos de gobierno",
    "pct_incidentes_phishing": "Incidentes de tipo phishing",
    "incidentes_severidad_alta": "Incidentes de severidad alta",
    "incidentes_severidad_critica": "Incidentes de severidad crítica",
    "incidentes_severidad_media": "Incidentes de severidad media",
    "incidentes_severidad_baja": "Incidentes de severidad baja",

    # Gubernamental: tipo de incidente
    "incidentes_tipo_fraude": "Fraude",
    "incidentes_tipo_compromiso_informacion": "Compromiso de la información",
    "incidentes_tipo_contenido_abusivo": "Contenido abusivo",
    "incidentes_tipo_intrusion": "Intrusión",
    "incidentes_tipo_contenido_danino": "Contenido dañino",
    "incidentes_tipo_disponibilidad": "Disponibilidad",
    "incidentes_tipo_vulnerable": "Sistema vulnerable",
    "incidentes_tipo_obtencion_informacion": "Obtención de información",
    "incidentes_tipo_otros": "Otros",

    "incidentes_tipo_phishing": "Phishing",
    "incidentes_tipo_compromiso_cuenta": "Compromiso de cuenta (robo de credenciales)",
    "incidentes_tipo_modificacion_no_autorizada": "Modificación no autorizada de información",
    "incidentes_tipo_acceso_no_autorizado": "Acceso no autorizado a la información",
}


def etiqueta_legible(metrica: str) -> str:
    """Devuelve el texto legible de una métrica; si no está mapeada, devuelve el nombre técnico tal cual."""
    return ETIQUETAS.get(metrica, metrica)