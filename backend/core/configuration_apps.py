def get_app_icons(nome_app=None):
    app_icons = {
        'chem_man': 'bi bi-moisture',
        'manutenzioni': 'bi bi-house-check',
        'tarature': 'bi bi-house-check',
        'autorizzazioni': 'bi bi-file-check',
        'risorse umane': 'bi bi-person-workspace',
        # Aggiungi altre app e icone come necessario
    }
    if nome_app:
        return app_icons.get(nome_app)
    return app_icons