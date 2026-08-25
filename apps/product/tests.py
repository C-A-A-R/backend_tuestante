from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from apps.product.models import Product, ProductType, ProductAngleImage, ProductColorImage
from apps.product.admin import ProductAngleImageInline, ProductColorImageInline
from apps.product.api.serializers import ProductSerializer


class ProductInlineSoftDeleteTest(TestCase):
    def setUp(self):
        self.product_type = ProductType.objects.create(product_type_name="Tipo Test")
        self.product = Product.objects.create(
            product_type=self.product_type,
            product_name="Producto Test",
            price=100.00
        )
        self.angle1 = ProductAngleImage.objects.create(product=self.product, angle="Izquierdo")
        self.angle2 = ProductAngleImage.objects.create(product=self.product, angle="Frente")
        self.color1 = ProductColorImage.objects.create(product=self.product, color_name="Rojo", color_hex="#FF0000")

    def test_inline_get_queryset_excludes_soft_deleted(self):
        """Verifica que el inline de Django Admin excluya los ángulos borrados lógicamente."""
        from django.test import RequestFactory
        from django.contrib.auth.models import User

        factory = RequestFactory()
        request = factory.get('/admin/')
        request.user = User(is_superuser=True, is_staff=True)

        admin_site = AdminSite()
        inline = ProductAngleImageInline(ProductAngleImage, admin_site)

        # 1. Eliminar lógicamente angle2
        self.angle2.delete()
        self.assertTrue(ProductAngleImage.objects.get(id=self.angle2.id).is_deleted)

        # 2. Consultar el queryset del Inline
        queryset = inline.get_queryset(request)
        angles_in_queryset = list(queryset.filter(product=self.product))

        # 3. Solo debe estar angle1
        self.assertEqual(len(angles_in_queryset), 1)
        self.assertEqual(angles_in_queryset[0].id, self.angle1.id)

    def test_serializer_excludes_soft_deleted_angles_and_colors(self):
        """Verifica que el serializador de la API excluya ángulos y colores borrados lógicamente."""
        self.angle2.delete()
        self.color1.delete()

        serializer = ProductSerializer(self.product)
        data = serializer.data

        angle_ids = [a['id'] for a in data['angle_images']]
        color_ids = [c['id'] for c in data['color_images']]

        self.assertIn(self.angle1.id, angle_ids)
        self.assertNotIn(self.angle2.id, angle_ids)
        self.assertNotIn(self.color1.id, color_ids)

