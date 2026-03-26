"""AppConfig for the blog application."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    name = "apps.blog"
    label = "blog"
    verbose_name = "Blog"

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.contrib.auth import management as auth_mgmt
        from django.contrib.auth.signals import user_logged_in
        from django.utils.timezone import now

        # Fix 1: create_permissions incompatible with ObjectIdAutoField
        def _noop_create_permissions(app_config, verbosity=2, interactive=True,
                                     using="default", apps=None, **kwargs):
            pass

        post_migrate.disconnect(
            auth_mgmt.create_permissions,
            dispatch_uid="django.contrib.auth.management.create_permissions",
        )
        post_migrate.connect(
            _noop_create_permissions,
            dispatch_uid="django.contrib.auth.management.create_permissions",
        )

        # Fix 2: AuthConfig.ready() connects update_last_login with dispatch_uid
        # "update_last_login". It calls user.save(update_fields=["last_login"])
        # which uses force_update=True and fails with MongoDB ObjectIdAutoField.
        # Disconnect by the exact dispatch_uid and replace with a queryset update.
        user_logged_in.disconnect(dispatch_uid="update_last_login")

        def _safe_update_last_login(sender, user, **kwargs):
            try:
                sender.objects.filter(pk=user.pk).update(last_login=now())
            except Exception:
                pass

        user_logged_in.connect(
            _safe_update_last_login,
            dispatch_uid="update_last_login",
        )
