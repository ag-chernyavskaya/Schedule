# from django.test import TestCase
# from Teacher.models import Teacher
# from User.models import User
# from course.models import Course
#
#
# class CourseModelTests(TestCase):
#
#     @classmethod
#     def setUpTestData(cls):
#         teacher = Teacher.objects.create(name="A", surname="B", age="23", start_date='2022-08-01', group_count='1',
#                                          course_name="Python Basic level", description="ku-ku",)
#         user = User.objects.create(email="sobaka@gmail.com", role='SuperAdmin', first_name="C", last_name='D',
#                                    date_joined='2022-08-01', is_staff=True, is_active=True,)
#         Course.objects.create(course_name='Python Basic level', teacher=teacher, user=user, start_day='2022-08-16')
#
#     def test_course_name_label(self):
#         course = Course.objects.get(id=1)
#         field_label = course._meta.get_field('course_name').verbose_name
#         self.assertEquals(field_label, 'course_name')
#
#     def test_start_day_label(self):
#         course = Course.objects.get(id=1)
#         field_label = course._meta.get_field('start_day').verbose_name
#         self.assertEquals(field_label, 'start_day')
#
#     def test_course_name_max_length(self):
#         course = Course.objects.get(id=1)
#         max_length = course._meta.get_field('course_name').max_length
#         self.assertEquals(max_length, 50)
#
#     def test_object_name_is_course_name_comma_start_day_comma_location(self):
#         course = Course.objects.get(id=1)
#         expected_object_name = f"{course.course_name}, {course.start_day}, {course.location}"
#         self.assertEquals(expected_object_name, str(course))
#
#     def test_get_absolute_url(self):
#         course = Course.objects.get(id=1)
#         # This will also fail if the urlconf is not defined.
#         self.assertEquals(course.get_absolute_url(), '/catalog/course/1')
#
