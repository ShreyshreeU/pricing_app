from django.db import models
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

class PricingConfigurationManager(models.Manager):
    def save_with_user(self, user, *args, **kwargs):
        instance = self.model(*args, **kwargs)
        instance.created_by = user
        instance.save()
        return instance

class PricingConfiguration(models.Model):
    distance_base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Rs')
    distance_base_price_upto = models.DecimalField(max_digits=10, decimal_places=2, default=3, help_text='Km')
    distance_base_price_after_upto = models.DecimalField(max_digits=10, decimal_places=2, default=90, help_text='Rs')

    distance_additional_price = models.DecimalField(max_digits=6, decimal_places=2, help_text='Rs')
    distance_additional_price_upto = models.DecimalField(max_digits=6, decimal_places=2, default=3, help_text='Km')
    distance_additional_price_after_upto = models.DecimalField(max_digits=6, decimal_places=2, default=28, help_text='Rs')

    time_multiplier_factor = models.DecimalField(max_digits=6, decimal_places=2)
    time_multiplier_factor_upto = models.DecimalField(max_digits=6, decimal_places=2, default=1, help_text='hrs')
    time_multiplier_factor_after_upto = models.DecimalField(max_digits=6, decimal_places=2, default=1.25)

    waiting_charges = models.DecimalField(max_digits=6, decimal_places=2, help_text='Rs')
    waiting_charges_upto = models.DecimalField(max_digits=6, decimal_places=2, default=3, help_text='mins')
    waiting_charges_after_upto = models.DecimalField(max_digits=6, decimal_places=2, default=2, help_text='Rs per min')

    days_of_week = models.CharField(max_length=50, help_text="Comma-separated days (e.g., Mon,Tue)")
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Pricing Config {self.id}"

    objects = PricingConfigurationManager()

    def save(self, *args, **kwargs):
        is_new_instance = not self.pk  # Check if it's a new instance
        super(PricingConfiguration, self).save(*args, **kwargs)

        # Log when a new instance is created
        if is_new_instance:
            logger.info(f"New {self.__class__.__name__} instance created by {self.created_by.username}: {self}")
        else:
            logger.info(f"{self.__class__.__name__} instance updated by {self.created_by.username}: {self}")
    
    # def save(self, *args, **kwargs):
    #     is_new_instance = not self.pk  # Check if it's a new instance
    #     super(PricingConfiguration, self).save(*args, **kwargs)
        
    #     # Log when a new instance is created
    #     if is_new_instance:
    #         logger.info(f"New {self.__class__.__name__} instance created: {self}")
    #     else:
    #         logger.info(f"{self.__class__.__name__} instance updated: {self}")

    def delete(self, *args, **kwargs):
        # Log when an instance is deleted
        logger.info(f"{self.__class__.__name__} instance deleted: {self}")
        super(PricingConfiguration, self).delete(*args, **kwargs)

    def log_configuration_change(self, user):
        logger.info(f"{self.__class__.__name__} configuration {self.id} updated by {user.username}")

