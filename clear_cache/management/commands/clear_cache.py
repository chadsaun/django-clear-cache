from django.conf import settings
from django.core.cache import cache, caches, InvalidCacheBackendError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """A simple management command which clears the site-wide cache."""
    help = 'Fully clear your site-wide cache. No arguments will clear the default cache.'
    
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('cache_names', nargs='*', type=str, help='Name of a specific cache to clear')
        
        # Named (optional) arguments
        parser.add_argument('--all', action='store_true', help='Clear all caches')
    
    def handle(self, *args, **kwargs):
        cache_names = kwargs.get('cache_names')
        delete_all = kwargs.get('all')
        
        if not cache_names:
            cache_names = ['default']
        
        try:
            assert settings.CACHES
        except AttributeError:
            raise CommandError(self.style.WARNING('You have no cache configured!\n'))
        
        if delete_all:
            cache_names = []
            for name in settings.CACHES:
                cache_names.append(name)
        
        for cache_name in cache_names:
            try:
                cache = caches[cache_name]
                cache.clear()
                self.stdout.write(self.style.SUCCESS("Cache '{}' has been cleared!\n".format(cache_name)))
            except InvalidCacheBackendError as e:
                self.stdout.write(self.style.ERROR('{}\n'.format(str(e))))
