from tortoise import fields
from tortoise.models import Model


class BoltJoint(Model):
    bolt_joint_id = fields.IntField(pk=True, index=True)
    material= fields.CharField(max_length=250)
    bolt = fields.ForeignKeyField(
        'models.Bolt', # путь относительно файла main.py
        related_name='boltjoint_bolt',
        on_delete=fields.NO_ACTION,
    )
    nut = fields.ForeignKeyField(
        'models.Nut',
        related_name='boltjoint_nut',
        on_delete=fields.NO_ACTION,
    )
    locknut = fields.ForeignKeyField(
        'models.Nut',
        related_name='boltjoint_locknut',
        on_delete=fields.NO_ACTION,
    )
    bolt_washer = fields.ForeignKeyField(
        'models.Washer',
        related_name='boltjoint_bolt_washer',
        on_delete=fields.NO_ACTION,
    )
    nut_washer = fields.ForeignKeyField(
        'models.Washer',
        related_name='boltjoint_nut_washer',
        on_delete=fields.NO_ACTION,
    )
    weight = fields.FloatField()
    cost = fields.FloatField()

    class Meta:
        table = 'bolt_joints'
    
    def __str__(self):
        return f'{self.bolt} {self.nut} {self.locknut}'
