import io
import os
import shutil
import tempfile
from PIL import Image
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.product.models import Category, ProductType, Product

TEMP_MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class ImageCompressionTest(TestCase):
    def tearDown(self):
        if os.path.exists(TEMP_MEDIA_ROOT):
            shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def create_dummy_image(self, width=2500, height=2500, format='JPEG'):
        buffer = io.BytesIO()
        image = Image.new('RGB', (width, height), color='red')
        image.save(buffer, format=format)
        buffer.seek(0)
        return buffer.getvalue()

    def test_single_compressed_file_saved(self):
        """Verifica que solo se guarde una versión comprimida y ligera de la imagen y no la original pesada."""
        raw_bytes = self.create_dummy_image()
        uploaded_file = SimpleUploadedFile("test_large_image.jpg", raw_bytes, content_type="image/jpeg")

        category = Category.objects.create(
            category_name="Categoría Test",
            category_image=uploaded_file
        )

        self.assertTrue(bool(category.category_image.name))

        saved_file_path = category.category_image.path
        self.assertTrue(os.path.exists(saved_file_path))

        # Verificar que solo exista 1 archivo en la carpeta de categorías
        category_dir = os.path.dirname(saved_file_path)
        files_in_dir = [f for f in os.listdir(category_dir) if os.path.isfile(os.path.join(category_dir, f))]
        self.assertEqual(len(files_in_dir), 1, f"Se esperaba 1 solo archivo pero hay {len(files_in_dir)}: {files_in_dir}")

        # Verificar que el peso guardado sea menor que el original
        saved_size = os.path.getsize(saved_file_path)
        original_size = len(raw_bytes)
        self.assertLess(saved_size, original_size)

        # Verificar que la imagen guardada sea de formato WEBP y dimensiones <= 1920x1920
        with Image.open(saved_file_path) as img:
            self.assertEqual(img.format, 'WEBP')
            self.assertLessEqual(img.width, 1920)
            self.assertLessEqual(img.height, 1920)

    def test_product_compressed_image_saved(self):
        """Verifica que para un Producto sólo se almacene y sirva la imagen comprimida."""
        raw_bytes = self.create_dummy_image()
        uploaded_file = SimpleUploadedFile("product_photo.jpg", raw_bytes, content_type="image/jpeg")

        product_type = ProductType.objects.create(product_type_name="Tipo General")
        product = Product.objects.create(
            product_type=product_type,
            product_name="Producto Test",
            price=100.00,
            product_image=uploaded_file
        )

        saved_file_path = product.product_image.path
        self.assertTrue(os.path.exists(saved_file_path))

        product_dir = os.path.dirname(saved_file_path)
        files_in_dir = [f for f in os.listdir(product_dir) if os.path.isfile(os.path.join(product_dir, f))]
        self.assertEqual(len(files_in_dir), 1)

        saved_size = os.path.getsize(saved_file_path)
        self.assertLess(saved_size, len(raw_bytes))

        with Image.open(saved_file_path) as img:
            self.assertEqual(img.format, 'WEBP')

    def test_update_model_does_not_create_duplicate_files(self):
        """Verifica que actualizar otros campos del modelo no genere duplicados u otros archivos huérfanos."""
        raw_bytes = self.create_dummy_image()
        uploaded_file = SimpleUploadedFile("test_large_image.jpg", raw_bytes, content_type="image/jpeg")

        category = Category.objects.create(
            category_name="Categoría Test Duplicate",
            category_image=uploaded_file
        )

        saved_file_path = category.category_image.path
        category_dir = os.path.dirname(saved_file_path)

        # Actualizar un campo no relacionado con la imagen
        category.category_name = "Categoría Test Actualizada"
        category.save()

        # Debe permanecer exactamente 1 archivo en el directorio
        files_in_dir = [f for f in os.listdir(category_dir) if os.path.isfile(os.path.join(category_dir, f))]
        self.assertEqual(len(files_in_dir), 1)


