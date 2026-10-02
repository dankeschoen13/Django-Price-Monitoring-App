from django.db import models

class Product(models.Model):
    """
    The master product being tracked.
    """
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductLink(models.Model):
    """
    Connects a master Product to a specific competitor website's listing.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="links")
    website_name = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    price_css_selector = models.CharField(max_length=255, blank=True)
    stock_css_selector = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.product.name} on {self.website_name}"


class PriceHistory(models.Model):
    """
    Stores every individual price check recorded over time.
    """
    product_link = models.ForeignKey(ProductLink, on_delete=models.CASCADE, related_name="price_history")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_in_stock = models.BooleanField(default=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-checked_at']

    def __str__(self):
        return f"{self.product_link} - ${self.price} at {self.checked_at}"