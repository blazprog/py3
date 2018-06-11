from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
import datetime
from django.utils.translation import ugettext_lazy as _
from .models import Sprint, Task

User = get_user_model()

class SprintSerializer(serializers.ModelSerializer):

	links = serializers.SerializerMethodField()

	class Meta:
		model = Sprint
		fields = ('id', 'name', 'description', 'end', 'links')
	def get_links(self, obj):
		request = self.context['request']
		return {
			'self': reverse('sprint-detail',
				kwargs={'pk': obj.pk},request=request),
			'tasks': reverse('task-list',
				request=request) + '?sprint={}'.format(obj.pk),
		}
	def validate_end(self, data):
		end_date = data
		new = not self.instance
		changed = self.instance and self.instance.end != end_date
		if (new or changed) and (end_date < datetime.date.today()):
			msg = _('End date cannot be in the past.')
			raise serializers.ValidationError(msg)
		return data


class TaskSerializer(serializers.ModelSerializer):

	assigned = serializers.SlugRelatedField(slug_field=User.USERNAME_FIELD, queryset=User.objects.all(), required=False)
	status_display = serializers.SerializerMethodField()
	links = serializers.SerializerMethodField()

	class Meta:
		model = Task
		fields = ('id', 'name', 'description', 'status', 'status_display', 'sprint', 'order', 'assigned', 'started', 'due', 'completed', 'links')

	def get_status_display(self, obj):
		return obj.get_status_display()   
	def get_links(self, obj):
		request = self.context['request']
		links = {
			'self': reverse('task-detail',
				kwargs={'pk': obj.pk}, request=request),
			'sprint': None,
			'assigned': None
		}
		if obj.sprint_id:
			links['sprint'] = reverse('sprint-detail',
				kwargs={'pk': obj.sprint_id}, request=request)
		if obj.assigned:
			links['assigned'] = reverse('user-detail',
				kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)
		return links
	def validate_sprint(self, data):
		sprint = data
		if self.instance and self.instance.pk:
			if sprint != self.instance.sprint:
				if self.instance.status == Task.STATUS_DONE:
					msg = _('Cannot change the sprint of a completed task.')
					raise serializers.ValidationError(msg)
				if sprint and sprint.end < datetime.date.today():
					msg = _('Cannot assign tasks to past sprints.')
					raise serializers.ValidationError(msg)
		else:
			if sprint and sprint.end < datetime.date.today():
				msg = _('Cannot add tasks to past sprints.')
				raise serializers.ValidationError(msg)
		return data

	def validate(self, attrs):
		sprint = attrs.get('sprint')
		status = int(attrs.get('status'))
		started = attrs.get('started')
		completed = attrs.get('completed')
		if not sprint and status != Task.STATUS_TODO:
			msg = _('Backlog tasks must have "Not Started" status.')
			raise serializers.ValidationError(msg)
		if started and status == Task.STATUS_TODO:
			msg = _('Started date cannot be set for not started tasks.')
			raise serializers.ValidationError(msg)
		if completed and status != Task.STATUS_DONE:
			msg = _('Completed date cannot be set for uncompleted tasks.')
			raise serializers.ValidationError(msg)
		return attrs

class UserSerializer(serializers.ModelSerializer):

	full_name = serializers.CharField(source='get_full_name', read_only=True)
	links = serializers.SerializerMethodField()

	class Meta:
		model = User
		fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')
	def get_links(self, obj):
		request = self.context['request']
		username = obj.get_username()
		return {
			'self': reverse('user-detail',
				kwargs={User.USERNAME_FIELD: username}, request=request),
			'tasks': '{}?assigned={}'.format(
				reverse('task-list', request=request), username)
		}