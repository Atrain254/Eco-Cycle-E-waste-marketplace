from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Item, UserProfile
from .forms import ItemForm, UserRegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Item, UserProfile, Category # Make sure Category is imported!

# Your existing view
def item_list(request):
    # 1. Start with all available items
    items = Item.objects.filter(is_available=True).order_by('-created_at')
    
    # 2. Get all categories to populate the dropdown menu
    categories = Category.objects.all()
    
    # 3. Check if the user typed anything in the search box or selected a category
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    # 4. If they searched for a word, filter the items (checks title OR description)
    if query:
        items = items.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        
    # 5. If they selected a category from the dropdown, filter by that category
    if category_id:
        items = items.filter(category_id=category_id)
     # 6. GRAB THE USER'S PROFILE
    # You MUST define this default value first so the variable always exists
    user_profile = None
    
    # Then run the check to see if they are logged in
    if request.user.is_authenticated:
        try:
            user_profile = request.user.userprofile
        except:
            user_profile = None
            
    # 7. ADD THE PROFILE TO THE CONTEXT DICTIONARY
    context = {
        'items': items,
        'categories': categories,
        'profile': user_profile,  
    }
    
    return render(request, 'marketplace/item_list.html', context)

#login session to add items
@login_required 
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES) 
        if form.is_valid():
            new_item = form.save(commit=False)
            
            # Assign the item to the person actually logged in!
            new_item.owner = request.user 
            
            new_item.save()
            return redirect('item_list')
    else:
        form = ItemForm()

    return render(request, 'marketplace/add_item.html', {'form': form})


# Our NEW view for adding items
def add_item(request):
    if request.method == 'POST':
        # Add request.FILES right here so Django grabs the photo!
        form = ItemForm(request.POST, request.FILES) 
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.owner = User.objects.first() 
            new_item.save()
            return redirect('item_list')
    else:
        form = ItemForm()

    return render(request, 'marketplace/add_item.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # 1. Save the basic User account (Username, Email, Password)
            user = form.save()
            
            # 2. Create and link their Eco-Cycle Profile (Household vs Technician)
            UserProfile.objects.create(
                user=user,
                user_type=form.cleaned_data.get('user_type'),
                phone_number=form.cleaned_data.get('phone_number')
            )
            
            # 3. Log them in immediately so they don't have to retype their info
            login(request, user)
            
            # 4. Send them to the marketplace
            return redirect('item_list')
    else:
        form = UserRegistrationForm()

    return render(request, 'marketplace/register.html', {'form': form})


@login_required
def dashboard(request):
    try:
        profile = request.user.userprofile
    except:
        profile = None
        
    if profile and profile.user_type == 'technician':
        # Technicians see items they have successfully claimed
        items = Item.objects.filter(claimed_by=request.user)
        dashboard_title = "My Claimed Salvage"
    else:
        # Households (or Admins) hit this block.
        # We MUST define 'items' here so the variable exists!
        
        # Safe fallback: Since we haven't strictly linked items to household owners yet, 
        # we will just show them all items for now to prevent a crash.
        items = Item.objects.all() 
        dashboard_title = "My Listed E-Waste"
        
    return render(request, 'marketplace/dashboard.html', {'items': items, 'profile': profile, 'dashboard_title': dashboard_title})


    # 1. View to display a single item's details
@login_required
def item_detail(request, pk):
    # Fetch the specific item using its ID, or show a 404 error if it doesn't exist
    item = get_object_or_404(Item, pk=pk)
    
    try:
        profile = request.user.userprofile
    except:
        profile = None
        
    return render(request, 'marketplace/item_detail.html', {'item': item, 'profile': profile})


# 2. Action view to handle clicking the "Claim" button
@login_required
def claim_item(request, pk):
    if request.method == 'POST':
        item = get_object_or_404(Item, pk=pk)
        
        # Change availability to False so it disappears from the open marketplace
        item.is_available = False
        item.save()
        item.claimed_by = request.user 
        item.save()
        # Redirect the technician straight back to their dashboard
        return redirect('dashboard')

