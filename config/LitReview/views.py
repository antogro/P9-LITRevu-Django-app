from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model
from .forms import TicketForm, ReviewForm
from django.db.models import Prefetch
from django.contrib import messages


@login_required
def home(request):
    user = request.user

    # Liste des utilisateurs suivis
    followed_users = UserFollows.objects.filter(user=user).values_list(
        "followed_user", flat=True
    )

    # Inclure l'utilisateur lui-même dans les utilisateurs suivis
    followed_users = list(followed_users) + [user.id]

    # Récupérer les tickets et critiques des utilisateurs suivis
    tickets = Ticket.objects.filter(user__in=followed_users).order_by("-time_created")
    reviews = Review.objects.filter(user__in=followed_users).order_by("-time_created")

    combined = []

    for ticket in tickets:
        ticket_reviews = Review.objects.filter(ticket=ticket)
        has_user_review = ticket_reviews.filter(user=request.user).exists()
        combined.append(
            {
                "is_ticket": True,
                "ticket": ticket,
                "has_user_review": has_user_review,
                "reviews": ticket_reviews,
            }
        )

    for review in reviews:
        if not any(
            item
            for item in combined
            if item.get("is_ticket") and item["ticket"] == review.ticket
        ):
            combined.append(
                {
                    "is_review": True,
                    "review": review,
                    "ticket": review.ticket,
                }
            )

    combined.sort(
        key=lambda x: (
            x["ticket"].time_created if x.get("is_ticket") else x["review"].time_created
        ),
        reverse=True,
    )

    return render(request, "LitReview/home.html", {"combined": combined})


@login_required
def followers(request):
    user = request.user

    # Récupérer les utilisateurs que l'utilisateur courant suit
    followed_users = UserFollows.objects.filter(user=user)

    # Récupérer les utilisateurs qui suivent l'utilisateur courant
    followers = UserFollows.objects.filter(followed_user=user)

    context = {
        "followed_users": followed_users,  # Utilisateurs suivis par l'utilisateur courant
        "followers": followers,  # Utilisateurs qui suivent l'utilisateur courant
    }

    return render(request, "LitReview/followers.html", context)


@login_required
def follow_user(request):
    user = request.user
    followed_username = request.GET.get("username")

    if followed_username:
        followed_user = get_object_or_404(get_user_model(), username=followed_username)
        if followed_user != user:  # Empêcher de se suivre soi-même
            existing_follow = UserFollows.objects.filter(
                user=user, followed_user=followed_user
            )

            if existing_follow.exists():
                # Afficher un message indiquant que l'utilisateur est déjà suivi
                messages.info(request, f"Vous suivez déjà {followed_user.username}.")
            else:
                # Suivre l'utilisateur s'il n'est pas déjà suivi
                UserFollows.objects.create(user=user, followed_user=followed_user)
                messages.success(
                    request, f"Vous suivez maintenant {followed_user.username}."
                )
        else:
            messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
    return redirect("followers")


@login_required
def unfollow_user(request):
    if request.method == "POST":
        user = request.user
        unfollow_username = request.POST.get("unfollow_username")

        if unfollow_username:
            unfollow_user = get_object_or_404(
                get_user_model(), username=unfollow_username
            )
            existing_follow = UserFollows.objects.filter(
                user=user, followed_user=unfollow_user
            )

            if existing_follow.exists():
                # Désabonner
                existing_follow.delete()
                messages.success(
                    request, f"Vous ne suivez plus {unfollow_user.username}."
                )
            else:
                messages.error(request, "Vous ne suivez pas cet utilisateur.")
        return redirect("followers")


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")
    else:
        form = TicketForm()
    return render(request, "LitReview/create_ticket.html", {"form": form})


@login_required
def create_review(request, ticket_id=None):
    ticket = get_object_or_404(Ticket, id=ticket_id) if ticket_id else None

    # Empêcher un utilisateur de soumettre plusieurs critiques pour le même ticket
    if ticket and Review.objects.filter(ticket=ticket, user=request.user).exists():
        return redirect(
            "home"
        )  # Ou afficher un message indiquant que la critique existe déjà

    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(request.POST, request.FILES) if not ticket else None

        if review_form.is_valid() and (ticket_form is None or ticket_form.is_valid()):
            review = review_form.save(commit=False)
            review.user = request.user

            if ticket_form:
                ticket = ticket_form.save(commit=False)
                ticket.user = request.user
                ticket.save()

            review.ticket = ticket
            review.save()
            return redirect("home")
    else:
        review_form = ReviewForm()
        ticket_form = TicketForm() if not ticket else None

    return render(
        request,
        "LitReview/create_review.html",
        {"review_form": review_form, "ticket_form": ticket_form, "ticket": ticket},
    )



def my_posts(request):
    user = request.user

    # Récupérer tous les tickets de l'utilisateur, avec pré-chargement des critiques associées
    user_tickets = Ticket.objects.filter(user=user).prefetch_related(
        Prefetch('review_set', queryset=Review.objects.filter(user=user), to_attr='user_reviews')
    ).distinct()

    # Récupérer toutes les critiques de l'utilisateur
    user_reviews = Review.objects.filter(user=user).select_related('ticket').distinct()

    # Critiques faites par d'autres utilisateurs sur les tickets de l'utilisateur
    other_user_reviews_on_user_tickets = Review.objects.filter(ticket__user=user).exclude(user=user).distinct()

    combined_posts = []

    # Ajout des tickets avec leurs critiques associées
    for ticket in user_tickets:
        combined_posts.append({
            'is_ticket': True,
            'ticket': ticket,
            'reviews': ticket.user_reviews,  # Critiques de l'utilisateur sur ce ticket
        })

    # Ajout des critiques de l'utilisateur
    for review in user_reviews:
        combined_posts.append({
            'is_review': True,
            'review': review,
        })

    # Ajout des critiques faites par d'autres utilisateurs sur les tickets de l'utilisateur
    for review in other_user_reviews_on_user_tickets:
        combined_posts.append({
            'is_review_response_to_user_ticket': True,
            'review': review,
        })

    context = {
        'combined_posts': combined_posts,
    }

    return render(
        request, "LitReview/my_posts.html", context
    )


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    edit_form = TicketForm(instance=ticket)

    if request.method == "POST":
        if "edit_ticket" in request.POST:
            edit_form = TicketForm(request.POST, request.FILES, instance=ticket)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("my_posts")
    context = {
        "edit_form": edit_form,
        "ticket": ticket,
    }

    return render(request, "LitReview/edit_ticket.html", context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    edit_form = ReviewForm(instance=review)
    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_form = ReviewForm(request.POST, request.FILES, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("my_posts")

    context = {"edit_form": edit_form}

    return render(request, "LitReview/edit_review.html", context=context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "La critique a été supprimée avec succès.")
        return redirect("my_posts")

    return redirect(
        "my_posts"
    )  # Redirige immédiatement si ce n'est pas une requête POST


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès.")
        return redirect("my_posts")

    return redirect(
        "my_posts"
    )  # Redirige immédiatement si ce n'est pas une requête POST


@login_required
def edit_post(request):
    post = get_object_or_404(Post, id=request.POST.get("post_id"), user=request)
