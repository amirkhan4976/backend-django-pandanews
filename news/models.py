from django.db import models
import uuid


class Source(models.Model):
    source_id = models.CharField(max_length=256, null=True, blank=True)
    name = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class AbstractNews(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    author = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    urlToImage = models.TextField(null=True, blank=True)
    publishedAt = models.DateTimeField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        abstract = True
        ordering = ["-publishedAt"]


class Science(AbstractNews):

    class Meta:
        verbose_name = "Science"
        verbose_name_plural = "Sciences"


class General(AbstractNews):

    class Meta:
        verbose_name = "General"
        verbose_name_plural = "Generals"


class Business(AbstractNews):

    class Meta:
        verbose_name = "Business"
        verbose_name_plural = "Business"


class Entertainment(AbstractNews):

    class Meta:
        verbose_name = "Entertainment"
        verbose_name_plural = "Entertainments"


class Health(AbstractNews):

    class Meta:
        verbose_name = "Health"
        verbose_name_plural = "Healths"


class Sports(AbstractNews):

    class Meta:
        verbose_name = "Sports"
        verbose_name_plural = "Sports"


class Technology(AbstractNews):

    class Meta:
        verbose_name = "Technology"
        verbose_name_plural = "Technologies"


class Crypto(AbstractNews):

    class Meta:
        verbose_name = "Crypto"
        verbose_name_plural = "Cryptos"


class StudentLoan(AbstractNews):

    class Meta:
        verbose_name = "StudentLoan"
        verbose_name_plural = "StudentLoans"


class Loan(AbstractNews):

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"


class HackersHacking(AbstractNews):

    class Meta:
        verbose_name = "HackersHacking"
        verbose_name_plural = "HackersHacking"


class AnonymousHacking(AbstractNews):

    class Meta:
        verbose_name = "AnonymousHacking"
        verbose_name_plural = "AnonymousHacking"
