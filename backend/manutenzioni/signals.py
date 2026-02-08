"""
Django signals for automatic cleanup of media files.

Handles:
- Delete file when record is deleted (post_delete)
- Delete old file when replaced (pre_save)
- Safety check: don't delete if other records use the same file

Uses Django Storage API for proper abstraction and race condition handling.
"""
import logging
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db.models import Q
from django.core.files.storage import default_storage
from .models import Attrezzatura, Taratura

logger = logging.getLogger(__name__)


def is_file_used_by_others(model, instance_id, field_name, file_name):
    """
    Check if the given file name is used by other records of the same model.

    Args:
        model: Django model class
        instance_id: ID of the current instance (to exclude from check)
        field_name: Name of the file field (e.g., 'image', 'documento')
        file_name: File name (string) to check

    Returns:
        True if other records use this file, False otherwise
    """
    if not file_name:
        return False

    # Query for other records using the same file name
    query = Q(**{field_name: file_name})
    if instance_id:
        query &= ~Q(id=instance_id)

    return model.objects.filter(query).exists()


def delete_file_safe(file_field):
    """
    Safely delete a file from storage using Django Storage API.

    Args:
        file_field: Django FileField or ImageField instance

    Returns:
        True if deleted successfully, False otherwise
    """
    if not file_field:
        return False

    file_name = file_field.name
    if not file_name:
        return False

    try:
        # Use the file field's storage (may be custom storage backend)
        storage = file_field.storage

        # Check if file exists before attempting delete
        if storage.exists(file_name):
            storage.delete(file_name)
            logger.info(f"Deleted file: {file_name}")
            return True
        else:
            # File already deleted or never existed - not an error
            logger.debug(f"File not found (already deleted or never existed): {file_name}")
            return False
    except FileNotFoundError:
        # Race condition: file deleted between exists() and delete()
        logger.debug(f"File not found during deletion (race condition): {file_name}")
        return False
    except PermissionError as e:
        # Insufficient permissions to delete file
        logger.error(f"Permission denied deleting file {file_name}: {e}")
        return False
    except Exception as e:
        # Unexpected error
        logger.error(f"Unexpected error deleting file {file_name}: {e}", exc_info=True)
        return False


# =============================================================================
# ATTREZZATURA - image cleanup
# =============================================================================

@receiver(post_delete, sender=Attrezzatura)
def attrezzatura_delete_image(sender, instance, **kwargs):
    """
    Delete image file when Attrezzatura record is deleted.
    Only deletes if no other Attrezzatura uses the same file.
    """
    if not instance.image:
        return

    file_name = instance.image.name

    # Check if other records use this file
    if is_file_used_by_others(Attrezzatura, None, 'image', file_name):
        logger.info(
            f"Skipping deletion of {file_name} - still used by other Attrezzatura records"
        )
        return

    # Safe to delete
    delete_file_safe(instance.image)


@receiver(pre_save, sender=Attrezzatura)
def attrezzatura_update_image(sender, instance, **kwargs):
    """
    Delete old image file when a new one is uploaded (update).
    Only deletes if no other Attrezzatura uses the same file.
    """
    if not instance.pk:
        # New record, no old file to delete
        return

    try:
        old_instance = Attrezzatura.objects.get(pk=instance.pk)
    except Attrezzatura.DoesNotExist:
        # Record doesn't exist yet (shouldn't happen in pre_save)
        logger.warning(
            f"Attrezzatura pk={instance.pk} not found in pre_save (possible race condition)"
        )
        return

    # Get old and new file names (string comparison)
    old_file_name = old_instance.image.name if old_instance.image else None
    new_file_name = instance.image.name if instance.image else None

    # Check if image field has changed
    if old_file_name and old_file_name != new_file_name:
        # File is being replaced or cleared

        # Check if other records use this file
        if is_file_used_by_others(Attrezzatura, instance.pk, 'image', old_file_name):
            logger.info(
                f"Skipping deletion of {old_file_name} - still used by other Attrezzatura records"
            )
            return

        # Safe to delete old file
        delete_file_safe(old_instance.image)


# =============================================================================
# TARATURA - documento cleanup
# =============================================================================

@receiver(post_delete, sender=Taratura)
def taratura_delete_documento(sender, instance, **kwargs):
    """
    Delete documento file when Taratura record is deleted.
    Only deletes if no other Taratura uses the same file.
    """
    if not instance.documento:
        return

    file_name = instance.documento.name

    # Check if other records use this file
    if is_file_used_by_others(Taratura, None, 'documento', file_name):
        logger.info(
            f"Skipping deletion of {file_name} - still used by other Taratura records"
        )
        return

    # Safe to delete
    delete_file_safe(instance.documento)


@receiver(pre_save, sender=Taratura)
def taratura_update_documento(sender, instance, **kwargs):
    """
    Delete old documento file when a new one is uploaded (update).
    Only deletes if no other Taratura uses the same file.
    """
    if not instance.pk:
        # New record, no old file to delete
        return

    try:
        old_instance = Taratura.objects.get(pk=instance.pk)
    except Taratura.DoesNotExist:
        # Record doesn't exist yet (shouldn't happen in pre_save)
        logger.warning(
            f"Taratura pk={instance.pk} not found in pre_save (possible race condition)"
        )
        return

    # Get old and new file names (string comparison)
    old_file_name = old_instance.documento.name if old_instance.documento else None
    new_file_name = instance.documento.name if instance.documento else None

    # Check if documento field has changed
    if old_file_name and old_file_name != new_file_name:
        # File is being replaced or cleared

        # Check if other records use this file
        if is_file_used_by_others(Taratura, instance.pk, 'documento', old_file_name):
            logger.info(
                f"Skipping deletion of {old_file_name} - still used by other Taratura records"
            )
            return

        # Safe to delete old file
        delete_file_safe(old_instance.documento)
