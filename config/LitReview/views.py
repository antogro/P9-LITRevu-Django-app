from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review, UserFollows, BlockUser
from django.contrib.auth import get_user_model
from .forms import TicketForm, ReviewForm
from django.db.models import Prefetch
from django.contrib import messages


@login_required
def home(request):
    """
    Permet l'affichage de la page principale,
    d'afficher les tickets et les reviews, et
    permettre la création de nouveaux tickets et
    commentaire.
    Bloque l'affichage des utilisateurs bloqué
    """
    user = request.user

    # Liste des utilisateurs bloqués
    blocked_users = BlockUser.objects.filter(user=user).values_list(
        "blocked_user", flat=True
    )

    # Liste des utilisateurs suivis, en excluant les utilisateurs bloqués
    followed_users = (
        UserFollows.objects.filter(user=user)
        .exclude(followed_user__in=blocked_users)
        .values_list("followed_user", flat=True)
    )

    # Inclure l'utilisateur lui-même dans les utilisateurs suivis
    followed_users = list(followed_users) + [user.id]

    # Récupérer les tickets et critiques des utilisateurs suivis,
    # en excluant les utilisateurs bloqués
    tickets = (
        Ticket.objects.filter(user__in=followed_users)
        .exclude(user__in=blocked_users)
        .order_by("-time_created")
    )
    reviews = (
        Review.objects.filter(user__in=followed_users)
        .exclude(user__in=blocked_users)
        .order_by("-time_created")
    )

    combined = []
    for ticket in tickets:
        ticket_reviews = Review.objects.filter(ticket=ticket).exclude(
            user__in=blocked_users
        )
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
            x["ticket"].time_created
            if x.get("is_ticket") else x["review"].time_created
        ),
        reverse=True,
    )

    return render(request, "LitReview/home.html", {"combined": combined})


@login_required
def blocked_user(request):
    """
    Permet de bloquer un utilisateur

    """
    user = request.user
    if request.method == "POST":
        blocked_username = request.POST.get("blocked_username")
        if blocked_username:
            blocked_user = get_object_or_404(
                get_user_model(), username=blocked_username
            )
            if user != blocked_user:
                # Bloquer l'utilisateur
                BlockUser.objects.get_or_create(
                    user=user,
                    blocked_user=blocked_user)

                # Désabonner automatiquement des deux côtés
                UserFollows.objects.filter(
                    user=user, followed_user=blocked_user
                ).delete()
                UserFollows.objects.filter(
                    user=blocked_user, followed_user=user
                ).delete()

                messages.success(request, f"Vous avez bloqué {blocked_user}.")
            else:
                messages.error(
                    request,
                    "Vous ne pouvez pas vous bloquer vous-même")

    # Récupérer toutes les données nécessaires
    followed_users = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(followed_user=user)
    blocked_users = BlockUser.objects.filter(user=user)

    context = {
        "user": user,
        "followed_users": followed_users,
        "followers": followers,
        "blocked_users": blocked_users,
    }
    return render(request, "LitReview/followers.html", context)


@login_required
def unblock_user(request):
    """
    Permet de débloquer un utilisateur qui a été préalablement bloqué.
    """
    user = request.user
    # Liste des utilisateurs à débloquer
    if request.method == "POST":
        unblock_username = request.POST.get("unblock_username")
        if unblock_username:
            unblock_user = get_object_or_404(
                get_user_model(), username=unblock_username
            )
            # débloque l'utilisateur
            BlockUser.objects.filter(
                user=user,
                blocked_user=unblock_user
                ).delete()
            messages.success(request, f"Vous avez débloqué {unblock_user}")

    followed_users = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(followed_user=user)
    blocked_users = BlockUser.objects.filter(user=user)

    context = {
        "user": user,
        "followed_users": followed_users,
        "followers": followers,
        "blocked_users": blocked_users,
    }
    return render(request, "LitReview/followers.html", context)


@login_required
def followers(request):
    """
    Permet de voir les utilisateurs qui suivent l'utilisateur connecté
    """

    # Liste les differents utilisateurs
    user = request.user
    followed_users = UserFollows.objects.filter(user=user)
    followers = UserFollows.objects.filter(followed_user=user)
    blocked_users = BlockUser.objects.filter(user=user)

    context = {
        "user": user,
        "followed_users": followed_users,
        "followers": followers,
        "blocked_users": blocked_users,
    }
    return render(request, "LitReview/followers.html", context)


@login_required
def follow_user(request):
    """
    Permet à l'utilisateur de suivre un autre utilisateur

    """
    user = request.user
    followed_username = request.GET.get("username")

    if followed_username:
        # Suivi de l'utilisateur
        followed_user = get_object_or_404(
            get_user_model(),
            username=followed_username)
        if followed_user != user:  # Empêche de se suivre soi-même

            existing_follow = UserFollows.objects.filter(
                user=user, followed_user=followed_user
            )
            # Vérifie si la relation exite déjà
            if existing_follow.exists():
                messages.info(
                    request,
                    f"Vous suivez déjà {followed_user.username}.")
            else:
                # Crée une nouvelle relation de suivi
                UserFollows.objects.create(
                    user=user,
                    followed_user=followed_user)
                messages.success(
                    request,
                    f"Vous suivez maintenant {followed_user.username}."
                )
        else:
            messages.error(
                request,
                "Vous ne pouvez pas vous suivre vous-même.")
    return redirect("followers")


