#!/usr/bin/env python
"""
Script di verifica post-migrazione SaaS Multi-Tenant

Esegui questo script dopo il deploy per verificare che la migrazione
sia andata a buon fine.

Uso:
    docker exec qms-backend python verify_saas_migration.py
    # oppure
    python manage.py shell < verify_saas_migration.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qmsproject.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import Company, Profile
from anagrafiche.models import Cliente, Fornitore
from django.db.models import Count


def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def check_companies():
    print_header("1. VERIFICA COMPANIES")

    companies = Company.objects.all()
    print(f"✓ Totale Companies: {companies.count()}")

    if companies.count() == 0:
        print("❌ ERRORE: Nessuna Company trovata!")
        return False

    for company in companies:
        print(f"\n  📊 Company: {company.name}")
        print(f"     - Slug: {company.slug}")
        print(f"     - Attiva: {'✓' if company.is_active else '✗'}")
        print(f"     - Piano: {company.subscription_plan}")
        print(f"     - Paese: {company.country}")

    return True


def check_profiles():
    print_header("2. VERIFICA PROFILI UTENTI")

    total_profiles = Profile.objects.count()
    profiles_with_company = Profile.objects.filter(company__isnull=False).count()
    profiles_without_company = Profile.objects.filter(company__isnull=True).count()

    print(f"✓ Totale Profili: {total_profiles}")
    print(f"✓ Profili con Company: {profiles_with_company}")

    if profiles_without_company > 0:
        print(f"❌ ATTENZIONE: {profiles_without_company} profili senza Company!")
        users_without_company = Profile.objects.filter(company__isnull=True)
        for profile in users_without_company:
            print(f"   - {profile.user.username} (ID: {profile.user.id})")
        return False

    # Raggruppa per ruolo
    roles = Profile.objects.values('role').annotate(count=Count('id'))
    print("\n  Distribuzione ruoli:")
    for role in roles:
        print(f"     - {role['role']}: {role['count']}")

    # Raggruppa per company
    companies = Profile.objects.values('company__name').annotate(count=Count('id'))
    print("\n  Distribuzione per Company:")
    for company in companies:
        print(f"     - {company['company__name']}: {company['count']} utenti")

    return True


def check_clienti():
    print_header("3. VERIFICA CLIENTI")

    total_clienti = Cliente.objects.count()
    clienti_with_company = Cliente.objects.filter(company__isnull=False).count()
    clienti_without_company = Cliente.objects.filter(company__isnull=True).count()

    print(f"✓ Totale Clienti: {total_clienti}")
    print(f"✓ Clienti con Company: {clienti_with_company}")

    if clienti_without_company > 0:
        print(f"❌ ERRORE: {clienti_without_company} clienti senza Company!")
        return False

    # Raggruppa per company
    if total_clienti > 0:
        companies = Cliente.objects.values('company__name').annotate(count=Count('id'))
        print("\n  Distribuzione per Company:")
        for company in companies:
            print(f"     - {company['company__name']}: {company['count']} clienti")

    return True


def check_fornitori():
    print_header("4. VERIFICA FORNITORI")

    total_fornitori = Fornitore.objects.count()
    fornitori_with_company = Fornitore.objects.filter(company__isnull=False).count()
    fornitori_without_company = Fornitore.objects.filter(company__isnull=True).count()

    print(f"✓ Totale Fornitori: {total_fornitori}")
    print(f"✓ Fornitori con Company: {fornitori_with_company}")

    if fornitori_without_company > 0:
        print(f"❌ ERRORE: {fornitori_without_company} fornitori senza Company!")
        return False

    # Raggruppa per company
    if total_fornitori > 0:
        companies = Fornitore.objects.values('company__name').annotate(count=Count('id'))
        print("\n  Distribuzione per Company:")
        for company in companies:
            print(f"     - {company['company__name']}: {company['count']} fornitori")

    return True


def check_middleware():
    print_header("5. VERIFICA CONFIGURAZIONE MIDDLEWARE")

    from django.conf import settings

    if 'core.middleware.CompanyMiddleware' in settings.MIDDLEWARE:
        print("✓ CompanyMiddleware configurato correttamente")
        return True
    else:
        print("❌ ERRORE: CompanyMiddleware non trovato in MIDDLEWARE!")
        print("   Aggiungi 'core.middleware.CompanyMiddleware' a MIDDLEWARE in settings.py")
        return False


def check_admin_registered():
    print_header("6. VERIFICA REGISTRAZIONE ADMIN")

    from django.contrib import admin
    from accounts.models import Company, Profile

    if Company in admin.site._registry:
        print("✓ Company registrato in Django Admin")
    else:
        print("⚠️  WARNING: Company non registrato in Django Admin")

    if Profile in admin.site._registry:
        print("✓ Profile registrato in Django Admin")
    else:
        print("⚠️  WARNING: Profile non registrato in Django Admin")

    return True


def main():
    print("\n" + "🔍" * 35)
    print("   VERIFICA MIGRAZIONE SAAS MULTI-TENANT")
    print("🔍" * 35)

    checks = [
        ("Companies", check_companies),
        ("Profili Utenti", check_profiles),
        ("Clienti", check_clienti),
        ("Fornitori", check_fornitori),
        ("Middleware", check_middleware),
        ("Admin", check_admin_registered),
    ]

    results = []

    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERRORE durante verifica {name}: {str(e)}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Riepilogo finale
    print_header("RIEPILOGO VERIFICA")

    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  - {name}")
        if not result:
            all_passed = False

    print("\n" + "=" * 70)

    if all_passed:
        print("\n🎉 SUCCESSO! La migrazione SaaS è stata completata correttamente!")
        print("\n📝 Prossimi step:")
        print("   1. Testa il login con un utente esistente")
        print("   2. Verifica che i dati siano visibili correttamente")
        print("   3. Prova a creare un nuovo cliente/fornitore")
        print("   4. Accedi al Django Admin per gestire le Companies")
        return 0
    else:
        print("\n⚠️  ATTENZIONE! Alcuni controlli sono falliti.")
        print("   Rivedi gli errori sopra e correggi prima di procedere.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
