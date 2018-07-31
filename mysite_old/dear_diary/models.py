from django.db import models

# Create your models here.

class Entry(models.Model):

	text = models.TextField()
	pub_date = models.DateTimeField(auto_now_add=True)
	is_readed = models.BooleanField(default=False)

	def __str__(self):
		return "Entries # {}".format(self.id)

	class Meta:
		verbose_name_plural = 'entries'


class EntrySummarry(Entry):
    class Meta:
        proxy = True
        verbose_name = 'Entry Summary'
        verbose_name_plural = 'Entries Summary'