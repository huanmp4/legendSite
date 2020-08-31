from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.news.models import News,Banner,NewsComment,Category
from apps.course.models import CourseOrder,Course,CourseCategory,Teacher
class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('hello world'))
        #编辑组权限
        #从django-content_type中查到model的id
        edit_content_types = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(NewsComment),
            ContentType.objects.get_for_model(Category)
        ]
        #从Permission表中过滤models的id
        permission_edit = Permission.objects.filter(content_type_id__in=edit_content_types)
        edit = Group.objects.create(name='编辑组')
        edit.permissions.set(permission_edit)
        edit.save()
        self.stdout.write(self.style.SUCCESS('编辑组已保存'))
        #财务组
        finance_content_type = [
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(Teacher),
        ]
        permission_finance = Permission.objects.filter(content_type_id__in=finance_content_type)
        finance = Group.objects.create(name='财务组')
        finance.permissions.set(permission_finance)
        finance.save()
        self.stdout.write(self.style.SUCCESS('财务组已保存'))

        permission_admin = permission_edit.union(permission_finance)
        admin = Group.objects.create(name='管理员组')
        admin.save()
        self.stdout.write(self.style.SUCCESS('管理组已保存'))



