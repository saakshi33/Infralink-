from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from infra.models import Project

class Command(BaseCommand):
    help = "Send emails to project heads if the project is nearing its deadline."

    def handle(self, *args, **kwargs):
        today = now().date()
        two_days_later = today + timedelta(days=2)

        # Query projects that are ending in less than 2 days
        projects_near_deadline = Project.objects.filter(end_date__lte=two_days_later, end_date__gte=today)

        if projects_near_deadline.exists():
            for project in projects_near_deadline:
                project_head_email = project.project_head.email  # Assuming project_head is a user with an email field
                
                # Send the email to the project head
                send_mail(
                    subject=f'Project Deadline Approaching: {project.project_name}',
                    message=f'Dear {project.project_head},\n\nYour project "{project.project_name}" is ending on {project.end_date}. Please ensure necessary actions are taken before the deadline.',
                    from_email='infralink04@gmail.com',
                    recipient_list=[project_head_email],
                    fail_silently=False,
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully sent email to {project_head_email} for project "{project.project_name}"'))

        else:
            self.stdout.write(self.style.WARNING('No projects nearing their deadlines.'))

