from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Transaction, BudgetPlanCategory, BudgetPlan, Notification, PasswordResetCode


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'country')
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'country']
    list_filter = ['country']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name', 'phone_number', 'country')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    ordering = ('username',)
    filter_horizontal = ()


# @admin.register(CustomUser)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'country')
#     search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'country']
#     list_filter = ['country']

    # def get_user_id(self, obj):
    #     return obj.user_id

    # get_user_id.short_description = 'User ID'

@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'code', 'timestamp']
    search_fields = ['user__username', 'user__email']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'transaction_type', 'amount', 'date']
    search_fields = ['title', 'category']
    list_filter = ['transaction_type', 'date','category']

@admin.register(BudgetPlanCategory)
class BudgetPlanCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_title', 'percentage', 'color']
    search_fields = ['category_title']

@admin.register(BudgetPlan)
class BudgetPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    filter_horizontal = ['categories']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'body']
    search_fields = ['title', 'category']
    list_filter = ['category']
