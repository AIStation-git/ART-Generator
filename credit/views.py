from django.shortcuts import render
from django.shortcuts import render
from accounts.models import User
from .forms import UpdateCreditForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

# Create your views here.

class UpdateCreditView(View):
    template_name = 'credit.html'
    
    def get(self, request):
        form = UpdateCreditForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = UpdateCreditForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            credit = form.cleaned_data['credit']
            
            # Update user with given email or create new user if email doesn't exist
            # user, created = User.objects.get_or_create(email=email)

            # Update user with given email or create new user if email doesn't exist
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'User with this email does not exist.')
                return render(request, self.template_name, {'form': form})
        


            user.credit = user.credit + credit if user.credit is not None else credit
            user.save()
            
            messages.success(request, 'Credit updated successfully')
            return redirect('buy')
        else:
            messages.error(request, 'Invalid form submission. Please correct the errors below.')

        return render(request, self.template_name, {'form': form})
