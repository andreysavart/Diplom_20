from tortoise import fields
from tortoise.models import Model


class Order(Model):
    order_id = fields.IntField(pk=True, index=True)
    customer = fields.CharField(max_length=250)
    created_at = fields.DatetimeField(auto_now_add=True)
    edited_at = fields.DatetimeField(auto_now=True)
    order_items = fields.ManyToManyField(
        'models.BoltJoint',
        related_name='order_boltjoints',
        on_delete=fields.NO_ACTION,
    )
    weight = fields.FloatField()
    cost = fields.FloatField()

    class Meta:
        table = 'orders'
    
    def __str__(self):
        return f'Заказ для {self.customer} от {self.created_at}'
