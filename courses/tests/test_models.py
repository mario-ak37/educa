from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from courses.models import Content, Course, Module, Subject, Text


class ModuleOrderFieldTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="mario", password="testpass")
        self.subject = Subject.objects.create(title="Programming", slug="programming")
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Python",
            slug="python",
            overview="Learn Python",
        )

    def test_first_module_order_is_zero(self):
        module = Module.objects.create(course=self.course, title="Intro")
        self.assertEqual(module.order, 0)

    def test_second_module_order_increments(self):
        Module.objects.create(course=self.course, title="Intro")
        module = Module.objects.create(course=self.course, title="Basics")
        self.assertEqual(module.order, 1)

    def test_modules_order_is_per_course(self):
        other_course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Django",
            slug="django",
            overview="Learn Django",
        )

        m1 = Module.objects.create(course=self.course, title="Intro")
        m2 = Module.objects.create(course=other_course, title="Intro")

        self.assertEqual(m1.order, 0)
        self.assertEqual(m2.order, 0)

    def test_explicit_order_is_respected(self):
        module = Module.objects.create(
            course=self.course,
            title="Manual",
            order=10,
        )
        self.assertEqual(module.order, 10)


class ModuleStringRepresentationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("mario")
        self.subject = Subject.objects.create(title="Programming", slug="programming")
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Python",
            slug="python",
            overview="Overview",
        )

    def test_module_str_includes_order_and_title(self):
        module = Module.objects.create(course=self.course, title="Intro")
        self.assertEqual(str(module), "0. Intro")


class ContentGenericForeignKeyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("mario")
        self.subject = Subject.objects.create(title="Programming", slug="programming")
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Python",
            slug="python",
            overview="Overview",
        )
        self.module = Module.objects.create(course=self.course, title="Intro")

    def test_content_resolves_text_item(self):
        text = Text.objects.create(
            owner=self.user,
            title="Lesson text",
            content="Hello world",
        )

        content_type = ContentType.objects.get_for_model(Text)

        content = Content.objects.create(
            module=self.module,
            content_type=content_type,
            object_id=text.id,
        )

        self.assertEqual(content.item, text)


class ContentOrderFieldTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("mario")
        self.subject = Subject.objects.create(title="Programming", slug="programming")
        self.course = Course.objects.create(
            owner=self.user,
            subject=self.subject,
            title="Python",
            slug="python",
            overview="Overview",
        )
        self.module = Module.objects.create(course=self.course, title="Intro")

        self.text1 = Text.objects.create(
            owner=self.user,
            title="Text 1",
            content="A",
        )
        self.text2 = Text.objects.create(
            owner=self.user,
            title="Text 2",
            content="B",
        )

        self.ct = ContentType.objects.get_for_model(Text)

    def test_first_content_order_is_zero(self):
        content = Content.objects.create(
            module=self.module,
            content_type=self.ct,
            object_id=self.text1.id,
        )
        self.assertEqual(content.order, 0)

    def test_content_order_increments(self):
        Content.objects.create(
            module=self.module,
            content_type=self.ct,
            object_id=self.text1.id,
        )
        content = Content.objects.create(
            module=self.module,
            content_type=self.ct,
            object_id=self.text2.id,
        )
        self.assertEqual(content.order, 1)


class CourseModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("mario")
        cls.subject = Subject.objects.create(title="Programming", slug="programming")
        cls.course = Course.objects.create(
            owner=cls.user,
            subject=cls.subject,
            title="Python",
            slug="python",
            overview="Overview",
        )

    def test_str_returns_title(self):
        self.assertEqual(str(self.course), "Python")


class ModuleModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("mario")
        cls.subject = Subject.objects.create(title="Programming", slug="programming")
        cls.course = Course.objects.create(
            owner=cls.user,
            subject=cls.subject,
            title="Python",
            slug="python",
            overview="Overview",
        )
        cls.module = Module.objects.create(course=cls.course, title="Intro", order=0)

    def test_str_returns_order_and_title(self):
        self.assertEqual(str(self.module), "0. Intro")