@login_required
def unfollow_user(request):
    """
    Permet de ne plus suivre un autre utilisateur
    """
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
                existing_follow.delete()
                messages.success(
                    request, f"Vous ne suivez plus {unfollow_user.username}."
                )
            else:
                messages.error(request, "Vous ne suivez pas cet utilisateur.")
        return redirect("followers")


def my_posts(request):
    """
    Permet à l'utilisateur d'afficher ses propres publications.
    Et bloque l'affichage des publications d'autres utilisateurs bloqué.
    """
    user = request.user

    # Récuperer les Utilisateurs bloqués
    blocked_users = BlockUser.objects.filter(user=user).values_list(
        "blocked_user", flat=True
    )
    # Récupérer tous les tickets de l'utilisateur,
    # avec pré-chargement des critiques associées
    user_tickets = (
        Ticket.objects.filter(user=user)
        .exclude(user__in=blocked_users)
        .prefetch_related(
            Prefetch(
                "review_set",
                queryset=Review.objects.filter(user=user).exclude(
                    user__in=blocked_users
                ),
                to_attr="user_reviews",
            )
        )
        .distinct()
    )

    # Récupérer toutes les critiques de l'utilisateur
    user_reviews = Review.objects.filter(user=user).exclude(
        user__in=blocked_users).select_related("ticket").distinct()

    other_user_reviews_on_user_tickets = (
        Review.objects.filter(ticket__user=user).exclude(
            user__in=blocked_users).exclude(user=user).distinct()
    )

    combined_posts = []

    # Ajout des tickets avec leurs critiques associées
    for ticket in user_tickets:
        combined_posts.append(
            {
                "is_ticket": True,
                "ticket": ticket,
                "reviews": ticket.user_reviews,
            }
        )

    # Ajout des critiques de l'utilisateur
    for review in user_reviews:
        combined_posts.append(
            {
                "is_review": True,
                "review": review,
            }
        )

    # Ajout des critiques faites par d'autres utilisateurs
    # sur les tickets de l'utilisateur
    for review in other_user_reviews_on_user_tickets:
        combined_posts.append(
            {
                "is_review_response_to_user_ticket": True,
                "review": review,
            }
        )

    context = {
        "combined_posts": combined_posts,
    }

    return render(request, "LitReview/my_posts.html", context)


@login_required
def create_ticket(request):
    """
    Permet à un utilisateur de créer un nouveau ticket (demande de critique)
    """
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        # Vérifie si le formulaire est valide
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
    """
    Permet de créer une critique, soit sur un ticket existant,
    soit en créant un nouveau ticket simultanément
    """
    # Si ticket_id fourni, récupère le ticket ou 404
    ticket = get_object_or_404(Ticket, id=ticket_id) if ticket_id else None

    # Empêcher un utilisateur de soumettre
    # plusieurs critiques pour le même ticket
    if ticket and Review.objects.filter(
            ticket=ticket,
            user=request.user).exists():
        return redirect(
            "home"
        )

    # Crée un formulaire de ticket uniquement si pas de ticket existant
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        ticket_form = TicketForm(
            request.POST, request.FILES) if not ticket else None

        # Vérifie si les formulaires sont valides
        if review_form.is_valid() and (
                ticket_form is None or ticket_form.is_valid()):
            review = review_form.save(commit=False)
            review.user = request.user

            # Si ticket existant, affecte le ticket

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
        {"review_form": review_form,
            "ticket_form": ticket_form,
            "ticket": ticket},
    )


@login_required
def edit_ticket(request, ticket_id):
    """
    Permet à l'utilisateur de modifier un ticket qu'il a créé
    """
    # Récupère le ticket ou 404, vérifie que l'utilisateur est le propriétaire
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    edit_form = TicketForm(instance=ticket)

    if request.method == "POST":
        if "edit_ticket" in request.POST:
            edit_form = TicketForm(
                request.POST,
                request.FILES,
                instance=ticket)
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
    """
    Permet à l'utilisateur de modifier une critique (review) qu'il a créé
    """
    # Récupère la review ou 404, vérifie que l'utilisateur est le propriétaire
    review = get_object_or_404(Review, id=review_id, user=request.user)
    edit_form = ReviewForm(instance=review)
    if request.method == "POST":
        if "edit_review" in request.POST:
            edit_form = ReviewForm(
                request.POST, request.FILES, instance=review)
            if edit_form.is_valid():
                edit_form.save()
                return redirect("my_posts")

    context = {"edit_form": edit_form}

    return render(request, "LitReview/edit_review.html", context=context)


@login_required
def delete_ticket(request, ticket_id):
    """
    Permet à l'utilisateur de supprimer un ticket qu'il a créé
    """
    # Récupère la ticket ou 404, vérifie que l'utilisateur est le propriétaire
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    # Supprime le ticket
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Le ticket a été supprimé avec succès.")
        return redirect("my_posts")

    # Redirige immédiatement si ce n'est pas une requête POST
    return redirect(
        "my_posts"
    )


@login_required
def delete_review(request, review_id):
    """
    Permet à l'utilisateur de supprimer une critique (review) qu'il a créé
    """
    # Récupère la review ou 404, vérifie que l'utilisateur est le propriétaire
    review = get_object_or_404(Review, id=review_id, user=request.user)

    # Protection contre les suppressions accidentelles
    if request.method == "POST":
        review.delete()
        messages.success(request, "La critique a été supprimée avec succès.")
        return redirect("my_posts")

    return redirect(
        "my_posts"
    )  # Redirige immédiatement si ce n'est pas une requête POST
