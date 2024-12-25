from django.db import models


class Item(models.Model):
    name = models.CharField('название детали', max_length=250)
    diameter = models.FloatField('диаметр')
    weight = models.FloatField('масса изделия, кг')
    accuracy_class = models.CharField('класс точности', max_length=250)
    cost = models.FloatField('стоимость, руб')
    strength_class = models.FloatField('класс прочности')


class Bolt(Item):
    length = models.FloatField('номинальная длина, мм')
    size = models.FloatField('размер под ключ, мм')

    class Meta:
        verbose_name = 'болт'
        verbose_name_plural = 'болты'

    def __str__(self):
        return f'{self.name}{self.diameter}x{self.length}'


class Nut(Item):
    size = models.FloatField('размер под ключ, мм')

    class Meta:
        verbose_name = 'гайка'
        verbose_name_plural = 'гайки'

    def __str__(self):
        return f'{self.name} {self.diameter}'


class Washer(Item):

    class Meta:
        verbose_name = 'шайба'
        verbose_name_plural = 'шайбы'

    def __str__(self):
        return f'{self.name} {self.diameter}'


class BoltJoint(models.Model):
    bolt = models.ForeignKey(
        Bolt,
        on_delete=models.DO_NOTHING,
        verbose_name='болт',
        related_name='boltjoint_bolt',
        null=True,
    )
    bolt_washer = models.ForeignKey(
        Washer,
        on_delete=models.DO_NOTHING,
        verbose_name='шайба со стороны болта',
        related_name='boltjoint_bolt_washer',
        null=True,
    )
    material = models.CharField('соединяемый материал', max_length=250)
    nut_washer = models.ForeignKey(
        Washer,
        on_delete=models.DO_NOTHING,
        verbose_name='шайба со стороны гайки',
        related_name='boltjoint_nut_washer',
        null=True,
    )
    nut = models.ForeignKey(
        Nut,
        on_delete=models.DO_NOTHING,
        verbose_name='гайка',
        related_name='boltjoint_nut',
        null=True,
    )
    locknut = models.ForeignKey(
        Nut,
        on_delete=models.DO_NOTHING,
        verbose_name='контргайка',
        related_name='boltjoint_locknut',
        null=True,
    )
    weight = models.FloatField('масса, кг', editable=False)
    cost = models.FloatField('стоимость, руб', editable=False)

    class Meta:
        verbose_name = 'болтовое соединение'
        verbose_name_plural = 'болтовые соединения'

    def __str__(self):
        return f'{self.bolt} {self.nut}'
    
    def save(self):
        self.weight = self.bolt.weight + self.bolt_washer.weight + self.nut_washer.weight + self.nut.weight + self.locknut.weight
        self.cost = self.bolt.cost + self.bolt_washer.cost + self.nut_washer.cost + self.nut.cost + self.locknut.cost
        return super(BoltJoint, self).save()


class Order(models.Model):
    customer = models.CharField('заказчик', max_length=250)
    created_at = models.DateTimeField('дата и время создания заказа', auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    order_items = models.ManyToManyField(
        BoltJoint,
        related_name='order_boltjoint',
        verbose_name='состав заказа',
    )
    cost = models.FloatField('Стоимость, руб', editable=False, default=0)
    weight = models.FloatField('масса заказа, кг', editable=False, default=0)

    objects = models.Manager()

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ номер {self.pk} от {self.created_at}. Заказчик: {self.customer}.'
    
    def save(self):
        super(Order, self).save()
        items = self.order_items.all()
        if items:
            weight = 0
            cost = 0
            for item in items:
                weight += item.weight
                cost += item.weight
            if weight != self.weight:
                self.weight = weight
            if cost != self.cost:
                self.cost = cost
            return super(Order, self).save()
