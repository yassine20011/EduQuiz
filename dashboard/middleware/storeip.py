import datetime

import requests
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from user_agents import parse

from dashboard.models import DataRelatedToUser, Profile


class SaveIpAddressMiddleware(MiddlewareMixin):
    
    def get_ip(self, request):
        # sourcery skip: assign-if-exp, inline-immediately-returned-variable
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip       

    def get_geolocation(self, ip):
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}')
            response.raise_for_status()
            if response.json()['status'] == 'success':
                return response.json()['regionName']
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err) from err
        
    
    def device_name(self, request):
        http_user_agent = request.META.get('HTTP_USER_AGENT')
        return parse(http_user_agent)    

    def process_request(self, request):  # sourcery skip: hoist-statement-from-if, merge-duplicate-blocks, remove-redundant-if, use-named-expression
        http_user_agent = request.META.get('HTTP_USER_AGENT')
        user_agent = parse(http_user_agent)
        ip = self.get_ip(request)
        geoip = self.get_geolocation(ip)

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                ip_addresses = DataRelatedToUser.objects.filter(profile=profile).order_by('-date')[0]
                if str(ip_addresses) != str(ip):
                    data = DataRelatedToUser(profile=profile, date=timezone.now(), ip_address=ip,device_name=user_agent, http_user_agent=http_user_agent, geoip=geoip)
                    data.save()
            except DataRelatedToUser.DoesNotExist and IndexError:
                profile = Profile.objects.get(user=request.user)
                data = DataRelatedToUser(profile=profile, date=timezone.now(), ip_address=ip, device_name=user_agent, http_user_agent=http_user_agent)
                data.save()
            return None