# import factory
# from faker import Faker
# from django.contrib.auth.models import User
# from store.models import Vendor, Artwork, VendorProfile, VendorSale, Payment, Tender

# fake = Faker()

# class UserFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = User

#     username = factory.Sequence(lambda n: f'user{n}')
#     email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
#     password = factory.PostGenerationMethodCall('set_password', 'password')

# class VendorFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Vendor

#     user = factory.SubFactory(UserFactory)


# class VendorProfileFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = VendorProfile

#     vendor = factory.SubFactory(VendorFactory)
#     name = factory.LazyAttribute(lambda _: fake.name())
#     age = factory.LazyAttribute(lambda _: fake.random_int(min=18, max=65))
#     city = factory.LazyAttribute(lambda _: fake.city())
#     working_or_studying = factory.LazyAttribute(lambda _: fake.random_element(elements=('Working', 'Studying')))

# class ArtworkFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Artwork

#     vendor_profile = factory.SubFactory(VendorProfileFactory)
#     theme = factory.LazyAttribute(lambda _: fake.word())
#     price = factory.LazyAttribute(lambda _: fake.random_int(min=100, max=1000))
#     medium = factory.LazyAttribute(lambda _: fake.random_element(elements=('Oil', 'Acrylic', 'Watercolor')))
#     image = factory.django.ImageField()

# class VendorSaleFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = VendorSale

#     vendor = factory.SubFactory(VendorFactory)
#     artwork = factory.SubFactory(ArtworkFactory)
#     quantity = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=10))

# class PaymentFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Payment

#     vendor = factory.SubFactory(VendorFactory)
#     amount = factory.LazyAttribute(lambda _: fake.random_int(min=100, max=1000))

# class TenderFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = Tender

#     title = factory.LazyAttribute(lambda _: fake.sentence(nb_words=3))
#     description = factory.LazyAttribute(lambda _: fake.paragraph())
